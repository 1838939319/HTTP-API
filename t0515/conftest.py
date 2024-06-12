import pytest
from t0515.common.recodelog import logs
from t0515.common.readymal import ReadYaml

read = ReadYaml()

@pytest.fixture(scope="session",autouse=True)
def clear_extarct_data():
    read.clear_yaml_data()

@pytest.fixture(scope="function",autouse=True)
def function_test():
    logs.info("-----------接口开始执行----------")
    yield
    logs.info("------------接口执行结束-----------")

