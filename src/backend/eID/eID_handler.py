from src.backend.eID.reader import read
from src.backend.eID.recognizer import recognize
from threading import Thread
from time import sleep
from src import data
from smartcard import System as EidReader
import hashlib
from src.enums import cardReaderState
from src.enums import pages


readers = EidReader.readers()
if not readers:
    if data.debugging:
        data.current_player_id = "dev"
        data.current_player = data.player_data[data.current_player_id]
        data.active_page = pages.game
    else:
        raise Exception("No smart card readers found.")
else:
    data.card_reader_available = True

def run_eid_thread():
    data.card_reader_thread_running = True
    print("new thread spawned")
    Thread(target=eid_thread_loop).start()

def stop_eid_thread():
    data.card_reader_thread_running = False
    
    
def eid_thread_loop():
    while data.card_reader_thread_running and data.running and data.card_reader_available:
        connection = recognize(readers)
        if connection is not None and data.card_data is None:
            result = read(connection)
            if data.card_reader_state == cardReaderState.noCard:
                data.card_reader_state = cardReaderState.cardInserted
            if result is not None:
                data.card_data = filter_data(result)
                data.card_reader_state = cardReaderState.succes
            else:
                data.card_reader_state = cardReaderState.badRead
        elif connection is None:
            data.card_data = None
            data.card_reader_state = cardReaderState.noCard
        sleep(0.5)
    
MONTHS = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")

def filter_data(data):
    data["firstName"] = data["firstName"].split(" ")[0]
    day = data["birthdate"].split(" ")[0]
    month = MONTHS.index(data["birthdate"].split(" ")[1]) + 1
    year = data["birthdate"].split(" ")[-1]
    data["birthdate"] = f"{year}-{month}-{day}"
    data["rrn"] = hashlib.sha256(data["rrn"].encode()).hexdigest()
    return data