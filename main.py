from fastapi import FastAPI
import sqlite3
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn

app = FastAPI()
mqtt_config = MQTTConfig(host="172.16.5.101", port=1883)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

#Publish la couleur sur l'ESP32 en dur
@app.get("/test")
async def func():
    mqtt.publish("Enzo/led/couleur", "255 0 0 test") #publishing mqtt topic

    return {"result": True,"message":"Published" }

#Récupérer le message
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("Enzo/led/message")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.subscribe("Enzo/led/message")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())

#Récupérer la taille du panneau
@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("Enzo/led/panneau")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.subscribe("Enzo/led/panneau")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())



