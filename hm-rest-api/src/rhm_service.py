import os
import mysql.connector
from rhm_logging import *

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_database = os.environ.get('DB_DATABASE')


db_config = {
    'user': db_user,
    'password': db_password,
    'host': db_host,
    'database': db_database,
}

def save_new(temperature, humidity):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO weather_data (temperature, humidity) VALUES (%s, %s)"
        cursor.execute(query, (temperature, humidity))
        conn.commit()
        INFO("Added new entry to the database!")
    except mysql.connector.Error as err:
        ERROR(f"Database connection exception occurred: {err}")
    finally:
        conn.close()

def get_all():
    json_result = {}
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the row with the last inserted ID
        cursor.execute("SELECT * FROM weather_data")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        json_result = result

    except mysql.connector.Error as err:
        ERROR(f"Database connection exception occurred: {err}")

    finally:
        conn.close()

    return json_result

def get_last():
    data = {}
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Get the last inserted ID
        cursor.execute("SELECT MAX(ID) FROM weather_data")
        last_id = cursor.fetchone()[0]

        # Fetch the row with the last inserted ID
        cursor.execute("SELECT * FROM weather_data WHERE id = %s", (last_id,))
        last_row = cursor.fetchone()
        data = {
            "id": last_row[0],
            "timestamp": last_row[1],
            "temperature": last_row[2],
            "humidity": last_row[3]
        }

    except mysql.connector.Error as err:
        ERROR(f"Database connection exception occurred: {err}")

    finally:
        conn.close()

    return data

