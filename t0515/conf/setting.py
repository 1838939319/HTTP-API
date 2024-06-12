import os
import sys
import logging

DIR_PATH= os.path.dirname(os.path.dirname(__file__))


LOG_LEVE = logging.DEBUG#设置日志级别
STRAM_LOG_LEVE = logging.DEBUG# 输入日志到控制台

#文件路径
file_paths={
    "extract":os.path.join(DIR_PATH,"extract.yaml"),
    "conf": os.path.join(DIR_PATH,"conf","config.ini"),
    "LOG": os.path.join(DIR_PATH,"log")
}