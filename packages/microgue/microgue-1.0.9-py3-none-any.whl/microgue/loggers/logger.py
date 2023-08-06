import logging
import uuid


class Logger:
    trace_id = None
    _instance = None

    def __new__(cls, name=None, level=logging.DEBUG, trace_id=None, *args, **kwargs):
        if not cls._instance:
            logging.basicConfig()
            cls._instance = super().__new__(cls)
            cls._instance.__logger = logging.getLogger(name)
            cls._instance.__logger.setLevel(level)
            cls._instance.trace_id = uuid.uuid4()
        return cls._instance

    def start_trace(self, trace_id=None):
        if trace_id:
            self.trace_id = trace_id
        else:
            self.trace_id = uuid.uuid4()

    def debug(self, message, priority=None):
        self.log(message, priority=priority, level=logging.DEBUG)

    def info(self, message, priority=None):
        self.log(message, priority=priority, level=logging.INFO)

    def error(self, message, priority=None):
        self.log(message, priority=priority, level=logging.ERROR)

    def warning(self, message, priority=None):
        self.log(message, priority=priority, level=logging.WARNING)

    def critical(self, message, priority=None):
        self.log(message, priority=priority, level=logging.CRITICAL)

    def log(self, message, priority=None, level=logging.DEBUG):
        if priority == 1:
            self.__logger.log(level, f"{self.trace_id} ########## {message} ########################################")
        elif priority == 2:
            self.__logger.log(level, f"{self.trace_id} ########## {message} ##########")
        elif priority == 3:
            self.__logger.log(level, f"{self.trace_id} ########## {message}")
        else:
            self.__logger.log(level, f"{self.trace_id} {message}")
