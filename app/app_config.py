import os
from dotenv import load_dotenv

load_dotenv()

def get_environ_variable_or_exit(name):
    if name not in os.environ:
        raise Exception(f"Missing {name} in ENVIRONMENT variables")
    return os.environ[name]


DATASTORE_FILENAME = "./data/data.pickle"
mqtt_broker = get_environ_variable_or_exit("MQTT_BROKER")
mqtt_port = int(get_environ_variable_or_exit("MQTT_PORT"))
mqtt_topic = get_environ_variable_or_exit("MQTT_TOPIC")
