# rpi_listener.py
from bleak import BleakClient
import paho.mqtt.client as mqtt
import asyncio

# --- BLE Config ---
PICO_MAC = "6A:3D:58:DD:3A:D8"  # Replace with Pico's BLE MAC
CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"

# --- MQTT Config ---
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.com")

def on_ble_notify(sender, data):
    buttons = data.decode().split(',')
    print(f"Buttons: {buttons}")
    
    # Process game logic here
    game_state = {"balance": 100, "last_bet": 5}
    
    # Send ACK + data back
    asyncio.run(send_ble_ack(game_state))

async def send_ble_ack(data):
    async with BleakClient(PICO_MAC) as client:
        await client.write_gatt_char(CHAR_UUID, str(data).encode())

# --- Main ---
async def run():
    client = BleakClient(PICO_MAC)
    await client.connect()
    await client.start_notify(CHAR_UUID, on_ble_notify)
    while True:
        await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(run())