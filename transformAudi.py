#!/home/ubuntu/anaconda3/bin/python

import pandas as pd
import numpy as np
import os 
import json


def json_to_schema(file):
    audi_file = pd.read_json(file)
    df = audi_file.loc[['center','class','id', 'rot_angle', 'size']]
    schema = pd.DataFrame(index=range(len(df.columns)), columns = ['sample_id', 'object_id', 'center_x', 'center_y', 'center_z', 'width', 'length', 'height', 'angle', 'object_class', 'data_location_in_s3'])
    schema["sample_id"]= file[-14:-5]
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
    with open(r'/Users/mohammed/Documents/export_dataframe.csv', 'a') as f:
        schema.to_csv(f, header=f.tell()==0, index=False)



def main():
    rootdir = r'/Users/mohammed/Downloads/a2d2-preview/camera_lidar_semantic_bboxes'
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
           if "label3D" in file and file.endswith(".json"):
                json_file = os.path.join(subdir, file)
                json_to_schema(json_file)
                #print(path)


if __name__ == '__main__':
  main()


