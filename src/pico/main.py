# main.py
import ubluetooth, network, ujson, umqtt, machine, time, binascii
from wlan_conf import WIFI1, WIFI2
from machine import PWM, Pin
from time import sleep
from lcd_i2c import Lcd
from mqtt_creds import *

PWM_SCALE_FACTOR = 65535 / 99

# Hardware Setup
pwm_hit = PWM(Pin(17))
pwm_hit.freq(1000)
pwm_stand = PWM(Pin(16))
pwm_stand.freq(1000)

# --- Global State ---
ble = None
client = None
wlan = None
char_handle = None
ble_connected = False
conn_handle = None
last_reconnect_time = 0
RECONNECT_DELAY = 3000  # 3 seconds
MQTT_INTERVAL = 15000   # 15s (ThingSpeak minimum)

# --- MQTT Configuration ---
def mqtt_callback(topic, msg):
    print(f"MQTT RX: {topic.decode()} = {msg.decode()}")

def initialize_mqtt():
    global client
    try:
        client = umqtt.MQTTClient(
            client_id=CLIENT_ID,
            server=MQTT_SERVER,
            user=UNAME,
            password=PASSWD,
            port=1883,
            keepalive=60
        )
        client.set_callback(mqtt_callback)
        client.connect()
        print("MQTT Connected!")
        return True
    except Exception as e:
        print("MQTT Init Error:", e)
        return False

def publish_status():
    if client and wlan.isconnected():
        try:
            status = 1 if ble_connected else 0
            payload = f"field1={status}"
            client.publish("channels/" + CHANNEL + "/publish", payload)
            print(f"Published BLE Status: {status}")
        except Exception as e:
            print("MQTT Publish Error:", e)
            client.disconnect()
            initialize_mqtt()

# --- BLE Configuration ---
SERVICE_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
CHAR_TX_UUID = ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
CHAR_RX_UUID = ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
game_state = "i"
def initialize_ble():
    global ble, char_handle, ble_connected, conn_handle
    try:
        if ble:
            ble.active(False)
            time.sleep_ms(500)
            
        ble = ubluetooth.BLE()
        ble.active(True)
        ble.config(gap_name="picobello")
        ble.irq(ble_irq_handler)
        
        services = ble.gatts_register_services((
            (SERVICE_UUID, (
                (CHAR_TX_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY),
                (CHAR_RX_UUID, ubluetooth.FLAG_WRITE),
            ),),
        ))
        char_handle = services[0][0]
        
        adv_payload = bytearray()
        adv_payload += bytearray([0x02, 0x01, 0x06])
        adv_payload += bytearray([len("picobello") + 1, 0x09]) + "picobello".encode()
        adv_payload += bytearray([0x03, 0x02, 0x01, 0x00])
        
        ble.gap_advertise(100, adv_payload)
        ble_connected = False
        conn_handle = None
        publish_status()  # Initial status update
        return True
    except Exception as e:
        print("BLE Init Error:", e)
        return False

