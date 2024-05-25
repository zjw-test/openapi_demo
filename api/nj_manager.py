# -*- coding: UTF-8 -*-
import logging

from api.http_base_manager import HttpBaseManager
from config.confRead import Config
import urllib.parse


class NjManager(HttpBaseManager):

    def __init__(self):
        super().__init__()
        config_instance = Config()
        openapi_config = config_instance.read_openapi()
        self.v1 = openapi_config["v1"]

    def nj_search(self, params):
        """通过查询参数获取相关的脑筋急转弯"""
        logging.info("starting to nj_search")
        uri = f"/njjzw/api/{self.v1}/riddle/brain/search"
        new_params = {k: v for k, v in params.items() if v is not None}
        query_string = urllib.parse.urlencode(new_params)
        new_uri = uri + "?" + query_string
        ret_code, ret_data = self.http_request(new_uri, "GET")
        if ret_code == 200:
            return ret_code, ret_data
        logging.warning("nj_search failed! ret_code:{0}, ret_data:{1}".format(ret_code, ret_data))
        return ret_code, ret_data
