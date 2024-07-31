import logging
from logs_cfg import config_logger
config_logger()
logger = logging.getLogger(__name__)
from aia_utils.toml_utils import getVersion, aia_utils_version
from aia_utils.manifest import generate_manifest

#poetry run pytest tests/test_init.py::test_init -s
def test_init():
    logger.info('test_init')
    logger.info(aia_utils_version())
    assert getVersion() != None

#poetry run pytest tests/test_init.py::test_manifest -s
def test_manifest():
    logger.info('test_manifest22')
    manifest = generate_manifest(custom_properties={"custom_k": "custom_v"})
    logger.info('==========================')
    logger.info(manifest)
    logger.info('==========================')
    assert manifest != None