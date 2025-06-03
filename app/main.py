import pickle
import threading
import time
from os import path
import app_logger
import logging
import paho.mqtt.client as mqtt
from flask import Flask, jsonify, abort
import schedule
from pathlib import Path
import os
import app_config
import app_data

app = Flask(__name__)

changed_data_store = False


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(app_config.mqtt_topic)
    logging.info(f"connected to MQTT broker and subscribed {app_config.mqtt_topic}")


def on_message(client, userdata, msg):
    global changed_data_store, single_log
    try:
        payload_decoded = msg.payload.decode("utf-8")
        app_data.data_store[msg.topic] = payload_decoded
        # logging.debug(f"Received message: {msg.topic} = {payload_decoded}")
        changed_data_store = True
    except UnicodeDecodeError as e:
        pass


def backup_datastore():
    global changed_data_store
    if not changed_data_store:
        return
    with open(app_config.DATASTORE_FILENAME, "wb") as fp:
        fp.write(pickle.dumps(app_data.data_store))
        logging.debug("Saving datastore to disk.")
    changed_data_store = False


schedule.every(60).seconds.do(backup_datastore)


def schedule_thread_fun():
    while True:
        schedule.run_pending()
        time.sleep(5)


@app.route('/all', methods=['GET'])
def flask_all():
    return jsonify(app_data.data_store)


@app.route('/single/<path:subpath>', methods=['GET'])
def flask_single(subpath):
    if subpath not in app_data.data_store:
        abort(404)
    return app_data.data_store[subpath]


def startup():
    global app, changed_data_store

    logging.debug("Debug mode is enabled")
    logging.info(f"app init (mqtt://{app_config.mqtt_broker}:{app_config.mqtt_port}/{app_config.mqtt_topic})")

    Path(app_config.DATASTORE_FILENAME).parent.mkdir(parents=True, exist_ok=True)

    if path.exists(app_config.DATASTORE_FILENAME):
        with open(app_config.DATASTORE_FILENAME, "rb") as fp:
            app_data.data_store = pickle.loads(fp.read())
            logging.info(f"Rebuilding IPDB")

    changed_data_store = False

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    if app_config.mqtt_username is not None and app_config.mqtt_username == "":
        mqtt_client.username_pw_set(app_config.mqtt_username, app_config.mqtt_password)
        logging.info(f"Using credentials with username {app_config.mqtt_username}")
    mqtt_client.connect(app_config.mqtt_broker, app_config.mqtt_port, 60)

    mqtt_client.loop_start()
    logging.info(f"started mqtt loop")
    schedule_thread = threading.Thread(target=schedule_thread_fun, daemon=True)
    schedule_thread.start()
    return app


app = startup()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

