# -*- coding: UTF-8 -*-
import logging
import pytest


class TestXh:

    @pytest.mark.xh
    def test_get_random(self, xh_manager):
        """随机获取笑话"""
        logging.info("starting test case test_get_random")
        payload = {'pageSize': 1}
        ret_code, ret_data = xh_manager.get_jokes_by_random(payload)
        logging.info(f"日志内容：{ret_data}")
        assert ret_code == 200
        logging.info("test case test_describe_resource_pools success")

    @pytest.mark.xh
    def test_get_random_002(self, xh_manager, mysql_connection):
        """随机获取笑话并验证数据库操作"""
        logging.info("starting test case test_get_random")
        payload = {'pageSize': 1}
        ret_code, ret_data = xh_manager.get_jokes_by_random(payload)
        logging.info(f"日志内容：{ret_data}")
        assert ret_code == 200

        # 查询验证
        select_query = "select count(*) from student where s_sex = '男'"
        query_result = mysql_connection.execute_query(select_query)
        student_count = query_result[0]['count(*)']
        logging.info(f"Number of male students: {student_count}")
        assert student_count == 4

        # 使用从conftest.py中传递过来的数据库连接
        # insert_query = "INSERT INTO jokes (content) VALUES ('这是一个测试笑话')"
        # rows_affected = mysql_connection.execute_non_query(insert_query)
        # assert rows_affected > 0, "笑话插入数据库失败"

        logging.info("test case test_get_random success")
