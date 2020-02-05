import pandas as pd
import numpy as np
import boto3 
import json


def json_to_schema(filename, file):
    audi_file = pd.read_json(file)
    df = audi_file.loc[['center','class','id', 'rot_angle', 'size']]
    schema = pd.DataFrame(index=range(len(df.columns)), columns = ['sample_id', 'object_id', 'center_x', 'center_y', 'center_z', 'width', 'length', 'height', 'angle', 'object_class', 'image_location_in_s3'])
    schema["sample_id"] = filename[-14:-5]
    data_path = filename.replace("label3D/cam_front_center/20180807145028_label3D_frontcenter", "camera/cam_front_center/20180807145028_camera_frontcenter")
    data_path = data_path.replace("json", "png")
    data_path = "s3://mohammed-audi-dataset-bucket/" + data_path 
    sample_data = data_path
    schema["image_location_in_s3"] = sample_data 
    for lab, row in df.iterrows():
        if lab == "center":
            center_x = []
            center_y = []
            center_z = []
            centers_array = df.loc["center"].values
            for i in range(len(centers_array)):
                center_x.append(centers_array[i][0])
                center_y.append(centers_array[i][1])
                center_z.append(centers_array[i][2])
            schema["center_x"]= center_x
            schema["center_y"]= center_y
            schema["center_z"]= center_z
        if lab == "class":
            schema["object_class"]= df.loc["class"].values
        if lab == "id":
            schema["object_id"] = df.loc["id"].values
        if lab == "rot_angle":
            schema["angle"] = df.loc["rot_angle"].values
        if lab == "size":
            width = []
            length = []
            height = []
            sizes_array = df.loc["size"].values
            for i in range(len(sizes_array)):
                width.append(sizes_array[i][0])
                length.append(sizes_array[i][1])
                height.append(sizes_array[i][2]) 
            schema["width"] = width
            schema["length"] = length
            schema["height"] = height
    with open(r'/home/ubuntu/data/audi_to_schema.csv', 'a') as f:
        schema.to_csv(f, header=f.tell()==0, index=False)



def main():

    bucket_name = "mohammed-audi-dataset-bucket"
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    numFiles = 0

    for obj in bucket.objects.all():
    #for obj in bucket.objects.filter(Prefix='20180925_101535/label3D/cam_front_center/'):
      if  obj.size > 0:
           key = obj.key
           if 'label3D/cam_front_center/' in key and '.json' in key:
           #print(key)
             numFiles = numFiles + 1
             body = obj.get()['Body']
             json_to_schema(key, body)
             #break
    print(numFiles)


if __name__ == '__main__':
  main()

#20180807_145028/label3D/cam_front_center/20180807145028_label3D_frontcenter_000000091.json
#20180807_145028/label3D/cam_front_center/20180807145028_label3D_frontcenter_000000091.json
#20180807_145028/camera/cam_front_center/20180807145028_camera_frontcenter_000000091.png


