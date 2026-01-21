import psycopg2
import csv
from api_request import fetch_data
from io import StringIO
from datetime import datetime
import os

def connect_to_database():
    # Simulate a database connection
    print("Connecting to the PostgreSQL database.")
    try:
        connection = psycopg2.connect(
            host=os.getenv("APP_DB_HOST", "db"),
            port=int(os.getenv("APP_DB_PORT", "5432")),
            dbname=os.getenv("APP_DB_NAME"),       # required
            user=os.getenv("APP_DB_USER"),         # required
            password=os.getenv("APP_DB_PASSWORD") # required
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return

def create_table(connection):
    print("Preparing Raw Landing Table.")
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE SCHEMA IF NOT EXISTS dev;
        CREATE TABLE IF NOT EXISTS dev.raw_earthquake_data (
            id TEXT PRIMARY KEY,  -- USGS provides a unique ID string
            magnitude FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            depth FLOAT,
            location TEXT,
            time TEXT             -- Store as TEXT initially, dbt will cast it
        );
        TRUNCATE TABLE dev.raw_earthquake_data; -- Keeps the Bronze layer fresh
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error preparing table: {e}")
        raise
# def create_table(connection):
#     print("Creating table if not exists.")
#     try:
#         cursor = connection.cursor()
#         create_table_query = """
#         CREATE SCHEMA IF NOT EXISTS dev;
#         CREATE TABLE IF NOT EXISTS dev.raw_earthquake_data (
#             id SERIAL PRIMARY KEY,
#             magnitude FLOAT,
#             location TEXT,
#             time TIMESTAMPTZ
#         );
#         """
#         cursor.execute(create_table_query)
#         connection.commit()
#         print("Table created successfully.")
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error creating table: {e}")
#         raise

# def insert_records(connection, records):
#     print("Inserting records into the database.")
#     try:
#         cursor = connection.cursor()
#         insert_query = """
#         INSERT INTO dev.raw_earthquake_data (magnitude, location, time)
#         VALUES (%s, %s, %s);
#         """
#         for record in records:
#             cursor.execute(insert_query, (record['magnitude'], record['location'], record['time']))
#             connection.commit()
#         print("Records inserted successfully.")
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error inserting records: {e}")
#         raise

def insert_records(connection, records):
    try:
        cursor = connection.cursor()
        # Use ON CONFLICT to avoid errors if the same ID is ingested twice
        insert_query = """
        INSERT INTO dev.raw_earthquake_data (id, magnitude, latitude, longitude, depth, location, time)
        VALUES (%(id)s, %(magnitude)s, %(latitude)s, %(longitude)s, %(depth)s, %(location)s, %(time)s)
        ON CONFLICT (id) DO NOTHING;
        """
        cursor.executemany(insert_query, records)
        connection.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error inserting: {e}")
        raise

# def parse_csv(csv_text):
#     """
#     Parses USGS-style CSV:
#     time,latitude,longitude,depth,mag,...,place,...
#     """
#     reader = csv.DictReader(StringIO(csv_text))
#     records = []

#     for row in reader:
#         records.append({
#             "magnitude": float(row["mag"]),
#             "location": row["place"],
#             "time": row["time"]
#         })

#     return records
def parse_csv(csv_text):
    reader = csv.DictReader(StringIO(csv_text))
    records = []
    for row in reader:
        records.append({
            "id": row["id"],
            "magnitude": float(row["mag"]) if row["mag"] else None,
            "latitude": float(row["latitude"]) if row["latitude"] else None,
            "longitude": float(row["longitude"]) if row["longitude"] else None,
            "depth": float(row["depth"]) if row["depth"] else None,
            "location": row["place"],
            "time": row["time"]
        })
    return records

def main():
    try:
        data = fetch_data()
        connection = connect_to_database()
        create_table(connection)
        records = parse_csv(data)
        insert_records(connection, records)
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        if "connection" in locals():
            connection.close()
            print("Database connection closed.")