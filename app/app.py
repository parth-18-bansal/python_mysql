from flask import Flask, jsonify
import mysql.connector
import os
from prometheus_client import start_http_server, Counter
# # #import logging

app = Flask(__name__)

# #database connection
DB_HOST = os.getenv("DB_HOST","localhost")
DB_USER = os.getenv("DB_USER","root")
DB_PASSWORD = os.getenv("DB_PASSWORD","root")
DB_NAME = os.getenv("DB_NAME","app")

def connect_to_db():
    connect = mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
    return connect

# # Create a counter metric to track requests
REQUESTS = Counter('http_requests_total', 'Total number of HTTP requests')

# # logging
# #logging.basicConfig(filename='app.log',level=logging.INFO)

@app.route('/')
def home():
    REQUESTS.inc()
    
    app.logger.info("Home Page")

    connect = connect_to_db()
    cursor = connect.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS messages (id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255))")
    cursor.execute("INSERT INTO messages (text) VALUES ('Hello from Local MySQL!')")

    connect.commit()

    cursor.execute("SELECT * FROM messages")
    messages = cursor.fetchall()

    cursor.close()
    connect.close()

    return jsonify({"messages": messages})

if __name__ == "__main__":
    start_http_server(8000)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

# when we use the debug = True, the app will reload itself when we make changes to the code. so if we use the debug = True and not
# not add use_reloader = False, the app will reload itself and the prometheus server will start again and again.
# first time it get bind with 8000 then debug also try to bind the prometheus server with 8000 but it is already binded so it will
# throw an error. so to avoid this we use use_reloader = False. so that prometheus server will not start again and again.
# or we will remove the debug = True. so that the app will not reload itself. so the prometheus server will not start again and again.


# to check the process which is using a particular port. = sudo lsof -i :9323

# to kill the process which is using a particular port. = sudo kill -9 <PID>


