# Created by Delitel

import logging
import os

formatter = logging.Formatter('[%(asctime)s] %(levelname)s | %(name)s: %(message)s', '%d-%m-%Y %H:%M:%S')


class LOGGER:

    def __init__(self, logger_name):

        if not os.path.exists("logs"):
            os.mkdir("logs")

        self.logger = logging.getLogger(logger_name)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()

        self.logger.setLevel(logging.INFO)

        file = logging.FileHandler(f"logs/{logger_name}.txt")
        file.setFormatter(formatter)

        stream_handl = logging.StreamHandler()
        stream_handl.setFormatter(formatter)

        self.logger.addHandler(file)
        self.logger.addHandler(stream_handl)

    def info(self, text, exc_info=False):
        """ВЫВОД ИНФО В ЛОГ"""
        self.logger.info(text, exc_info=exc_info)

    def error(self, text, exc_info=False):
        """ВЫВОД ОШИБКИ В ЛОГ"""
        self.logger.error(text, exc_info=exc_info)

