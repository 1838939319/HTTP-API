import pytest
import os
import shutil

if __name__ == '__main__':
    pytest.main(['-s', '-v','-m unserManager', '--alluredir=./report/temp/', './testcase/', '--clean-alluredir'])
    shutil.copy("environment.xml", "./report/temp")
    os.system(f'allure serve ./report/temp')