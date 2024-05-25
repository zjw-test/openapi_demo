# -*- coding: UTF-8 -*-
import logging
from api.http_base_manager import HttpBaseManager
from config.confRead import Config


class KdManager(HttpBaseManager):

    def __init__(self):
        super().__init__()
        config_instance = Config()
        openapi_config = config_instance.read_openapi()
        self.wlgj1 = openapi_config["wlgj1"]

    def trace_search(self, data):
        """实时快递查询"""
        logging.info("starting to trace_search")
        uri = f"/{self.wlgj1}/paidtobuy_api/trace_search"
        ret_code, ret_data = self.http_request(uri, "POST", data)
        if ret_code == 200:
            return ret_code, ret_data
        logging.warning("trace_search failed! ret_code:{0}, ret_data:{1}".format(ret_code, ret_data))
        return ret_code, ret_data
