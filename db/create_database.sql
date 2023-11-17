CREATE DATABASE spacetrack;

\c spacetrack;

CREATE SCHEMA spacetrack;

CREATE TABLE spacetrack.position (
    "id" VARCHAR(30) NOT NULL,
    "creation_date" TIMESTAMP NOT NULL,
    "longitude" INT NOT NULL,
    "latitude" NUMERIC
);