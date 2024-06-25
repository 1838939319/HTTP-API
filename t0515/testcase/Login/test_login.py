import pytest
from t0515.common.readymal import get_testcase_yaml
from t0515.base.apiutil import BaseRequest
import allure

@allure.feature("用户登录接口")
class TestLogin:
    @allure.story("正确用户名和密码校验")
    @pytest.mark.parametrize("base_info,test_case",get_testcase_yaml("./testcase/Login/login.yaml"))
    def test_case01(self,base_info,test_case):
        allure.dynamic.title(base_info["case_name"])
        BaseRequest().specification_yaml(base_info,test_case)

    # @allure.story("错误用户名和密码校验")
    # @pytest.mark.parametrize('params', get_testcase_yaml("./testcase/Login/login.yaml"))
    # def test_case02(self, params):
    #     BaseRequest().specification_yaml(params)

    # def test_case02(self):
    #     print("22222222")
    #
    # def test_case03(self,function_test):
    #     print("33333333")
    #     print(function_test)
#
# if __name__ == '__main__':
#     pytest.main()