# -*- coding: UTF-8 -*-
import logging
import pytest

from common.read_json_utils import read_json, read_json_title


class TestKd:

    @pytest.mark.nj
    @pytest.mark.parametrize("question, answer, search_type, page, page_size",
                             read_json("nj.json", "nj_search"),
                             ids=read_json_title("nj.json", "nj_search"))
    def test_nj_search(self, nj_manager, question, answer, search_type, page, page_size):
        """通过查询参数获取相关的脑筋急转弯"""
        logging.info("starting test case test_nj_search")
        params = {
            "question": question,
            "answer": answer,
            "search_type": search_type,
            "page": page,
            "page_size": page_size
        }
        ret_code, ret_data = nj_manager.nj_search(params)
        logging.info(f"日志内容：{ret_data}")
        assert ret_code == 200
        logging.info("test case test_nj_search success")
