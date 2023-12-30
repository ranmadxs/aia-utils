from importlib.metadata import version
from aia_utils.Queue import QueueConsumer, QueueProducer
from aia_utils.logs_cfg import config_logger
from aia_utils.repositories.aia_msg_repo import AIAMessageRepository
from aia_utils.repositories.aia_semantic_repo import AIASemanticGraph

__version__ = version(__name__)


__all__ = ["QueueConsumer", "QueueProducer", "config_logger", "AIAMessageRepository", "AIASemanticGraph"]