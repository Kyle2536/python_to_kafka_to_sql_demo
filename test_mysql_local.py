import mysql.connector

try:
    db = mysql.connector.connect(
        host="richardsonsql.mysql.database.azure.com",
        port=3306,
        user="utdsql",
        password="Capstone2536!",
        database="kafka"
    )
    print("✅ Connected successfully:", db.get_server_info())

    cursor = db.cursor()
    cursor.execute("SHOW TABLES;")
    print("📋 Tables:", cursor.fetchall())

    db.close()

except Exception as e:
    print("❌ Connection failed:", e)
