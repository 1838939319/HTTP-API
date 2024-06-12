import os
import allure
from t0515.common.recodelog import logs
import jsonpath,operator
from t0515.common.connection import ConnectMysql

class Assertions:
    """
    断言接口断言模式封装
    1. 字符串包含
    2. 结果相等断言
    3. 结果不相等断言
    4. 断言接口返回值中的任何一个值
    5. 数据库断言
    """

    def contians_assert(self,value,response,status_code):
        """
        字符串包含断言，断言预期结果的字符串是否包含在实际接口的返回值中
        :param value:预期结果：yaml文件中validation关键字的结果
        :param response:
        :param status_code:
        :return:
        """
        #断言状态标识，0代表成功，其他代表失败
        flag = 0
        for assert_key,assert_values in value.items():
            # print(assert_key,assert_values)
            if assert_key == "status_code":
                if assert_values!=status_code:
                    flag +=1
                    logs.error("contains断言失败，接口返回码【%s】不等于【%s】"%(status_code,assert_values))
                    allure.attach(f"预期结果{status_code}\n实际结果{assert_values}，代码响应结果：失败",'contains断言失败结果',allure.attachment_type.TEXT)
            else:
                res_list = jsonpath.jsonpath(response,"$.%s"%(assert_key))
                if isinstance(res_list[0],str):
                    resp_list = "".join(res_list)
                    if resp_list:
                        if assert_values in resp_list:
                            logs.info("字符串包含断言成功：，预期结果【%s】，实际结果【%s】"%(resp_list,assert_values))
                            allure.attach(f"预期结果{res_list}\n实际结果{assert_values}，校验结果：成功",'contains断言成功结果',allure.attachment_type.TEXT)
                        else:
                            flag+=1
                            logs.error("contains断言失败，预期结果【%s】，实际结果【%s】"%(resp_list,assert_values))
                            allure.attach(f"预期结果{res_list}\n实际结果{assert_values}，代码响应结果：失败",'contains断言失败结果',allure.attachment_type.TEXT)
            return flag
    def equla_assert(self,value,response):
        """
        相等断言
        :param value:预期结果，也就是yaml文件中validation关键字下的参数，必须为dict类型
        :param response:接口实际返回值，必须为dict类型
        :return:flag标识，0为测试通过，其他值为不通过
        """
        flag = 0
        res_list = []
        #处理实际结果的数据结果，与预期结果的数据结构保持一致
        if isinstance(value,dict) and isinstance(response,dict):
            for res in response:
                if list(value.keys())[0] != res:
                    res_list.append(res)
            for rl in res_list:  #处理实际结果，过滤相关的数据信息获得需要校验的数据
                del response[rl]
            #判断实际结果与预期结果的值
            equal_result = operator.eq(value,response)
            if equal_result:
                logs.info(f"相等断言成功，预期结果{value},等于实际结果{response}")
                allure.attach(f"相等断言成功，预期结果{value},等于实际接口返回结果{response}", 'eq断言响应结果', allure.attachment_type.TEXT)
            else:
                flag = flag+1
                logs.info(f"相等断言失败，预期结果{value},不等于实际结果{response}")
                allure.attach(f"相等断言失败，预期结果{value}\n不等于实际结果{response}","eq断言结果",allure.attachment_type.TEXT)
        else:
            raise TypeError("相等断言失败，预期结果和接口的实际响应结果必须为字典类型")
        return flag

    def not_equla_assert(self,value,response):
        """
        不相等断言
        :param value:预期结果，也就是yaml文件中validation关键字下的参数，必须为dict类型
        :param response:接口实际返回值，必须为dict类型
        :return:flag标识，0为测试通过，其他值为不通过
        """
        flag = 0
        res_list = []
        #处理实际结果的数据结果，与预期结果的数据结构保持一致
        if isinstance(value,dict) and isinstance(response,dict):
            for res in response:
                if list(value.keys())[0] != res:
                    res_list.append(res)
            for rl in res_list:  #处理实际结果，过滤相关的数据信息获得需要校验的数据
                del response[rl]
            #判断实际结果与预期结果的值
            equal_result = operator.ne(value,response)
            if equal_result:
                logs.info(f"不相等断言成功，预期结果{value},不等于实际接口返回结果{response}")
                allure.attach(f"不相等断言成功，预期结果{value},不等于实际接口返回结果{response}",'ne断言响应结果',allure.attachment_type.TEXT)
            else:
                flag = flag+1
                logs.info(f"不相等断言失败，预期结果{value},等于实际结果{response}")
                allure.attach(f"不相等断言失败，预期结果{value},等于实际接口返回结果{response}", 'ne断言响应结果', allure.attachment_type.TEXT)
        else:
            raise TypeError("不相等断言失败，预期结果和接口的实际响应结果必须为字典类型")
        return flag

    def assert_response_any(self,actual_results,expected_results):
        """
        断言接口响应中body的任何属性值
        :param actual_results:接口实际相应信息
        :param expected_results:预期结果，在接口返回值的任意值
        :return:
        """
        flag= 0
        try:
            exp_key =  list(expected_results.keys())[0]
            if exp_key in actual_results:
                exp_values = actual_results[exp_key]
                rv_result = operator.eq(exp_values,list(expected_results.valuse())[0])
                if rv_result:
                    logs.info("结果响应任意值断言成功")
                else:
                    flag += 1
                    logs.info("结果响应任意值断言失败")
        except Exception as e:
            logs.info(e)
            raise
        return flag
    #数据库断言
    def assert_mysql(self,expecte_mysql):
        """

        :param expecte_mysql: 预期结果，也就是yaml文件中的sql
        :param actual_results:
        :return:返回flag标识，0为通过，其他为失败
        """
        conn = ConnectMysql()
        flag = 0
        db_value = conn.query(expecte_mysql)
        if dict is not None:
            logs.info("数据库断言成功")
        else:
            logs.error("数据库断言失败")
            flag = flag+1
        return flag



    def assert_result(self,expected,response,status_code):
        """
        断言模式，通过all_flag标记
        :param expected:预期结果
        :param response:响应结果,必须为json格式
        :param status_code:状态码
        :return:
        """
        try:
            all_flag = 0
            for yq in expected:
                for key, value in yq.items():
                    if key =="contains":
                        flag = self.contians_assert(value,response,status_code)
                        all_flag = all_flag+flag
                    elif key == "eq":
                        flag = self.equla_assert(value,response)
                        all_flag = all_flag+flag
                    elif key == "ne":
                        flag = self.not_equla_assert(value,response)
                        all_flag = all_flag+flag
                    elif key == "any":
                        flag = self.assert_response_any(response,value)
                        all_flag = all_flag + flag
                    elif key == "db":
                        flag = self.assert_mysql(expected_sql)

            assert all_flag==0
            logs.info("测试成功")

        except Exception as e:
            logs.error("测试失败",e)
            assert all_flag==0




#
# if __name__ == '__main__':
#     from t0515.common.readymal import get_testcase_yaml
#     data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)),r'testcase/Login','login.yaml'))[0]
#     value = data["testCase"][0]['validation']
#     response={
#         "error_code": None,
#         "msg": "登陆成功",
#         "msg_code": 200,
#         "token": "0F59AB8e0DB48d69b0E8a7B69CB4F"
#     }
#     ass = Assertions()
#     for i in value:
#         # print(value)
#         for keys,values in i.items() :
#             # print(i)
#             # print(values)
#             ass.not_equla_assert(values,response)
#     # ass.equla_assert(value,response)
