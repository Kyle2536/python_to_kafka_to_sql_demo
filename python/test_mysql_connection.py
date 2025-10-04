import mysql.connector

try:
    conn = mysql.connector.connect(
        host="richardsonsql.mysql.database.azure.com",   # Keep this if MySQL is on the same machine
        port=3306,          # Default MySQL port
        user="utdsql",        # Replace with your MySQL username
        password="Capstone2025!",  # Replace with your MySQL password
        database="kafka" # Replace with your database name
    )
    print("Connected to MySQL successfully!")
    conn.close()
except mysql.connector.Error as e:
    print(f"Error: {e}")
