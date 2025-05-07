from flask import Flask
from flask_mqtt import Mqtt
import jsonify
import psycopg2

app = Flask(__name__)

# MQTT connection
app.config['MQTT_BROKER_URL'] = '10.8.21.61'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to mqtt")
        mqtt_client.subscribe("/counter")
    else:
        print("Not connected to mqtt. Code:", rc)

@mqtt_client.on_message()
def handle_msg(client, userdata, msg):
    payload = msg.payload.decode()
    print(payload)
    print(msg)

@app.route("/mqtt_couter", methods=['POST'])
def publish_mqtt_counter():
    request_data = request_data.get_json()
    result = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return jsonify({'code':result[0]})

# Database connection
conn = psycopg2.connect(database="postgres", user="mosquitto", 
                        password="2024.PERTE", host="localhost", port="5432") 

@app.route("/")
def inidex():
    cursor = conn.cursor()
    
    thing_id='b6899396-139f-11f0-9ef6-8f16bab1c04c'
    cursor.execute('''SELECT phenomenonTime FROM Datastream where name=%s''', thing_id)
    times = cursor.fetchall()
    print("Times:", times)

    data=[]
    for t in times:
        cursor.execute('''SELECT parameters FROM Observation where phenomenonTime=%f''', t)
        data.append(cursor.fetchall())

    cursor.close()
    return Flask.render_template('index.html', data=data)

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=5000)