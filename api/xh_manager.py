# -*- coding: UTF-8 -*-
import logging
from api.http_base_manager import HttpBaseManager
from config.confRead import Config

from global_config import config_log

config_log()


class XhManager(HttpBaseManager):

    def __init__(self):
        super().__init__()  # 修改为更简洁的super()调用形式
        config_instance = Config()
        openapi_config = config_instance.read_openapi()
        self.xhdq = openapi_config["xhdq"]
        self.joke = openapi_config["joke"]

    def get_jokes_by_random(self, data):
        """随机获取笑话"""
        logging.debug("starting to get_jokes_by_random")
        uri = f"/{self.xhdq}/common/{self.joke}/getJokesByRandom"
        ret_code, ret_data = self.http_request(uri, "POST", data,
                                               content_type='application/x-www-form-urlencoded')
        if ret_code == 200:
            return ret_code, ret_data
        logging.warning("get_jokes_by_random failed! ret_code:{0}, ret_data:{1}".format(ret_code, ret_data))
        return ret_code, ret_data
