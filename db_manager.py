import json
import logging

# Setup logger - might need to remove if it gets annoying
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')


# Loads the database file and checks to see if item already exists
def load(links, titles):
    # Open the file for reading and load the data into a dict
    with open('db.json', 'r') as file:
        data = json.load(file)

    # Open the file for writing and log any new entries
    with open('db.json', 'w') as file:
        for idx, _ in enumerate(links):
            # If this is not in the database, send a notification
            if not titles[idx] in data:
                # TODO: Send message here
                data[str(titles[idx])] = links[idx]
            else:
                logger.info(f'Item with key "{titles[idx]}" already exists')

        json.dump(data, file, indent=4)
