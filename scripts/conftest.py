# -*- coding: UTF-8 -*-
import logging
import os
import shutil

import pymysql

from global_config import FILE_LOCATION

from api.kd_manager import KdManager
from api.nj_manager import NjManager
from common.mysql_utils import MySQLHelper
from config.confRead import Config
from global_config import config_log

import pytest
from api.xh_manager import XhManager

config_log()
# 全局配置日志

def is_master():
    """判断当前是否为主节点"""
    return not os.environ.get('PYTEST_XDIST_WORKER', False)


# 钩子函数，在pytest的整个测试会话开始之前执行
def pytest_sessionstart(session):
    """会话开始前执行的代码，仅在主节点上执行清理任务"""
    if is_master():
        tmp_path = FILE_LOCATION + os.sep + "tmp"
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.makedirs(tmp_path)
        logging.info("主节点会话开始：执行了清理任务")


# class级别会话开始执行
# @pytest.fixture(scope="class")
# def demo_user_login():
#     pass


# 钩子函数，在pytest测试会话结束后执行
def pytest_sessionfinish(session, exitstatus):
    """会话结束后执行的代码，仅在主节点上生成Allure测试报告"""
    if is_master():
        tmp_path = FILE_LOCATION + os.sep + "tmp"
        report_path = FILE_LOCATION + os.sep + "report"
        os.system(f"allure generate --clean {tmp_path} -o {report_path}")
        logging.info("会话结束：生成了Allure测试报告")


@pytest.fixture(scope="session")
def mysql_connection():
    """Fixture to initialize and provide MySQL connection from config file."""
    config = Config()
    db_config = config.read_database()

    mysql_helper = MySQLHelper(
        host=db_config['host'],
        port=int(db_config['port']),
        user=db_config['user'],
        password=db_config['password'],
        db_name=db_config['database_name']
    )
    logging.info(
        f"connecting to database {db_config['host']}:{db_config['port']}:{db_config['user']}...")

    try:
        mysql_helper.connect()  # 尝试连接到数据库
        logging.info("Successfully connected to the database.")
    except pymysql.err.OperationalError as oe:
        logging.error(f"OperationalError connecting to the database: {oe}")
    except pymysql.err.InterfaceError as ie:
        logging.error(f"InterfaceError connecting to the database: {ie}")
    except Exception as e:
        logging.error(f"General error connecting to the database: {e}")
        raise  # 重新抛出异常，让pytest捕获并报告错误

    yield mysql_helper  # 提供给测试使用

    # 在尝试关闭连接前检查连接状态
    if mysql_helper.connection and not getattr(mysql_helper.connection, '_closed', False):
        mysql_helper.connection.close()
        logging.info("MySQL connection closed.")
    else:
        logging.warning("Connection was either already closed or not properly initialized.")


@pytest.fixture(scope="class")
def xh_manager():
    """初始化并返回XhManager实例"""
    return XhManager()


@pytest.fixture(scope="class")
def kd_manager():
    """初始化并返回KdManager实例"""
    return KdManager()


@pytest.fixture(scope="class")
def nj_manager():
    """初始化并返回KdManager实例"""
    return NjManager()
