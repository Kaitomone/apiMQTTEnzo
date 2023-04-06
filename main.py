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
    mqtt.publish("enzo/led/couleur", "255 0 0 test") #publishing mqtt topic

    return {"result": True,"message":"Published" }



