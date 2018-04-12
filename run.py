from SmartOutlet import app

import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)-7s] (%(threadName)-11s) %(message)s",
                    )

# separate thread 
def database_service():
    logging.debug("Starting")
    print("this is where the database will start")
    logging.debug("Exiting")
    
database_t = threading.Thread(name="Database", target=database_service)
database_t.start()

app.run(debug=True, host="0.0.0.0")
