from t0515.common.readymal import ReadYaml
import random
class DebugTalk:
    def __init__(self):
        self.read = ReadYaml()

    def get_extract_order_data(selfd,data,ranodms):
        if ranodms not in [0,-1,-2]:
            return data[int(ranodms)-1]

    def get_extract_data_list(self,node_name,randoma=None):
        """
        :param node_name: yaml中的key值
        :param sec_node_name:yaml中的key值
        :param random: 随机读取yaml文件中的数据,0>随机读取，-1全部读取
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        print(data)
        if randoma is not None:
            randoma = int(randoma)
            data_value = {
                randoma: self.get_extract_order_data(data, randoma),
                0: random.choice(data),
                -1: ",".join(data)

            }
            data = data_value[randoma]
        return data

    def get_extract_data(self,node_name,sec_node_name=None):
        """

        :param node_name: yaml中的key值
        :param sec_node_name:yaml中的key值
        :param random: 随机读取yaml文件中的数据
        :return:
        """
        data = self.read.get_extract_yaml(node_name)
        res_data = data
        if sec_node_name is not None:
            res_data = data[sec_node_name]

        return res_data





    def md5_parms(self,parmas):
        pass

if __name__ == '__main__':
        debug = DebugTalk()
        print(debug.get_extract_data("token"))