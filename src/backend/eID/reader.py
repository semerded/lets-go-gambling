from smartcard.System import readers

# APDU command for selecting the Identity file (Belgian eID structure)
SELECT_ID_APDU_COMMAND = [
    0x00, 0xA4, 0x08, 0x0C, 0x06,
    0x3F, 0x00, 0xDF, 0x01, 0x40, 0x31  # Identity File Path
]

# Initial APDU Read Request (Le = 0 to get correct length)
READ_COMMAND = [0x00, 0xB0, 0x00, 0x00, 0x00]

# Correct Keys
RRN = 6
FIRST_NAME_TAG = 8
LAST_NAME_TAG = 7
BIRTHDATE_TAG = 12

# Select smart card reader


def read(connection):
    try:
        # Select ID file
        _, sw1, sw2 = connection.transmit(SELECT_ID_APDU_COMMAND)
        if sw1 != 0x90 or sw2 != 0x00:
            raise Exception("Failed to select ID file on the eID card.")

        # Read data (adjusting Le dynamically)
        response, sw1, sw2 = connection.transmit(READ_COMMAND)
        if sw1 == 0x6C:  # If status 6Cxx, the second byte indicates correct length
            READ_COMMAND[-1] = sw2  # Set correct Le
            response, sw1, sw2 = connection.transmit(READ_COMMAND)

        # Parsing function for TLV data format
        def parse_eid_data(raw_data):
            parsed = {}
            idx = 0

            while idx < len(raw_data):
                tag = raw_data[idx]  # Read tag identifier
                idx += 1
                if idx >= len(raw_data):
                    break

                length = raw_data[idx]  # Read length byte
                idx += 1
                if idx + length > len(raw_data):
                    break

                value_bytes = raw_data[idx:idx + length]  # Extract data
                value = bytes(value_bytes).decode("utf-8", errors="ignore").strip()

                parsed[tag] = value  # Store parsed data
                idx += length  # Move to next entry

            return parsed

        # Extract correct fields
        parsed_data = parse_eid_data(response)
        relevant_data = {"firstName": parsed_data[FIRST_NAME_TAG], "lastName": parsed_data[LAST_NAME_TAG],
                        "birthdate": parsed_data[BIRTHDATE_TAG], "rrn": parsed_data[RRN]}
        return relevant_data
    except Exception as e:
        return None # average card reader experience
