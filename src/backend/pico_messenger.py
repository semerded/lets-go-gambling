import paho.mqtt.client as mqtt
import json

# MQTT Setup
def on_connect(client, userdata, flags, rc):
    print("Connected to HiveMQ!")
    client.subscribe("pico/gpio_data")  # Listen to Pico

def on_message(client, userdata, msg):
    if msg.topic == "pico/gpio_data":
        gpio_val = msg.payload.decode()
        print("Pico GPIO:", gpio_val)
        
        # Process data (e.g., update balance)
        balance = 100  # Replace with your logic
        stats = {"balance": balance, "status": "OK"}
        
        # Send ACK + stats back to Pico
        client.publish("rpi/acks", "ACK")
        client.publish("rpi/stats", json.dumps(stats))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883)
client.loop_forever()