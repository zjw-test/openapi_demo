# -*- coding: UTF-8 -*-
import copy
import json
import logging
import os

import requests
from config.confRead import Config
import urllib.parse


class HttpBaseManager:
    """
    HTTP请求管理器，用于封装HTTP请求的通用逻辑，包括配置、头信息管理、请求发送等。
    """

    def __init__(self):
        """
        初始化方法，从配置文件加载API设置，并设置默认请求头及超时时间。
        """
        # 读取配置文件中的OpenAPI设置
        config_instance = Config()
        openapi_config = config_instance.read_openapi()

        # 解析并保存协议、主机、端口、认证令牌等配置
        self.protocol = openapi_config["protocol"]
        self.host = openapi_config["host"]
        self.port = openapi_config.get("port", "")
        self.host_port = f"{self.host}:{self.port}" if self.port else self.host
        self.x_apispace_token = openapi_config["X-APISpace-Token"]

        # 设置默认请求头，更改默认Content-Type为application/json
        self.default_headers = {
            "X-APISpace-Token": self.x_apispace_token,
            "Content-Type": "application/json"
        }

        # 设置默认超时时间（单位秒）
        self.timeout = openapi_config.get("timeout", 300)

    def generate_headers(self, content_type="application/json"):
        """
        生成请求头，允许覆盖默认的Content-Type，现默认为application/json。
        :param content_type: 自定义的Content-Type，默认为application/json。
        :return: 包含自定义Content-Type的请求头字典。
        """
        headers = copy.deepcopy(self.default_headers)
        headers["Content-Type"] = content_type
        return headers

    def http_request(self, uri, method="GET", data=None, headers=None, content_type=None, protocol=None):
        """
        发送HTTP请求，并处理响应。
        :param uri: 请求的URI路径。
        :param method: 请求方法，默认为GET。
        :param data: 请求体数据。
        :param headers: 自定义请求头，若未提供则使用默认头。
        :param content_type: 自定义Content-Type。
        :param protocol: 请求使用的协议，默认从配置读取。
        :return: 一个元组，包含响应状态码和解析后的响应数据（字典形式）。
        """
        # 初始化请求参数和JSON数据
        params = None
        json_data = None

        # 使用自定义或默认的请求头，确保默认Content-Type为application/json
        headers = headers or self.generate_headers(content_type)

        # 构建完整URL
        effective_protocol = protocol or self.protocol
        url = f"{effective_protocol}://{self.host_port}{uri}"

        # 记录日志，显示即将发起的请求信息
        logging.info(f"Making request with headers: {headers}, to URL: {url}")

        # 根据请求方法准备参数或JSON数据
        if method.lower() == 'get':
            params = data or {}
        elif method.lower() in ['post', 'put', 'patch']:
            # 根据Content-Type决定如何处理data
            if headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                data = urllib.parse.urlencode(data) if data else ''
            else:
                json_data = data
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # 初始化响应状态码和数据
        ret_code = None
        ret_data = None

        try:
            # 发送请求，根据Content-Type选择参数形式
            request_kwargs = {'json': json_data} if json_data is not None else {'data': data}
            response = requests.request(
                method,
                url,
                params=params,
                **request_kwargs,
                headers=headers,
                timeout=self.timeout
            )

            # 检查响应状态并解析响应数据
            response.raise_for_status()
            ret_data = response.json() if response.text else {}
            logging.info(f"Response Data: {ret_data}")
            ret_code = response.status_code

        except requests.exceptions.Timeout as e:
            logging.error(f"Request timed out: {e}")
            ret_code, ret_data = -1, {"error": "Timeout"}
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            ret_code, ret_data = -1, {}
        finally:
            logging.info(
                f"HTTP request complete, status code: {ret_code or 'unknown'}, response data: {ret_data or 'no data'}"
            )

        return ret_code, ret_data

    def download_file(self, requests_method, url, filename, params):
        """下载文件"""
        headers = self.generate_headers()
        response = requests.request(requests_method, url, headers=headers, data=json.dumps(params))
        assert response.status_code == 200
        # 确保请求成功
        if response is None:
            logging.debug("Error: Response is None")
            return

        # 确保响应的状态码为200
        if response.status_code != 200:
            raise Exception("Error: Response status code is not 200")

        # 将文件写入到本地
        with open(filename, 'wb') as f:
            f.write(response.content)

        # 断言文件存在
        assert os.path.exists(filename)

        # 断言文件大小
        actual_file_size = os.path.getsize(filename)
        assert actual_file_size > 0
        logging.debug(actual_file_size)

        # 删除文件
        os.remove(filename)
