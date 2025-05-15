from bleak import BleakClient
from threading import Thread
import asyncio
import paho.mqtt.client as mqtt
import json
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- BLE Configuration ---
PICO_MAC = "D8:3A:DD:58:3D:6A"  # Replace with your Pico's MAC
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHAR_TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"  # Notify (from Pico)
CHAR_RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Write (to Pico)

# --- MQTT Configuration ---
# mqtt_client = mqtt.Client()
# mqtt_client.connect("broker.hivemq.com")

class PicoConnection:
    def __init__(self):
        self.client = None
        self.connected = False

    async def connect(self):
        while True:
            try:
                logger.info("Attempting to connect to Pico...")
                self.client = BleakClient(PICO_MAC, mtu=40)
                await self.client.connect(timeout=15.0)
                
                # Verify services using the preferred .services property
                if not self.client.services:
                    logger.error("No services discovered")
                    raise Exception("No services discovered")
                
                logger.info("Discovered services:")
                found_tx = False
                for service in self.client.services:
                    logger.info(f"- Service: {service.uuid}")
                    for char in service.characteristics:
                        logger.info(f"  - Characteristic: {char.uuid}")
                        if char.uuid.lower() == CHAR_TX_UUID.lower():
                            found_tx = True
                
                if not found_tx:
                    logger.error(f"TX characteristic {CHAR_TX_UUID} not found")
                    raise Exception("TX characteristic not found")
                
                self.connected = True
                logger.info("Successfully connected to Pico!")
                
                # Start notifications
                await self.client.start_notify(CHAR_TX_UUID, self.handle_notification)
                logger.info(f"Subscribed to notifications on {CHAR_TX_UUID}")
                
                # Main connection loop
                while self.connected:
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Connection error: {e}")
                self.connected = False
                if self.client:
                    try:
                        await self.client.disconnect()
                    except Exception as e:
                        logger.error(f"Disconnect error: {e}")
                await asyncio.sleep(5)

    def handle_notification(self, sender, data):
        try:
            button_states = data.decode().split(',')
            logger.info(f"Received button states: {button_states}")
            
            # Process game logic
            game_state = {"status": "OK", "buttons": button_states}
            
            # Send ACK back via BLE
            asyncio.create_task(self.send_ack(game_state))
            
            # Also send to MQTT if needed
            # mqtt_client.publish("pico/buttons", json.dumps(button_states))
            
        except Exception as e:
            logger.error(f"Notification error: {e}")

    async def send_ack(self, data):
        try:
            if self.connected and self.client:
                await self.client.write_gatt_char(CHAR_RX_UUID, "hello world i'm steve from minecraft pico world lol send nudes".encode())
                logger.info("Sent ACK to Pico")
        except Exception as e:
            logger.error(f"Failed to send ACK: {e}")
            self.connected = False

def pico_messenger():
    connection = PicoConnection()
    asyncio.run(connection.connect())
Thread(target=pico_messenger, daemon=True).start()

# if __name__ == "__main__":
#     try:
        
#     except KeyboardInterrupt:
#         logger.info("Shutting down...")
#     except Exception as e:
#         logger.error(f"Fatal error: {e}")