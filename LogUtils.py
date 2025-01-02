import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

# 设置文件大小限制 (例如: 5 MB)
MAX_LOG_SIZE = 10 * 1024 * 1024  # 5 MB
LOG_DIR = "logs"  # 存放日志文件的目录

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)

# 判断文件大小是否超过限制
def check_log_file_size(file_path):
    return os.path.getsize(file_path) >= MAX_LOG_SIZE

# 获取日志文件的路径
def get_log_filename():
    log_files = [f for f in os.listdir(LOG_DIR) if f.startswith("selenium_log")]
    if log_files:
        log_files.sort(key=lambda x: int(re.search(r'(\d+)', x).group(0)), reverse=True)  # 按文件名排序，找到最新的日志文件
        last_log_file = log_files[0]
        index = int(last_log_file.split('_')[-1].split('.')[0])
        return os.path.join(LOG_DIR, f"selenium_log_{index + 1}.txt")
    else:
        return os.path.join(LOG_DIR, "selenium_log_1.txt")

def test(log_file_path):
    with open(log_file_path, "a") as log_file:
        try:
            x = 1 / 0  # 故意制造错误
        except Exception as e:
            log_file.write(f"An error occurred: {e}\n")
