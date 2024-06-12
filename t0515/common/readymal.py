#coding: utf-8

import yaml
import os
from t0515.conf.setting import file_paths

def get_testcase_yaml(file):
    """
    获取yaml文件的数据
    :param file: yaml文件的路径
    :return:
    """
    try:
        with open(file,'r',encoding='utf-8')as f:
            yaml_data=yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(e)

class ReadYaml:
    def __init__(self,yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = "../testcase/Login/login.yaml"

    def write_yaml_data(self,value):
        """
        写入yaml数据到文件
        :param value:
        :return:
        """
        try:
            file_path= file_paths["extract"]
            if not os.path.exists(file_path):
                os.system(file_path)
            file = open(file_path,"a",encoding="utf-8")
            if isinstance(value,dict):
                write_data=yaml.dump(value,allow_unicode=True,sort_keys=False)
                file.write(write_data)
            else:
                print(
                    "写入数据必须为字典类型"
                )
        except Exception as e:
            print(e)
        finally:
            file.close()

    def get_extract_yaml(self,node_name):
        """
        读取接口的变量值
        :param node_name: yaml的key值
        :return:
        """
        file_path = file_paths["extract"]
        if os.path.exists(file_path):
            print("文件已存在")
        else:
            print("extract.yaml不存在")
            file = open(file_path, "w")
            file.close()
            print("extract.yaml创建成功")
        with open(file_path, "r", encoding="utf-8")as f:
            extract_data=yaml.safe_load(f)
            print(extract_data)
        return extract_data[node_name]

    def clear_yaml_data(self):
        """
        清楚extract.yaml文件中的数据
        :return:
        """
        with open(file_paths["extract"],"w") as f:
            f.truncate()




if __name__ == '__main__':
    res = get_testcase_yaml('../testcase/Login/login.yaml')
#     # url = res['baseInfo']['url']
#     # new_url="http://127.0.0.1:8787"+url
#     # methond = res['baseInfo']['method']
#     # data = res['testCase'][0]['data']
#     header = res['baseInfo']['header']
#     # s= SendRequest()
#     # res1 = s.run_main(url=new_url,data=data,header=header,method=methond)
#     #
    print(res)
#     # print(header)
#     # print(methond)
#     d = ReadYaml()
#     new_data={}
#     new_data["header"]=header
#     # d.write_yaml_data(new_data)
#     d.get_extract_yaml("token")