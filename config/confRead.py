# -*- coding: UTF-8 -*-
import configparser
import os


class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nj_config.ini')

    def read_openapi(self):
        """
        读取配置文件中host相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['openapi']

    def read_user(self):
        """
        读取配置文件中directory相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['user']

    def read_database(self):
        """
        读取配置文件中database相关信息
        :return: 包含数据库连接信息的字典
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return {
            'host': self.config.get('database', 'host'),
            'port': self.config.get('database', 'port'),
            'user': self.config.get('database', 'user'),
            'password': self.config.get('database', 'password'),
            'database_name': self.config.get('database', 'database_name')
        }


if __name__ == '__main__':
    a0 = Config()
    host = a0.read_database().get("host")
    print(host)
