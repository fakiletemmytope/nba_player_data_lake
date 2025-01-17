#!/bin/env python3
import requests
import json
import boto3
import os
import dotenv


dotenv.load_dotenv()
apikey = os.getenv("APIKEY")
bucket_name = os.getenv("BUCKETNAME")
url = os.getenv("APIURL")
s3_client = boto3.client("s3")
athena_client = boto3.client("athena")
glue_database_name = "nba_player_database"
athena_output_location = f"s3://{bucket_name}/athena-results/"


def fetch_nba_data():
    """Fetch NBA player data from sportsdata.io."""
    try:
        headers = {"Ocp-Apim-Subscription-Key": apikey}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        print("Fetched NBA data successfully.")
        return response.json()  # Return JSON response
    except Exception as e:
        print(f"Error fetching NBA data: {e}")
        return []


def convert_to_line_delimited_json(data):
    """Convert data to line-delimited JSON format."""
    print("Converting data to line-delimited JSON format...")
    return "\n".join([json.dumps(record) for record in data])


def store_data_s3():
    """Upload NBA data to the S3 bucket."""
    try:
        data = fetch_nba_data()
        # Convert data to line-delimited JSON
        line_delimited_data = convert_to_line_delimited_json(data)

        # Define S3 object key
        file_key = "raw-data/nba_player_data.json"

        # Upload JSON data to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimited_data,
        )
        print(f"Uploaded data to S3: {file_key}")
    except Exception as e:
        print(f"Error uploading data to S3: {e}")


def query_with_athena():
    """Set up Athena output location."""
    try:
        print(
            ("********************"),
            ("About to query table for players information"),
            ("********************"),
        )
        athena_client.start_query_execution(
            QueryString="SELECT * FROM nba_players",
            QueryExecutionContext={"Database": glue_database_name},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("completed\n")

        print(
            ("********************"),
            ("About to query table for players info where team is 'GS'"),
            ("********************"),
        )
        athena_client.start_query_execution(
            QueryString="SELECT * FROM nba_players WHERE team = 'GS'",
            QueryExecutionContext={"Database": glue_database_name},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("completed\n")

        athena_client.start_query_execution(
            QueryString=(
                ("SELECT FirstName, LastName, Team FROM"),
                ("nba_players WHERE Position = 'PG';")
            ),
            QueryExecutionContext={"Database": glue_database_name},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("completed\n")

        print("Athena output location configured successfully.")

    except Exception as e:
        print(f"Error configuring Athena: {e}")


if __name__ == "__main__":
    store_data_s3()
    query_with_athena()
    print("Data lake setup complete.")
