from json_loader import JsonLoader
from db_loader import PostgresLoader
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('.env')  # Load env parameters
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

def load_data(json_file_path, fields, schema, table):
    try:
        # Create instances of JsonLoader and PostgresLoader
        json_loader = JsonLoader(json_file_path)
        db_loader = PostgresLoader(db_name, db_user, db_password, db_host, db_port)

        # Load data from JSON file and insert into database
        data_dict = json_loader.load(fields)
        db_loader.load_dict(schema, table, data_dict)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Define parameters
    json_file_path = 'data/starlink_historical_data.json'
    fields = ['spaceTrack.CREATION_DATE', 'longitude', 'latitude', 'id']
    schema = 'spacetrack'
    table = 'position'

    # Call load_data function
    load_data(json_file_path, fields, schema, table)