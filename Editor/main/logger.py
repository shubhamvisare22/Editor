import logging
import os
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    _instances: dict = {}

    def __new__(cls, job):
        if job not in cls._instances:
            cls._instances[job] = super(Logger, cls).__new__(cls)
        return cls._instances[job]

    def __init__(self, job):
        if hasattr(self, "initialized"):
            return  # Prevent re-initialization for singleton
        self.initialized = True
        self.job = job
        logs_dir = f"./log_files/{job}"
        self.log_obj = logging.getLogger(self.job)
        self.log_obj.setLevel(logging.DEBUG)
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        self.handler = TimedRotatingFileHandler(
            filename=os.path.join(logs_dir, f"{self.job}.log"),
            when="D",
            interval=1,
            backupCount=90,
            encoding="utf-8",
            delay=False,
        )
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(pathname)s - %(lineno)d - %(funcName)s - %(message)s"
        )
        self.handler.setFormatter(self.formatter)
        self.log_obj.addHandler(self.handler)

    @staticmethod
    def get_logger(job):
        return Logger(job).log_obj
