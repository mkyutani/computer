import os
import sys
from dotenv import load_dotenv
from loguru import logger as loguru_logger

class Env:

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Env, cls).__new__(cls)
            load_dotenv()
            cls._logger = loguru_logger
            cls._logger.remove()
            cls._logger.add(sys.stderr, level="INFO")
            cls._logger.add( 'logs/log.txt', level="DEBUG")
        return cls._instance

    def __init__(self):
        pass

    def get(self, name):
        return os.environment.get(name)

    def logger(self):
        return self._logger

env = Env()
logger = Env().logger()