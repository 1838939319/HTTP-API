import pytest
from t0515.common.readymal import get_testcase_yaml
from t0515.base.apiutil import BaseRequest
import allure

@allure.feature("获品列表")
@pytest.mark.unserManager
class TestLogin:
    @allure.story("获取商品列表")
    @pytest.mark.parametrize('params',get_testcase_yaml("./testcase/productManager/getProductList.yaml"))
    def test_case01(self,params):
         BaseRequest().specification_yaml(params)

    @allure.story("获取商品详情")
    @pytest.mark.parametrize('params', get_testcase_yaml("./testcase/productManager/productDetail"))
    def test_case02(self, params):
        BaseRequest().specification_yaml(params)
