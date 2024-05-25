# -*- coding: UTF-8 -*-
import logging

import pymysql


class MySQLHelper:
    def __init__(self, host, port, user, password, db_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                password=self.password,
                database=self.db_name,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logging.info("Successfully connected to the database")
        except Exception as e:
            logging.error(f"Error connecting to the MySQL database: {e}")

    def execute_query(self, query):
        """执行 SELECT 类型的 SQL 语句"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logging.error(f"Error executing query: {e}")
        finally:
            self.connection.close()

    def execute_non_query(self, query):
        """执行 INSERT、UPDATE、DELETE 等非 SELECT 类型的 SQL 语句"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(query)
                self.connection.commit()  # 提交事务
                return affected_rows
        except Exception as e:
            logging.error(f"Error executing non-query: {e}")
            self.connection.rollback()  # 发生错误时回滚事务
        finally:
            self.connection.close()


if __name__ == "__main__":
    helper = MySQLHelper('localhost', 'your_username', 'your_password', 'your_db_name')
    helper.connect()

    # 执行查询
    query = "SELECT * FROM your_table"
    results = helper.execute_query(query)
    print(results)

    # 执行非查询（例如插入）
    non_query = "INSERT INTO your_table (column1, column2) VALUES ('value1', 'value2')"
    rows_affected = helper.execute_non_query(non_query)
    print(f"{rows_affected} rows affected.")
