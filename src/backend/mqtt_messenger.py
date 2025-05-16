import paho.mqtt.client as mqtt
import time
from src.database.creds import *
from src import data
from threading import Thread

# ThingSpeak MQTT Settings
MQTT_HOST = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_TOPIC_PUBLISH = "channels/" + CHANNEL + "/publish"  

class MqttMessenger:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)
        self.client.username_pw_set(UNAME, PASSWD)
        self.client.on_connect = MqttMessenger.on_connect
        self.client.on_disconnect = MqttMessenger.on_disconnect

        # Connect to the broker
        self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
        self.client.loop_start()  # Start network loop (non-blocking)
        
        self.games_won = 0
        self.games_lost = 0
        self.money_won = 0
        self.money_lost = 0
        self.blackjack = 0
        self.games_played = 0
        self.payload =""
        
        
    # Callback when connecting to the broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Connection failed with code {rc}. Retrying...")

    # Callback for disconnection
    def on_disconnect(client, userdata, rc):
        print(f"Disconnected! Reason: {rc}")
        time.sleep(5)
        client.reconnect()  # Auto-reconnect
        
    def start_thread(self):
        thread = Thread(target=self._loop)
        thread.daemon = True
        thread.start()

    # Initialize MQTT client
    def update_money_won(self, money_won):
        self.money_won += money_won
        
    def update_money_lost(self, money_lost):
        self.money_lost += money_lost
        
    def update_blackjack_count(self):
        self.blackjack += 1
    
    def update_games_played(self):
        self.games_played += 1
    
    def update_games_won(self):
        self.games_won += 1
    
    def update_games_lost(self):
        self.games_lost += 1
        
    def get_highest_balance(self):
        return str(max(player["balance"] for player in data.player_data.values()))
   
    def _loop(self):
        while data.running:
            highest_balance = self.get_highest_balance()
            
            self.payload = "field6=" + highest_balance
            self.payload += "&field7=" + str(self.games_won)
            self.payload += "&field8=" + str(self.games_lost)
            self.payload += "&field5=" + str(self.games_played)
            self.payload += "&field4=" + str(self.blackjack)
            self.payload += "&field3=" + str(self.money_lost)
            self.payload += "&field2=" + str(self.money_won)
            
            self.client.publish(MQTT_TOPIC_PUBLISH, self.payload)
            print(f"Published: {self.payload}")
            self.payload = ""
            self.games_won = 0
            self.games_lost = 0
            self.money_won = 0
            self.money_lost = 0
            self.blackjack = 0
            self.games_played = 0
            time.sleep(15) 
        self.client.disconnect()
        print("MQTT Disconnected.")