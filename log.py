import mysql.connector
from datetime import datetime

# Configure your database connection
db_config = {
    'user': 'root',
    'password': 'arnavmysql',
    'host': 'localhost',
    'database': 'arnav'
}

def log_message(message):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert the message and current timestamp
        query = "INSERT INTO logs (message) VALUES (%s)"
        cursor.execute(query, (message,))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