def ble_irq_handler(event, data):
    global ble_connected, conn_handle, last_reconnect_time, game_state
    try:
        if event == 1:  # Connected
            conn_handle, _, _ = data
            ble_connected = True
            publish_status()
            
        elif event == 2:  # Disconnected
            ble_connected = False
            conn_handle = None
            last_reconnect_time = time.ticks_ms()
            publish_status()
            
        elif event == 3:  # GATT Write
            conn_handle, attr_handle = data
            received = ble.gatts_read(attr_handle).decode()

            try:
                print(int(received[:3]), received[3:4], int(received[4:6]), int(received[6:8]), received[8:].split("$"))
            except:
                print(received)
            
            
            pwm1_value = int(round(int(received[4:6]) * PWM_SCALE_FACTOR))
            pwm_hit.duty_u16(min(65535, max(0, pwm1_value)))

            pwm2_value = int(round(int(received[6:8]) * PWM_SCALE_FACTOR))
            pwm_stand.duty_u16(min(65535, max(0, pwm2_value)))
            
            state = received[3:4]
            message = received[8:].split("$")
            print(f"pwm1: {pwm1_value}, pwm2: {pwm2_value}, state: {state}, message: {message}")
            lcd.lcd_clear()
            game_state = state
            if state == "i":
                lcd.lcd_display_string("play virtual", 1, 0)
                lcd.lcd_display_string("blackjack free!", 2, 0)
            elif state == "s":     
                lcd.lcd_display_string("balance:"+ message[0], 1, 0)
                lcd.lcd_display_string("betting:"+ message[1], 2, 0)
            elif state == "b":
                lcd.lcd_display_string("balance:"+ message[0], 1, 0)
                lcd.lcd_display_string("bet:"+ message[1], 2, 0)
            elif state == "r":
                lcd.lcd_display_string("diff:"+ message[0], 1, 0)
                lcd.lcd_display_string("balance:"+ message[1], 2, 0)
            
    except Exception as e:
        print("IRQ Handler Error:", e)

# --- WiFi Initialization ---
def initialize_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    for net in [WIFI1, WIFI2]:
        try:
            wlan.connect(net[0], net[1])
            for _ in range(10):
                if wlan.isconnected():
                    print("WiFi Connected! IP:", wlan.ifconfig()[0])
                    return True
                time.sleep(1)
        except Exception as e:
            print("WiFi Error:", e)
    return False

# --- Main Initialization ---
lcd = Lcd(12, 13)
lcd.lcd_display_string("Initializing...")

print("Starting BLE...")
if not initialize_ble():
    machine.reset()

print("Starting WiFi...")
initialize_wifi()  # Optional for MQTT

print("Starting MQTT...")
initialize_mqtt()

# --- Main Loop ---
last_mqtt_time = time.ticks_ms()
last_ble_check = time.ticks_ms()

class PwmRunner:
    def __init__(self, start_value = 0):
        self.min = 0
        self.max = 99
        self.value = start_value
        self.running_up = True if start_value == self.max else False
        
    def update(self):
        if self.running_up:
            self.value += 1
            if self.value == self.max:
                self.running_up = False
        else:
            self.value -= 1
            if self.value == self.min:
                self.running_up = True
                
pwm_runner1 = PwmRunner(0)
pwm_runner2 = PwmRunner(99)

while True:
    try:
        current_time = time.ticks_ms()
        
        # BLE Reconnection
        if not ble_connected and time.ticks_diff(current_time, last_reconnect_time) > RECONNECT_DELAY:
            initialize_ble()
            last_reconnect_time = current_time
            
        # Periodic MQTT Updates
        if time.ticks_diff(current_time, last_mqtt_time) >= MQTT_INTERVAL:
            publish_status()
            last_mqtt_time = current_time
            
        # Existing Button Handling
        if ble_connected:
            buttons = [str(machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN).value()) for pin in range(1, 7)]
            try:
                ble.gatts_write(char_handle, ",".join(buttons).encode())
                ble.gatts_notify(conn_handle, char_handle)
            except Exception as e:
                print("BLE Notify Error:", e)
                ble_connected = False
                
        # MQTT Message Processing
        if client:
            client.check_msg()
            
        if game_state == "i":
            print('pwm runner')
            pwm_runner1.update()
            pwm_runner2.update()
            pwm1_value = int(round(pwm_runner1.value * PWM_SCALE_FACTOR))
            pwm_hit.duty_u16(min(65535, max(0, pwm1_value)))

            pwm2_value = int(round(pwm_runner2.value * PWM_SCALE_FACTOR))
            pwm_stand.duty_u16(min(65535, max(0, pwm2_value)))
            
        time.sleep_ms(50)
        
    except Exception as e:
        print("Main Loop Error:", e)
        machine.reset()