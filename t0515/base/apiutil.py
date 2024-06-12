import re

from t0515.common.readymal import get_testcase_yaml,ReadYaml
from t0515.common.debugTalk import DebugTalk
from t0515.conf.operationConfig import Operation
from t0515.common.recodelog import logs
import allure
import  json
import jsonpath
from t0515.common.sendRequest import SendRequest
from t0515.common.assertions import Assertions

class BaseRequest:
    def __init__(self):
        self.read = ReadYaml()
        self.conf = Operation()
        self.send = SendRequest()
        self.ass = Assertions()

    def replace_load(self,data):
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)

        for i in range(str_data.count("${")):
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("${")
                end_index = str_data.index("}",start_index)
                ref_all_name = str_data[start_index:end_index+1]
                #获取方法名称
                func_name = ref_all_name[ref_all_name.index("{")+1:ref_all_name.index("(")]
                #获取参数
                func_params = ref_all_name[ref_all_name.index("(")+1:ref_all_name.index(")")]
                f = func_params.split(",")
                #替换
                extract_data = getattr(DebugTalk(),func_name)(*func_params.split(",") if func_params else "")
                str_data = str_data.replace(ref_all_name,str(extract_data))
        #数据还原
        if data and isinstance(data,dict):
            data = json.loads(str_data)

        else:
            data= str_data
        return data

    def specification_yaml(self,case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info:list类型
        :return:
        """
        cookies = None
        params_type = ['params','data','json']
        try:
            base_url = self.conf.get_apienv_data('host')
            url = base_url+case_info["baseInfo"]["url"]
            allure.attach(url,f"接口地址:{url}")
            api_name = case_info["baseInfo"]["api_name"]
            allure.attach(api_name,f"接口名称:{api_name}")
            method= case_info["baseInfo"]["method"]
            allure.attach(method,f"请求方式:{method}")
            header = case_info["baseInfo"]["header"]
            allure.attach(str(header),f"请求头：{header}",allure.attachment_type.TEXT)
            try:
                cookies = self.replace_load(case_info["baseInfo"]["cookies"])
                allure.attach(str(cookies),f"cookie:{cookies}",allure.attachment_type.TEXT)
            except:
                pass
            for tc in case_info['testCase']:
                case_name = tc.pop('case_name')
                allure.attach(case_name,f"测试用例名称：{case_name}")
                validation = tc.pop('validation')
                allure.attach(str(validation),f"预期断言结果",allure.attachment_type.TEXT)
                extract = tc.pop('extract',None) #存在则返回结果，不存在该字段则返回None
                extract_list = tc.pop('extract_list', None)


                for key,value in tc.items():
                    if key in params_type:
                        tc[key] = self.replace_load(value)
                res = self.send.run_main(name=api_name,url=url,case_name=case_name,headers=header,method=method,cookies=cookies,files=None,**tc)
                res_text = res.text
                allure.attach(res.text,f"接口响应信息：",allure.attachment_type.TEXT)
                allure.attach(str(res.status_code),f"接口响应状态：{res.status_code}",allure.attachment_type.TEXT)
                res_json = res.json()
                if extract is not None:
                    self.extract_data(extract,res_text)
                if extract_list is not None:
                    self.extract_data_list(extract_list,res_text)

                #处理接口断言
                self.ass.assert_result(validation,res_json,res.status_code)

        except Exception as e:
            logs.error(e)
            raise e
    def extract_data(self,testcase_extract,response):
        """
        提取接口的返回值，支持正则表达式提取及json提取
        :param testcase_extract:yaml文件中extract的值
        :param response:接口的响应信息
        :return:
        """
        try:
            parm_list=["(.*?)","(.+?)",r"(\d+)",r"(\d*)"]
            for key,value in testcase_extract.items():
                #处理正则表达式的数据
                for pat in parm_list:
                    if pat in value:
                        res_list = re.search(value,response)
                        if pat in [r"(\d+)",r"(\d*)"]:
                            extract_data = {key:int(res_list.group(1))}
                        else:
                            extract_data = {key: res_list.group(1)}
                        self.read.write_yaml_data(extract_data)

                #处理json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)[0]#将json转为字符格式后提取
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data={key:"未提取到json数据，返回数据为空"}
                    logs.info(f"json提取到的参数为：{extract_data}")
                    self.read.write_yaml_data(extract_data)
        except :
            logs.error("接口返回值提取异常，请检查yaml的extract数据是否正确。")
    def extract_data_list(self,testcase_extract_list,response):
        """
        提取接口的返回值，支持正则表达式提取及json提取
        :param testcase_extract:yaml文件中extract_list的值,结果以列表形式返回
        :param response:接口的响应信息
        :return:
        """
        try:
            for key,value in testcase_extract_list.items():
                #处理正则表达式的数据
                if "(.*?)" in value or  "(.+?)" in value:
                    res_list = re.findall(value,response,re.S)
                    if res_list:
                        extract_data = {key: res_list}
                        logs.info(f"正则表达式提取到的参数为：{extract_data}")
                        self.read.write_yaml_data(extract_data)

                #处理json提取器
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response),value)#将json转为字符格式后提取
                    if ext_json:
                        extract_data = {key:ext_json}
                    else:
                        extract_data={key:"未提取到json数据，返回数据为空"}
                    logs.info(f"json提取到的参数为：{extract_data}")
                    self.read.write_yaml_data(extract_data)
        except :
            logs.error("接口返回值提取异常，请检查yaml的extract数据是否正确。")




if __name__ == '__main__':
    data = get_testcase_yaml("../testcase/Login/login.yaml")[0]
    print(data)
    base = BaseRequest()
    # result = base.replace_load(data)
    # print(result)
    # d = DebugTalk()
    # d.get_extract_data("token")
    res = base.specification_yaml(data)
    print(res)