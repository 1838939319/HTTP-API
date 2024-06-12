from t0515.conf import setting
import os
import time,logging
from logging.handlers import RotatingFileHandler


log_path = setting.file_paths['LOG']
if not os.path.exists(log_path):
    os.mkdir(log_path)
logfile_name = log_path+r"\test{}.log".format(time.strftime("%Y%m%d"))
print(logfile_name)
class Recodelog:
    """
    封装日志
    """

    def output_log(self):
        logger = logging.getLogger(__name__)#获取调用log的文件名
        #防止重复打印日志
        if not logger.handlers:
            logger.setLevel(setting.LOG_LEVE)
            log_format = logging.Formatter('%(levelname)s - %(asctime)s - %(filename)s -[%(module)s:%(funcName)s - %(message)s')
            #输出日志到指定文件
            fh = RotatingFileHandler(filename=logfile_name,mode="a",maxBytes=5242880,backupCount=7,encoding="utf-8")
            fh.setLevel(setting.LOG_LEVE)
            fh.setFormatter(log_format)
            #将相应的handler添加到logger
            logger.addHandler(fh)
            #将日志输出到控制台
            sh = logging.StreamHandler()
            sh.setFormatter(setting.STRAM_LOG_LEVE)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
        return logger

apilog = Recodelog()
logs = apilog.output_log()