# -*- coding: UTF-8 -*-
import logging
import pytest

from common.read_json_utils import read_json, read_json_title


class TestKd:

    @pytest.mark.kd
    @pytest.mark.parametrize("cpCode, mailNo, tel, orderType",
                             read_json("kd.json", "trace_search"),
                             ids=read_json_title("kd.json", "trace_search"))
    def test_trace_search(self, kd_manager, cpCode, mailNo, tel, orderType):
        """实时快递查询"""
        logging.info("starting test case test_trace_search")
        data = {
            "cpCode": cpCode,
            "mailNo": mailNo,
            "tel": tel,
            "orderType": orderType
        }
        ret_code, ret_data = kd_manager.trace_search(data)
        logging.info(f"日志内容：{ret_data}")
        assert ret_code == 200
        logging.info("test case test_trace_search success")
