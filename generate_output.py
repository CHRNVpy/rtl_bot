from datetime import datetime, timedelta

import bson
from pymongo import MongoClient

# Replace these with your MongoDB Atlas connection string and database name
atlas_uri = ("mongodb+srv://chernovsib:bmHBSPfv0uWHAMuX@cluster0.ewhkpvr.mongodb.net/?retryWrites=true&w=majority"
             "&appName=AtlasApp")

local_bson_file = "sample_collection.bson"

# Connect to your MongoDB Atlas cluster
client = MongoClient(atlas_uri)
db = client.aggr_bot

# Specify the collection where you want to import the data
collection_name = "aggr_bot"
collection = db[collection_name]


def fill_in_db(bson_file_path: str) -> None:
    # Import the BSON data using the insert_many() method
    with open(bson_file_path, 'rb') as f:
        bson_data = f.read()
    bson_objects = list(bson.decode_all(bson_data))
    db[collection_name].insert_many(bson_objects)


def generate_pipeline(input_data: dict) -> list:
    # Convert input date strings to datetime objects
    dt_from = datetime.strptime(input_data["dt_from"], "%Y-%m-%dT%H:%M:%S")
    dt_upto = datetime.strptime(input_data["dt_upto"], "%Y-%m-%dT%H:%M:%S")
    pipeline_format = ''
    if input_data['group_type'] == 'hour':
        pipeline_format = "%Y-%m-%dT%H:00:00"
    elif input_data['group_type'] == 'day':
        pipeline_format = "%Y-%m-%d"
    elif input_data['group_type'] == 'month':
        pipeline_format = "%Y-%m"
    # Define the aggregation pipeline
    pipeline = [
        {
            "$match": {
                "dt": {"$gte": dt_from, "$lte": dt_upto}
            }
        },
        {
            "$project": {
                f"{input_data['group_type']}": {"$dateToString": {"format": pipeline_format, "date": "$dt"}},
                "value": 1
            }
        },
        {
            "$group": {
                "_id": f"${input_data['group_type']}",
                "totalValue": {"$sum": "$value"}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    return pipeline


def generate_response(input_data: dict) -> dict:
    # Convert input date strings to datetime objects
    dt_from = datetime.strptime(input_data["dt_from"], "%Y-%m-%dT%H:%M:%S")
    dt_upto = datetime.strptime(input_data["dt_upto"], "%Y-%m-%dT%H:%M:%S")

    pipeline = generate_pipeline(input_data)
    # Execute the aggregation
    result = list(collection.aggregate(pipeline))
    dataset = []
    labels = []
    if input_data['group_type'] == 'hour':
        # Generate a list of hours within the specified date range
        hour_range = []
        current_hour = dt_from
        while current_hour <= dt_upto:
            hour_range.append(current_hour.strftime("%Y-%m-%dT%H:00:00"))
            current_hour += timedelta(hours=1)
        # Create a dictionary to hold the result for each hour
        result_dict = {doc["_id"]: doc["totalValue"] for doc in result}
        # Create the output dataset and labels lists, setting the value to 0 for any missing hour
        dataset = [result_dict.get(hour, 0) for hour in hour_range]
        labels = hour_range
    elif input_data['group_type'] == 'day':
        # Generate a list of dates within the specified date range
        date_range = []
        current_date = dt_from
        while current_date <= dt_upto:
            date_range.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)
            # Create a dictionary to hold the result for each day
        result_dict = {doc["_id"]: doc["totalValue"] for doc in result}
        # Create the output dataset and labels lists
        dataset = [result_dict.get(day, 0) for day in date_range]
        labels = [day + "T00:00:00" for day in date_range]
    elif input_data['group_type'] == 'month':
        # Format the result to match the desired structure
        dataset = [doc["totalValue"] for doc in result]
        labels = [doc["_id"] + "-01T00:00:00" for doc in result]
    output = {
        "dataset": dataset,
        "labels": labels
    }
    return output
