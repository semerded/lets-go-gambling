from smartcard.System import readers

# Get list of available smart card readers
r = readers()
if not r:
    raise Exception("No smart card readers found.")

reader = r[0]  # Select first reader
connection = reader.createConnection()

try:
    connection.connect()
    print("✅ Smart card detected!")
except:
    print("❌ No card inserted.")
