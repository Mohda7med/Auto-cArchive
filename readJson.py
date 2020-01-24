#!/bin/python3

import pandas as pd
import boto3
import json


bucket_name = "mohammed-autonomous-vehicles-bucket"
# file_name = "trip_data/fhv_tripdata_2015-01.csv"

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)

# Iterates through all the objects, doing the pagination for you. Each obj
# is an ObjectSummary, so it doesn't contain the body. You'll need to call
# get to get the whole body.

for obj in bucket.objects.all():
  if  obj.size > 0:
    key = obj.key
    if 'cams_lidars' in key:
       body = obj.get()['Body']

#      data = pd.read_csv(body)
#      print (data.head())

       # read file
       with open(body, 'r') as myfile:
          data=myfile.read()

       # parse file
       text = json.loads(data)
#       text = json.loads(body)
       print ( str(text['box_0']) )





