from smartcard.System import readers

# Get list of available smart card readers

def recognize(readers):
    reader = readers[0]  # Select first reader
    connection = reader.createConnection()

    try:
        connection.connect()
        return connection
    except:
        return None
