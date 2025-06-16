import os
from dotenv import load_dotenv
load_dotenv()
import logging
from aia_utils.mqtt import MqttProducer, MqttConsumer
from aia_utils.logs_cfg import config_logger
config_logger()
logger = logging.getLogger(__name__)


import paho.mqtt.client as mqtt
import pytest
import time

# Datos del broker MQTT
MQTT_HOST = "broker.mqttdashboard.com"
MQTT_PORT = 1883
MQTT_USERNAME = "test"
MQTT_PASSWORD = "test"
MQTT_TOPIC = "yai-mqtt/in"
TEST_MESSAGE = "Test message from pytest"
received_messages = []

def callback_on_message(message):
    """Callback para manejar mensajes entrantes."""
    logger.info(f"Received message: {message}")
  

#poetry run pytest tests/test_mqtt.py::test_produce -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce():
    topic = os.environ['MQTT_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topic)
    client_id = "aia-utils-test-001"
    producer = MqttProducer(topic, client_id)
    producer.send_message(TEST_MESSAGE)

#poetry run pytest tests/test_mqtt.py::test_consume_message -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_consume_message():
    """Test para recibir un mensaje MQTT"""
    topic = os.environ['MQTT_TOPIC_PRODUCER']
    logger.info("Test consume queue " + topic)
    client_id = "aia-utils-test-001"
    MqttConsumer(topic, client_id, [callback_on_message])