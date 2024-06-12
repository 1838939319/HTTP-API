#coding:utf-8
import json

import allure
import pytest
import requests
from t0515.common.recodelog import logs
from requests import utils
from  t0515.common.readymal import ReadYaml

class SendRequest(object):
    """
    封装接口的请求
    """

    def __init__(self):
        self.read = ReadYaml()

    def get(self,url,data,header):
        """

        :param url: 请求路由
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        if header is None:
            res = requests.get(url=url,params=data)
        else:
            res = requests.get(url=url,params=data,headers=header)

        return res.json()

    def post(self, url, data, header):
        """

        :param url: 请求路由
        :param data: 请求参数
        :param header: 请求头
        :return:
        """
        if header is None:
            res = requests.post(url,data,verify=False)
        else:
            res = requests.get(url,data,headers=header,verify=False)

        return res.json()
    def send_request(self,**kwargs):
        cookie = {}
        session = requests.session()
        result = None
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie["Cookie"] = set_cookie
                self.read.write_yaml_data(set_cookie)
                logs.info(f"cookie：{cookie}")
            logs.info(f"接口实际返回信息：{result.text if result.text else result}")
        except requests.exceptions.ConnectionError:
            logs.error("接口连接服务器异常")
            pytest.fail("接口连接服务器异常")
        except requests.exceptions.HTTPError:
            logs.error("http异常")
            pytest.fail("http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail(e,"连接异常，请检查服务或数据是否正确")

        return result

    def run_main(self,name,url,case_name,headers,method,cookies=None,files=None,**kwargs):
        """

        :param name:
        :param url:
        :param case_name:
        :param header:
        :param method:
        :param cookies:
        :param file:
        :param kwargs:
        :return:
        """
        try:
            #日志收集信息
            logs.info(f"接口名称:{name}")
            logs.info(f"接口请求地址:{url}")
            logs.info(f"请求方法：{method}")
            logs.info(f"测试用例：{case_name}")
            logs.info(f"请求头：{headers}")
            logs.info(f"cookies :{cookies}")
            #处理请求参数
            res_params = json.dumps(kwargs,ensure_ascii=False)
            if "data" in kwargs.keys():
                allure.attach(res_params, f"接口请求信息：{res_params}", allure.attachment_type.TEXT)
                logs.info(f"请求参数：{kwargs}")
            if "json" in kwargs.keys():
                allure.attach(res_params, f"接口请求信息：{res_params}", allure.attachment_type.TEXT)
                logs.info(f"请求参数：{kwargs}")
            if "params" in kwargs.keys():
                allure.attach(res_params, f"接口请求信息：{res_params}", allure.attachment_type.TEXT)
                logs.info(f"请求参数：{kwargs}")
        except Exception as e:
            logs.error(e)
        response = self.send_request(url=url,headers=headers,method=method,cookies=None,files=None,verify=False,**kwargs)
        return response