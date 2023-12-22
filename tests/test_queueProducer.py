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

#poetry run pytest tests/test_queueProducer.py::test_produce -s
def test_produce():
    topicProducer = os.environ['TEST_CLOUDKAFKA_TOPIC_PRODUCER']
    logger.info("Test Produce queue " + topicProducer)
    queueProducer = QueueProducer(topicProducer, "test001", "aia-utils")
    queueProducer.send({"cmd": "test"})
    queueProducer.flush()