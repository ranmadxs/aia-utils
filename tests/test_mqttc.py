import paho.mqtt.client as mqtt
import logging
import pytest
MQTT_HOST = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_USERNAME = "test"
MQTT_PASSWORD = "test"
MQTT_TOPIC = "yai-mqtt/in"
TEST_MESSAGE = "Test message from pytest"
received_messages = []

# Configurar logging
from logs_cfg import config_logger
config_logger()
logger = logging.getLogger(__name__)

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        logger.error(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        logger.info(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        logger.info("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        logger.error(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

def on_message(client, userdata, message):
    # userdata is the structure we choose to provide, here it's a list()
    userdata.append(message.payload)
    msg_txt = message.payload.decode()
    logger.info(f"Received message: {msg_txt} from topic: {message.topic}")
    # We only want to process 10 messages
    if len(userdata) >= 2:
        client.unsubscribe(MQTT_TOPIC)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        logger.error(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(MQTT_TOPIC)


#poetry run pytest tests/test_mqttc.py::test_consume_message -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_consume_message():
    """Test para recibir un mensaje MQTT"""

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe

    mqttc.user_data_set([])
    mqttc.connect(MQTT_HOST)
    mqttc.loop_forever()
    print(f"Received the following message: {mqttc.user_data_get()}")