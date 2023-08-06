from .singleton import Singleton
import logging
import sys
import os


class LogFormat:
    DEFAULT = "%(levelname)s|%(asctime)s|%(message)s"

class LogMode:
    LOG_MODE_FILE: str = "file"
    LOG_MODE_CONSOLE: str = "console"


class LogLevel:
    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    ERROR: str = "ERROR"


class Logger(Singleton):

    def __init__(self, 
                 log_name: str = "logger", 
                 log_level: str = LogLevel.INFO, 
                 log_mode: str  = LogMode.LOG_MODE_FILE, 
                 log_path: str = "server.log",
                 log_format: str = LogFormat.DEFAULT):
        self._logger: logging.Logger = logging.getLogger(log_name)
        self.log_mode: str = log_mode
        self.log_level: str = log_level
        self.log_path: str = log_path
        self.log_format: str = log_format

    def init_logger(self):
        self._logger.setLevel(self.log_level)
        handler = None
        if self.log_mode == LogMode.LOG_MODE_FILE:
            up_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            log_path = up_path + f"/{os.getpid()}-" + self.log_path
            print(f"log_path: {log_path}")
            handler = logging.FileHandler(up_path + f"/{os.getpid()}-" + self.log_path, encoding="utf-8")

        if self.log_mode == LogMode.LOG_MODE_CONSOLE:
            handler = logging.StreamHandler(sys.stdout)

        if not handler:
            return

        handler.setLevel(level=self.log_level)
        log_format = logging.Formatter(self.log_format)
        handler.setFormatter(log_format)

        self._logger.addHandler(handler)

    @staticmethod
    def format_msg(msg):
        try:
            caller = sys._getframe(1)
            file_name = '/'.join(caller.f_code.co_filename.split('/')[-3:])
            call_name, file_no = caller.f_code.co_name, caller.f_lineno
            return ':'.join([file_name, call_name, str(file_no)]) + f'|{msg}'
        except Exception as e:
            return msg

    def debug(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LogMode.LOG_MODE_CONSOLE:
            msg = f"\033[34m{msg}\033[0m"
        self._logger.debug(msg)

    def info(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LogMode.LOG_MODE_CONSOLE:
            msg = f"\033[32m{msg}\033[0m"
        self._logger.info(msg)

    def warning(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LogMode.LOG_MODE_CONSOLE:
            msg = f"\033[33m{msg}\033[0m"
        self._logger.warning(msg)

    def error(self, msg: str):
        msg = self.format_msg(msg)
        if self.log_mode == LogMode.LOG_MODE_CONSOLE:
            msg = f"\033[31m{msg}\033[0m"
        self._logger.error(msg, stack_info=True)


logger = Logger()


if __name__ == "__main__":
    logger.init_logger()
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")


