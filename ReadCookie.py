import csv
import random

mock_user=[{'GA':'GA1.1.1318980546.1734180344','GS':'GS1.1.1734180344.1'},
           {'GA':'GA1.1.541331381.1734180353','GS':'GS1.1.1734180352.1'},
           {'GA':'GA1.1.225438254.1734180363','GS':'GS1.1.1734180362.1'},
           {'GA':'GA1.1.962964952.1734180372','GS':'GS1.1.1734180371.1'},
           {'GA':'GA1.1.728492228.1734180380','GS':'GS1.1.1734180380.1'},]

def read_file(filepath):
    # 打开并读取CSV文件
    with open(filepath, mode='r') as csvfile:
        #reader = list(csv.DictReader(csvfile))   # 使用DictReader，以便按列名访问数据

        # 随机选择一行数据
        random_row = random.choice(mock_user)
        return random_row


def read_firefox_cookie():
    return read_file("firefox-cookie.csv")
