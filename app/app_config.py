import os
from dotenv import load_dotenv

load_dotenv()

def get_environ_variable_or_exit(name, default_value=None):
    if name not in os.environ:
        if default_value is not None:
            return default_value
        raise Exception(f"Missing {name} in ENVIRONMENT variables")
    return os.environ[name]


DATASTORE_FILENAME = "./data/data.pickle"
mqtt_broker = get_environ_variable_or_exit("MQTT_BROKER")
mqtt_port = int(get_environ_variable_or_exit("MQTT_PORT"))
mqtt_topic = get_environ_variable_or_exit("MQTT_TOPIC")

mqtt_username = get_environ_variable_or_exit("MQTT_USERNAME", "")
mqtt_password = get_environ_variable_or_exit("MQTT_PASSWORD", "")

