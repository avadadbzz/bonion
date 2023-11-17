from flask import Flask, jsonify, request
from db_loader import PostgresLoader
from datetime import datetime
from haversine import haversine
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()  # take environment variables from .env.
secret_key = os.getenv('SECRET_KEY')
database_url = os.getenv('DATABASE_URL')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_port = os.getenv('DB_PORT')

# Create a connection pool
conn_pool = PostgresLoader(db_name, db_user, db_password, db_host, db_port)

@app.route('/test', methods=['GET'])
def test():
    return 'API is running'

@app.route('/v1/lastposition', methods=['GET'])
def getid():
    #get args
    id = request.args.get('id', type = str)
    date = "'" + request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'), type=str) + "'"
    #conn and query db
    query = """SELECT id, latitude, longitude, creation_date
                FROM (
                  SELECT id, latitude, longitude, creation_date,
                         rank () OVER (PARTITION BY id ORDER BY creation_date DESC) as rank
                  FROM spacetrack.position
                  WHERE id = %s and creation_date <= %s
                ) t
                WHERE t.rank = 1"""
    params = (id, date)
    x = conn_pool.get(query, params, dict_cursor=True)
    return jsonify(x)

@app.route('/v1/nearest', methods=['GET'])
def find_nearest():
    lat  = request.args.get('lat', type = float )
    long = request.args.get('long', type= float)
    date = "'" + request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'), type=str) + "'"
    input_position = (lat, long)
    #conn and query db
    query = """SELECT latitude, longitude, id, creation_date
                FROM (
                  SELECT id, latitude, longitude, creation_date,
                         rank () OVER (PARTITION BY id ORDER BY creation_date DESC) as rank
                  FROM spacetrack.position
                  WHERE creation_date <= %s and latitude is not null and longitude is not null
                ) t
                WHERE t.rank = 1 """
    params = (date,)
    result = conn_pool.get(query, params)
    positions = [tuple(lst) for lst in result["data"]]

    nearest_position = None
    smallest_distance = None

    for position in positions:
        position = position
        distance = haversine(input_position, (position[0], position[1]))
        if smallest_distance is None or distance < smallest_distance:
            smallest_distance = distance
            nearest_position = position
    return (f"id: {nearest_position[2]}, nearest_position: {nearest_position[0]}, smallest_distance: {smallest_distance}, date: {nearest_position[3]}")

app.run(port=5000, host='0.0.0.0', debug=True)