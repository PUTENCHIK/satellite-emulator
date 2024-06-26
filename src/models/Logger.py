import logging
import sys
import os
import socket
from logging.handlers import RotatingFileHandler

class Logger:
	FORMATTER_STRING = f"%(asctime)s %(name)s" \
	f" %(levelname)s %(message)s"
	FORMATTER = logging.Formatter(FORMATTER_STRING)
	LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'logs.log')
	MAX_BYTES = 10 * 1024 * 1024 # 10 МБ
	BACKUP_COUNT = 5 # Сохранять 5 резервных копий

	# Создаем глобальный логгер
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	# Настраиваем обработчики (только один раз!)
	file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, mode='a')
	file_handler.setFormatter(FORMATTER)
	logger.addHandler(file_handler)

	def __init__(self, name: str, console_out: bool = False):
		# Устанавливаем имя логгера, если необходимо
		self.logger.name = name

		if console_out:
			stdout_handler = logging.StreamHandler(sys.stdout)
			stdout_handler.setFormatter(Logger.FORMATTER)
			self.logger.addHandler(stdout_handler)

	def add_debug(self, text: str):
		self.logger.debug(text)

	def add_info(self, text: str):
		self.logger.info(text)

	def add_warning(self, text: str):
		self.logger.warning(text)

	def add_error(self, text: str):
		self.logger.error(text)
