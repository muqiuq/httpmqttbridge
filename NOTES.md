# Test Docker locally

```bash
podman build -t httpmqttbridge . && podman run -e DEBUG=DEBUG -e MQTT_BROKER=test.mosquitto.org -e MQTT_PORT=1883 -e MQTT_TOPIC="#" --rm -p 5000:5000 httpmqttbridge
```