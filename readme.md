# Starlink Position API
This API provides information about the last known position of Starlink satellites and the nearest satellite to a given location.

## Setup
Clone the repository and run `docker-compose up -d` this gonna execute the follow steps:
  * Start the database and create the schema and table
  * Run a python script to read and extract the important fields from json file and insert into db
  * Start the API

## Endpoints

#### The API runs over localhost:8080

### /test
- Method: GET
- Description: Tests if the API is running.
- Response: A string saying "API is running".
### /v1/lastposition
- Method: GET
- Description: Returns the last known position of a specific Starlink satellite.
- Parameters:
  - id (required): The ID of the satellite.
  - date (optional): The date to get the position for. Defaults to the current date.
- Response: A JSON object containing the ID, latitude, longitude, and creation date of the last known position of the satellite.
### /v1/nearest
- Method: GET
- Description: Returns the nearest Starlink satellite to a given location.
- Parameters:
  - lat (required): The latitude of the location.
  - long (required): The longitude of the location.
  - date (optional): The date to find the nearest satellite for. Defaults to the current date.
- Response: A string containing the ID, nearest position, smallest distance, and date of the nearest satellite.

### Examples
```
localhost:8080/v1/nearest?lat=45.7597&long=4.8422
localhost:8080/v1/nearest?lat=45.7597&long=4.8422&date=2021-10-01
localhost:8080/v1/lastposition?id=5eed7716096e5900069857e3
localhost:8080/v1/lastposition?id=5eed7716096e5900069857e3&date=2021-01-27
```

## SQL Query
SQL used to query the database and get the last satellite position
### Get last position, given id and time:
```
SELECT id, latitude, longitude, creation_date
                FROM (
                  SELECT id, latitude, longitude, creation_date,
                         rank () OVER (PARTITION BY id ORDER BY creation_date DESC) as rank
                  FROM spacetrack.position
                  WHERE id = %s and creation_date <= %s
                ) t
                WHERE t.rank = 1
```
