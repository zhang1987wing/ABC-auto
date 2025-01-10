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

    try:

        # 发送 POST 请求
        response = requests.post(url, json=data, timeout=60)

        '''
        response = json.loads("{'id': 409, 'proxy': {'region': 'global', 'proxy_address': 'proxy.stormip.cn', 'proxy_port': 1000, 'proxy_username': 'storm-shuaizhang4476', "
                              "'proxy_password': 'zs19974476'}, 'new_users_target_urls': ['https://chat.sending.me/#/home', 'https://chat.sending.me/#/discover', "
                              "'https://chat.sending.me/#/room/!p13HU3XjRIXKGln2-@sdn_0ada666bc21e55ba55a5c36a7fe670c3b13b7579:0ada666bc21e55ba55a5c36a7fe670c3b13b7579'], "
                              "'existing_users_target_urls': ['https://chat.sending.me/#/room/!p13HU3XjRIXKGln2-@sdn_0ada666bc21e55ba55a5c36a7fe670c3b13b7579:0ada666bc21e55ba55a5c36a7fe670c3b13b7579', "
                              "'https://chat.sending.me/#/discover'], 'new_user_count': 2, 'existing_user_count': 0, 'existing_fb_users': [], 'new_users_events': "
                              "['register', 'register_success', 'login', 'login_success', 'set_user_name', 'set_user_name_success', 'onboarding_success', 'sync_start', 'sync_completed', "
                              "'read_message', 'room_join', 'room_join_success', 'send_message', 'send_message_success'], 'existing_users_events': ['sync_start', 'sync_completed', "
                              "'room_join', 'room_join_success', 'read_message', 'send_message', 'send_message_success']}")
                              '''

        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def handle_fb_user(device_id, cookie, created_by_task_id):
    # 设置请求的 URL 和参数
    url = 'https://luckycoin.im/growth-api/fb_user'

    # 需要发送的数据（字典格式）
    data = {
        "device_id": device_id,
        "data": cookie,
        "created_by_task_id": created_by_task_id
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, json=data, timeout=60)
        print(response.request.body)

        # 处理响应
        if response.status_code == 200 or response.status_code == 201:
            # 成功响应
            data = response.json()  # 假设返回的是 JSON 格式
            print(data)
        else:
            print(f"请求失败，状态码: {response.status_code}")

        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def get_deviceid(system):
    # 设置请求的 URL 和参数
    url = 'https://luckycoin.im/growth-api/device/list'

    try:
        # 发送 get 请求
        response = requests.get(url, timeout=60)
        device_list = []

        # 处理响应
        if response.status_code == 200:
            # 成功响应
            data = response.json()  # 假设返回的是 JSON 格式

            for system_info in data:

                if system_info["platform"] == system:
                    device_list.append(system_info)
                    break

                if system_info["host_os"] == system:
                    if system_info["platform"] == "Firefox":
                        # device_list.append(system_info)
                        continue
                    else:
                        device_list.append(system_info)

                    if system_info["platform"] in ["Safari", "Android", "iOS"]:
                        continue
                    else:
                        device_list.append(system_info)
                else:
                    continue
        else:
            print(f"请求失败，状态码: {response.status_code}")

        return device_list
    except Exception as e:
        print(f"请求失败: {e}")



# handle_fb_user(1, "_ga:GA1.1.1318980546.1734180344;_ga_HNRD6KMSBG:GS1.1.1734180344.1.0.1734180350.0.0.0", 1)
#get_deviceid("MacOS")
