import csv
from  t0515.common.recodelog import logs
from t0515.conf.setting import DIR_PATH
import os


def get_csv_data(file_name):
    lis1 = []
    try:
        with open(os.path.join(DIR_PATH,"data",file_name)) as f:
            csv_result = csv.reader(f)
            for i in csv_result:
                lis1.append(i)
            return lis1
    except Exception as e:
        logs.error(e)

if __name__ == '__main__':
    print(get_csv_data("test.csv"))
