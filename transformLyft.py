import pandas as pd
import numpy as np
import random
import json
from squaternion import euler2quat, quat2euler, Quaternion
from lyft_dataset_sdk.lyftdataset import LyftDataset
from lyft_dataset_sdk.lyftdataset import LyftDatasetExplorer
from lyft_dataset_sdk.utils.geometry_utils import BoxVisibility   


def main():
    #import dataset and read files
    level5data = LyftDataset(data_path='/home/ubuntu/lyft-bucket', json_path='/home/ubuntu/lyft-bucket/v1.02-train', verbose=True)
    instance = pd.read_json('/home/ubuntu/lyft-bucket/v1.02-train/instance.json')
    category = pd.read_json('/home/ubuntu/lyft-bucket/v1.02-train/category.json')
    sample_annotation = pd.read_json('/home/ubuntu/lyft-bucket/v1.02-train/sample_annotation.json')
    instance.rename(columns = {'token':'object_id'}, inplace = True)

    # join instance with category get object_id and class + last annotation
    df = pd.merge(instance, category, left_on="category_token", right_on="token").drop(['category_token','token','nbr_annotations', 'first_annotation_token', 'description'], axis=1)
    df.rename(columns = {'name':'object_class'}, inplace = True)

    # join the previoud dataframe with with annotaions dataframe to get all the info about objects
    df2 = pd.merge(df, sample_annotation, left_on="last_annotation_token", right_on="token").drop(['token', 'instance_token', 'visibility_token', 'attribute_tokens','prev', 'next', 'num_lidar_pts', 'num_radar_pts'], axis=1)
    #df2.rename(columns = {'name':'object_class'}, inplace = True)


    # Construct the schema dataframe 
    schema = pd.DataFrame(index=range(len(df2)), columns = ['sample_id', 'object_id', 'center_x', 'center_y', 'center_z', 'width', 'length', 'height', 'yaw', 'object_class', 'image_location_in_s3'])

    
    # fill sample-id, object_id, object_class columns 
    schema[["sample_id", "object_id", "object_class"]] = df2[["sample_token", "object_id", "object_class"]]
    
    # fill 'center_x', 'center_y', 'center_z', 'width', 'length', 'height' in the schema dataframe from df2 
    for (columnName, columnData) in df2.iteritems():
        if columnName == "size":
            width = []
            length = []
            height = [] 
            for i in range(len(columnData)): 
                width.append(columnData[i][0])
                length.append(columnData[i][1])
                height.append(columnData[i][2])
            schema["width"] = width
            schema["length"] = length
            schema["height"] = height
        if columnName == "translation":
            center_x = []
            center_y = []
            center_z = []
            for i in range(len(columnData)):
                center_x.append(columnData[i][0])
                center_y.append(columnData[i][1])
                center_z.append(columnData[i][2])
            schema["center_x"]= center_x
            schema["center_y"]= center_y
            schema["center_z"]= center_z
    
    
    # Calculate Yaw (Orientation of object)
    for (columnName, columnData) in df2.iteritems():
        if columnName == "rotation":
            yaw = []
            for i in range(len(columnData)): 
                rotation = columnData[i]
                quaternion = Quaternion(*rotation)
                angles = quat2euler(*quaternion, degrees=False)
                yaw.append(angles[2])
            schema["yaw"] = yaw 
            
    # Get path to image in S3 where object appears
    for (columnName, columnData) in df2.iteritems():
        if columnName == "last_annotation_token":
            pathes = []
            for i in range(len(columnData)):
                ann_record = level5data.get("sample_annotation", columnData[i])
                sample_record = level5data.get("sample", ann_record["sample_token"])        
                cams = [key for key in sample_record["data"].keys() if "CAM" in key]
                i = random.randint(0, len(cams)-1)
                data_path = level5data.get_sample_data_path(sample_record["data"][cams[i]])
                data_path = str(data_path).replace("/home/ubuntu/lyft-bucket/", "s3://mohammed-lyft-dataset-bucket/")
                pathes.append(data_path)
            schema["image_location_in_s3"] = pathes
            
    # Export to csv file 
    with open(r'/home/ubuntu/data/lyft_to_schema.csv', 'a') as f:
        schema.to_csv(f, header=f.tell()==0, index=False)


            
            
                       

if __name__ == '__main__':
  main()