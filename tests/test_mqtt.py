import os
from dotenv import load_dotenv
load_dotenv()
import logging
from mqtt import MqttClient
from logs_cfg import config_logger
config_logger()
logger = logging.getLogger(__name__)

#poetry run pytest tests/test_mqtt.py::test_produce -s
def test_produce():
    topic = os.environ['MQTT_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topic)
    client_id = "aia-utils-test-001"
    mqtt_client = MqttClient(topic, client_id)
    mqtt_client.send_message("Test message vPaho2")