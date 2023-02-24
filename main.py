from fastapi import FastAPI
import sqlite3
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn

app = FastAPI()
mqtt_config = MQTTConfig(host="172.16.5.101", port=1883)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("enzo/led/couleur/R") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.subscribe("enzo/led/couleur/R")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("enzo/led/couleur/G")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.subscribe("enzo/led/couleur/G")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("enzo/led/couleur/B")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.subscribe("enzo/led/couleur/B")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode())
    
@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/test")
async def func():
    mqtt.publish("enzo/led/couleur", "127 0 122") #publishing mqtt topic

    return {"result": True,"message":"Published" }