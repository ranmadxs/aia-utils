#https://api.cloudkarafka.com/
from Queue import QueueProducer
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

#poetry run pytest tests/test_queueProducer.py::test_produce -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce():
    topicProducer = os.environ['TEST_CLOUDKAFKA_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topicProducer)
    queueProducer = QueueProducer("test001", "test001", "aia-utils")
    queueProducer.send({"cmd": "test"})
    queueProducer.flush()

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

#poetry run pytest tests/test_queueProducer.py::test_produce2 -s
@pytest.mark.skip(reason="esta pensado para correr en local")
def test_produce2():
    p = Producer({'bootstrap.servers': '192.168.1.13:9094'})
    p.poll(0)
    p.produce('test001', 'again aiaf33333', callback=delivery_report)
    p.flush()

