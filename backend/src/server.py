from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os

host = os.environ.get("DATABASE_CONTAINER_NAME")
port = os.environ.get("DATABASE_CONTAINER_PORT")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("MYSQL_ROOT_PASSWORD")
database = os.environ.get('DATABASE_NAME')

if all((host, port, user, password, database)):
    db = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = db.cursor()
else:
    cursor = None

app = Flask(__name__)
CORS(app)

@app.route("/validate-server-runtime", methods=["GET"])
def validate_server_runtime():
    return jsonify("Hello World!"), 200

@app.route("/validate-db-connection", methods=["GET"])
def validate_db_connection():
    cursor.execute("SHOW TABLES")
    return jsonify(cursor.fetchall()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("BACKEND_CONTAINER_PORT"))