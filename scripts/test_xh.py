# -*- coding: UTF-8 -*-
import logging

import pytest

from api.xh_manager import XhManager


class TestXh:

    @pytest.fixture(scope="class")
    def xh_manager(cls):
        """初始化并返回XhManager实例"""
        return XhManager()

    @pytest.mark.smoke
    def test_get_random(self, xh_manager):
        payload = {'pageSize': 1}
        ret_code, ret_data = xh_manager.get_jokes_by_random(payload)
        logging.info(f"日志内容：{ret_data}")
        assert ret_code == 200
