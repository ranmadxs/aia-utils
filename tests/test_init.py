import logging
from logs_cfg import config_logger
config_logger()
logger = logging.getLogger(__name__)
from aia_utils.toml_utils import getVersion

#poetry run pytest tests/test_init.py::test_init -s
def test_init():
    logger.info('test_init')
    logger.info(getVersion())
    assert getVersion() != None