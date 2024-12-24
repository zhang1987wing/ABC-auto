import json
import logging
import random

import requests

# 设置日志配置
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# 创建一个HTTP请求的处理器
http_handler = logging.StreamHandler()
http_handler.setLevel(logging.DEBUG)

# 请求日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
http_handler.setFormatter(formatter)

# 将处理器添加到logger
logger.addHandler(http_handler)

# 配置requests的日志级别为DEBUG
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.addHandler(http_handler)


def handle_task(device_id):
    # 设置请求的 URL 和参数
    url = 'https://luckycoin.im/growth-api/task'

    # 需要发送的数据（字典格式）
    data = {
        'device_id': device_id
    }

    # 发送 POST 请求
    response = requests.post(url, json=data)

    '''
    response = json.loads(
        '{"id": 3,"proxy": {"region": "global","proxy_address": "proxy.stormip.cn","proxy_port": 1000,'
        '"proxy_username": "storm-shuaizhang4476","proxy_password": "zs19974476"},"target_urls": '
        '"https://fb-test-sd.vercel.app;","new_user_count": 100,"existing_user_count": 0,"existing_fb_users": '
        '[{"data":"_GA:GA1.1.1318980546.1734180344;_ga_HNRD6KMSBG:GS1.1.1734180344.1"},{"data":"_GA:GA1.1.541331381.1734180353;'
        '_ga_HNRD6KMSBG:GS1.1.1734180352.1"}],"events": ["sync","send_message"]}')'''

    return response


def handle_fb_user(device_id, cookie, created_by_task_id):
    # 设置请求的 URL 和参数
    url = 'https://luckycoin.im/growth-api/fb_user'

    # 需要发送的数据（字典格式）
    data = {
        "device_id": device_id,
        "data": cookie,
        "created_by_task_id": created_by_task_id
    }

    # 发送 POST 请求
    response = requests.post(url, json=data)
    print(response.request.body)

    # 处理响应
    if response.status_code == 200 or response.status_code == 201:
        # 成功响应
        data = response.json()  # 假设返回的是 JSON 格式
        print(data)
    else:
        print(f"请求失败，状态码: {response.status_code}")

    return data

#handle_fb_user(1, "_ga:GA1.1.1318980546.1734180344;_ga_HNRD6KMSBG:GS1.1.1734180344.1.0.1734180350.0.0.0", 1)
