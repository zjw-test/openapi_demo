# -*- coding: UTF-8 -*-
import logging
import logging.handlers
import os
from datetime import datetime

FILE_LOCATION = os.path.dirname(__file__)


def config_log():
    logger = logging.getLogger()
    if not logger.handlers:  # 如果还没有配置处理器
        logger.setLevel(logging.INFO)
        cmd = logging.StreamHandler()
        today = datetime.now().strftime('%Y-%m-%d')
        log_path = os.path.join(FILE_LOCATION, "log", f'demo_log_{today}.log')
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_path,
            when='midnight', interval=1, backupCount=3,
            encoding='utf-8')
        fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
        formatter = logging.Formatter(fmt=fmt)
        file_handler.setFormatter(formatter)
        cmd.setFormatter(formatter)
        logger.addHandler(cmd)
        logger.addHandler(file_handler)
