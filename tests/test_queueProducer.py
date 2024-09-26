#https://api.cloudkarafka.com/
from Queue import QueueProducer, QueueConsumer
import os
from dotenv import load_dotenv
import logging
load_dotenv()
import json
from logs_cfg import config_logger
config_logger()
currentPath = os.getcwd()
logger = logging.getLogger(__name__)
import pytest
from confluent_kafka import Producer
TEST_MESSAGE = "Test message from pytest"
from mqtt import MqttProducer

#poetry run pytest tests/test_queueProducer.py::test_produce -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce():
    topicProducer = os.environ['TEST_CLOUDKAFKA_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topicProducer)
    queueProducer = QueueProducer("test001", "test001", "aia-utils")
    queueProducer.send(TEST_MESSAGE)
    queueProducer.flush()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

#poetry run pytest tests/test_queueProducer.py::test_consume -s
def test_consume():
    topicConsumer = os.environ['CLOUDKAFKA_TOPIC_CONSUMER']
    logger.info("Test Consume queue " + topicConsumer)
    queueConsumer = QueueConsumer(topicConsumer, "aia-utils")
    queueConsumer.listen()

#poetry run pytest tests/test_queueProducer.py::test_produce2 -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce2():
    p = Producer({'bootstrap.servers': '192.168.1.13:9094'})
    p.poll(0)
    p.produce('test001', 'again aiaf33333', callback=delivery_report)
    p.flush()

#poetry run pytest tests/test_mqtt.py::test_produce -s
#@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce():
    topic = os.environ['MQTT_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topic)
    client_id = "aia-utils-test-001"
    producer = MqttProducer(topic, client_id)
    producer.send_message(TEST_MESSAGE)