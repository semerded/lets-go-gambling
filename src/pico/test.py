# main.py
import ubluetooth, network, ujson, umqtt, machine, time, binascii
from wlan_conf import WIFI1, WIFI2
from machine import  PWM, Pin
from time import sleep
from lcd_i2c import Lcd

PWM_SCALE_FACTOR = 65535 / 99

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

# --- BLE Configuration ---
SERVICE_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
CHAR_TX_UUID = ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # Notify
CHAR_RX_UUID = ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  # Write

def initialize_ble():
    global ble, char_handle, ble_connected, conn_handle
    
    try:
        # Clean up previous connection
        if ble:
            try:
                ble.active(False)
            except:
                pass
            time.sleep_ms(500)
        
        # Initialize fresh BLE instance
        ble = ubluetooth.BLE()
        ble.active(True)
        ble.config(gap_name="picobello")
        ble.irq(ble_irq_handler)
        
        # Register service
        ble_service = (
            SERVICE_UUID,
            [
                (CHAR_TX_UUID, ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY),
                (CHAR_RX_UUID, ubluetooth.FLAG_WRITE),
            ],
        )
        
        services = ble.gatts_register_services((ble_service,))
        char_handle = services[0][0]  # TX characteristic
        rx_handle = services[0][1]    # RX characteristic
        
        # Setup advertising payload
        adv_payload = bytearray()
        adv_payload += bytearray([0x02, 0x01, 0x06])  # Flags
        adv_payload += bytearray([len("picobello") + 1, 0x09]) + "picobello".encode()  # Complete name
        adv_payload += bytearray([0x03, 0x02, 0x01, 0x00])  # Incomplete 16-bit service UUIDs
        
        ble.gap_advertise(100, adv_payload)
        
        ble_connected = False
        conn_handle = None
        print("BLE initialized and advertising")
        return True
    except Exception as e:
        print("BLE Init Error:", e)
        return False

def ble_irq_handler(event, data):
    global ble_connected, conn_handle, last_reconnect_time
    
    try:
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            ble_connected = True
            print("BLE Connected")
            
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            ble_connected = False
            conn_handle = None
            print("BLE Disconnected - restarting advertising")
            last_reconnect_time = time.ticks_ms()
            
        elif event == 3:  # _IRQ_GATTS_WRITE
            conn_handle, attr_handle = data
            received = ble.gatts_read(attr_handle)
            received = received.decode()
            
            pwm1_value = int(round(received[:2] * PWM_SCALE_FACTOR))
            pwm_hit.duty_u16(min(65535, max(0, pwm1_value)))

            
            pwm2_value = int(round(received[2:5] * PWM_SCALE_FACTOR))
            pwm_stand.duty_u16(min(65535, max(0, pwm2_value)))
            state = int(received[5:6])
            message = received[6:].split("$")
            print(f"pwm1: {pwm1_value}, pwm2: {pwm2_value}, state: {state}, message: {message}")
            
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
        machine.reset()  # Hard reset if we get stuck
        
def initialize_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    networks = [WIFI1, WIFI2]
    for net in networks:
        try:
            print("Connecting to", net[0])
            wlan.connect(net[0], net[1])
            
            for _ in range(10):
                if wlan.isconnected():
                    print("Connected! IP:", wlan.ifconfig()[0])
                    return True
                time.sleep(1)
                
        except Exception as e:
            print("WiFi Error:", e)
    
    print("Failed to connect to WiFi")
    return False

def initialize_mqtt():
    global client
    try:
        client = umqtt.MQTTClient("pico", "broker.hivemq.com", keepalive=30)
        client.connect()
        return True
    except Exception as e:
        print("MQTT Init Error:", e)
        return False

# --- Initialization ---
print("Initializing BLE...")
if not initialize_ble():
    print("Failed to initialize BLE - retrying...")
    machine.reset()  # Hard reset if BLE fails to initialize

print("Initializing WiFi...")
if not initialize_wifi():
    print("WiFi initialization failed - continuing without WiFi")

print("Initializing MQTT...")
initialize_mqtt() # Will try to reconnect later if fails

# --- MAC Address Handling ---  
try:
    mac_data = ble.config('mac')
    mac_bytes = mac_data[1]
    hex_str = binascii.hexlify(mac_bytes).decode('utf-8')
    formatted_mac = ':'.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)]).upper()
    print(f"BLE MAC: {formatted_mac} (Note: This is in reverse byte order)")
    print("On your scanning device, look for MAC:", ':'.join([hex_str[i:i+2] for i in range(len(hex_str)-2, -2, -2)]).upper())
except Exception as e:
    print("MAC Error:", e)

# --- Data Storage ---
try:
    with open('data.json') as f:
        game_data = ujson.load(f)
except:
    game_data = {"score": 0, "state": "ready"}

# --- Main Loop ---
last_ack = time.time()
last_ble_time = time.time()
last_mqtt_time = time.time()


lcd = Lcd(12, 13)
lcd.lcd_display_string("Lets go gambling")
while True:
    try:
        current_time = time.ticks_ms()
        
        # Handle BLE reconnection if needed
        if not ble_connected and time.ticks_diff(current_time, last_reconnect_time) > RECONNECT_DELAY:
            initialize_ble()
            last_reconnect_time = current_time
        
        # Send button states when connected
        if ble_connected:
            buttons = [str(machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN).value()) for pin in range(1, 7)]
            button_data = ",".join(buttons)
            
            try:
                ble.gatts_write(char_handle, button_data.encode())
                ble.gatts_notify(conn_handle, char_handle)
            except Exception as e:
                print("Notification Error:", e)
                ble_connected = False
    
        # 2. Handle MQTT
        if current_time - last_mqtt_time >= 5:  # 5s interval
            try:
                if wlan.isconnected():
                    if not client:
                        initialize_mqtt()
                    else:
                        client.check_msg()
                        
                        # Check for BLE ACK timeout
                        if current_time - last_ack > 5:
                            client.publish("dashboard/error", "RPi4 offline")
                
                last_mqtt_time = current_time
            except Exception as e:
                print("MQTT Error:", e)
                client = None

        # 3. Save data periodically
        if current_time % 60 < 0.1:  # Every ~60 seconds
            try:
                with open('data.json', 'w') as f:
                    ujson.dump(game_data, f)
            except Exception as e:
                print("Save Error:", e)
    except Exception as e:
        print("Main Loop Error:", e)
        time.sleep(1)
        machine.reset() 
    time.sleep_ms(50)