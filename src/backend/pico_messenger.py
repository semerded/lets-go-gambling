from bleak import BleakClient
import asyncio
import paho.mqtt.client as mqtt
import json

# --- BLE Configuration ---
PICO_MAC = "D8:3A:DD:58:3D:6A"  # Replace with your Pico's MAC
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Notify (from Pico)
CHAR_RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Write (to Pico)

# --- MQTT Configuration ---
mqtt_client = mqtt.Client()
mqtt_client.connect("broker.hivemq.com")

class PicoConnection:
    def __init__(self):
        self.client = None
        self.connected = False

    async def connect(self):
        while True:
            try:
                print("Connecting to Pico...")
                self.client = BleakClient(PICO_MAC)
                await self.client.connect(timeout=15.0)
                
                # Verify services
                services = await self.client.get_services()
                print("Discovered services:")
                for service in services:
                    print(f"- Service: {service.uuid}")
                    for char in service.characteristics:
                        print(f"  - Characteristic: {char.uuid}")
                
                if not any(char.uuid == CHAR_TX_UUID for service in services for char in service.characteristics):
                    raise Exception("TX characteristic not found")
                
                self.connected = True
                print("Connected to Pico!")
                
                # Start notifications
                await self.client.start_notify(CHAR_TX_UUID, self.handle_notification)
                
                # Main connection loop
                while self.connected:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                print(f"Connection error: {e}")
                self.connected = False
                if self.client:
                    try:
                        await self.client.disconnect()
                    except:
                        pass
                await asyncio.sleep(5)

    def handle_notification(self, sender, data):
        try:
            button_states = data.decode().split(',')
            print(f"Received button states: {button_states}")
            
            # Process game logic
            game_state = {"status": "OK", "buttons": button_states}
            
            # Send ACK back via BLE
            asyncio.create_task(self.send_ack(game_state))
            
            # Also send to MQTT if needed
            mqtt_client.publish("pico/buttons", json.dumps(button_states))
            
        except Exception as e:
            print(f"Notification error: {e}")

    async def send_ack(self, data):
        try:
            if self.connected and self.client:
                await self.client.write_gatt_char(CHAR_RX_UUID, json.dumps(data).encode())
                print("Sent ACK to Pico")
        except Exception as e:
            print(f"Failed to send ACK: {e}")
            self.connected = False

async def main():
    connection = PicoConnection()
    await connection.connect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")