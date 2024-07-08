from aiogram import Router
import logging
import os
from config import logs_path

router: Router = Router()

if not os.path.exists(logs_path):
    os.makedirs(logs_path)


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(filename=logs_path + 'logs.log')
stram_handler = logging.StreamHandler()
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(message)s")

stram_handler.setLevel("INFO")
file_handler.setLevel("INFO")
file_handler.setFormatter(formatter)
stram_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stram_handler)

logger.setLevel("INFO")