import bluetooth

ble = bluetooth.BLE()
ble.active(True)
# Scan for RPi's BLE server
ble.scan()