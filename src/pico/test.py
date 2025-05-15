from umqtt.simple import MQTTClient
import network
import time
import machine
from wlan_conf import WIFI1, WIFI2

# Wi-Fi Setup (same as before)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(*WIFI1) or wlan.connect(*WIFI2)

# MQTT Setup
client = MQTTClient("pico", "broker.hivemq.com")
ACK_TIMEOUT = 10  # Seconds to wait for RPi response
last_ack_time = time.time()

# Callback for RPi messages
def on_message(topic, msg):
    global last_ack_time
    if topic == b"rpi/acks":
        print("RPi ACK:", msg.decode())
        last_ack_time = time.time()  # Reset timeout
    elif topic == b"rpi/stats":
        print("RPi Stats:", msg.decode())
        # Forward stats to dashboard
        client.publish("dashboard/stats", msg)

client.set_callback(on_message)
client.connect()
client.subscribe("rpi/acks")
client.subscribe("rpi/stats")

# Main loop
while True:
    # 1. Read GPIO (example: button press)
    gpio_data = str(machine.Pin(1, machine.Pin.IN).value()) 
    client.publish("pico/gpio_data", gpio_data)

    # 2. Check for RPi response (timeout logic)
    client.check_msg()
    if time.time() - last_ack_time > ACK_TIMEOUT:
        client.publish("dashboard/error", "RPi not responding!")
        last_ack_time = time.time()  # Prevent spamming

    time.sleep(1)