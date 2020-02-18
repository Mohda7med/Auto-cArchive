import pandas as pd
import psycopg2


def main():
    # read the the unified dataset file 
    unified_schema = pd.read_csv('/home/ubuntu/data/unified_dataset.csv')
    
    #Create unique object ids throughout the unified dataset
    new_object_id = range(0, len(unified_schema['object_id']))
    unified_schema['object_id'] = new_object_id
    
    # Assign new sample ids, because current ids have different formats
    unified_schema = unified_schema.assign(sample_id=(unified_schema['sample_id']).astype('category').cat.codes)
    
    # fix the text of the object_class column
    unified_schema["object_class"]= unified_schema["object_class"].apply(str.lower)
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.adult", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.child", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.construction_worker", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.personal_mobility", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.police_officer", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.stroller", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("human.pedestrian.wheelchair", "pedestrian")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.bicycle", "bicycle")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.bus.bendy", "bus")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.bus.rigid", "bus")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.car", "car")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.emergency.ambulance", "ambulance")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.emergency.police", "police vehicle")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.motorcycle", "motorcycle")
    unified_schema["object_class"]= unified_schema["object_class"].str.replace("vehicle.truck", "truck")
    
    #save the clean schema in a csv file in the data folder 
    with open(r'/home/ubuntu/data/indexed_schema.csv', 'a') as f:
        unified_schema.to_csv(f, header=f.tell()==0, index=False)
        
    # Creating db table from the new csv file:
    try:
        conn = psycopg2.connect(host="ec2-54-70-11-35.us-west-2.compute.amazonaws.com", database="postgres", user="postgres", password="", port="5432")
    except (Exception) as error:
        print("I am unable to connect to the database" + str(error)) 
        exit()
    cur = conn.cursor()
    try:
        cur.execute("""
        DROP TABLE IF EXISTS Objects;
        CREATE TABLE Objects (
        sample_id integer, 
        object_id integer PRIMARY KEY,
        center_x numeric,
        center_y numeric,
        center_z numeric,
        width numeric,
        length numeric,
        height numeric,
        yaw numeric,
        object_class text,
        image_location_in_s3 text);""")
    except:
        print("Unable to create table")
    # fill the table from the csv file 
    with open('/home/ubuntu/data/indexed_schema.csv', 'r') as f:
        next(f) # Skip the header row.
        cur.copy_from(f, "Objects", sep=',')
    conn.commit()
    conn.close()
    cur.close()
    


if __name__ == '__main__':
  main()

