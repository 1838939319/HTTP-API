import configparser
from t0515.conf.setting import file_paths

class Operation:
    def __init__(self,file_path=None):
        if file_path is None:
            self.__file_path = file_paths["conf"]
        else:
            self.__file_path = file_path

        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path,encoding="utf-8")
        except Exception as e:
            print(e)

    def get_section_for_data(self,section,option):
        """

        :param section: 获取ini文件头部值
        :param option: 获取选项值的key
        :return:
        """
        try:
            data = self.conf.get(section,option)
            return data
        except Exception as e:
            print(e)
    #获取apienv下的值
    def get_apienv_data(self,option):
        return self.get_section_for_data("apievni",option)
        #获取mysql的配置信息
    def get_mysql_data(self,option):
        return self.get_section_for_data("MYSQL",option)




if __name__ == '__main__':
    oper = Operation()
    print(oper.get_apienv_data("host"))