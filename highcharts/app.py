from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL connection (Azure)
db_config = {
    "host": "richardsonsql.mysql.database.azure.com",
    "port": 3306,
    "user": "utdsql",
    "password": "Capstone2025!",
    "database": "kafka"
}

@app.route('/data')
def get_data():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT timestamp, peakspeed, direction, vehiclecount
        FROM raw_data_kafka
        ORDER BY id DESC LIMIT 100
    """)
    rows = cursor.fetchall()
    db.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
