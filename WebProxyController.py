import random

import ChromeProxy
import EdgeProxy
import FirefoxProxy
import RequestsHandler
import SafariProxy

# 配置代理和用户信息
'''
PROXY_SERVER = ["proxy.stormip.cn:1000", "us.stormip.cn:1000", "eu.stormip.cn:1000", "hk.stormip.cn:1000"]
PROXY_USERNAME = ["storm-shuaizhang4476",
                      #美国
                      "storm-shuaizhang4476_area-US",
                      #欧洲
                      "storm-shuaizhang4476_area-RU",
                      "storm-shuaizhang4476_area-GB",
                      "storm-shuaizhang4476_area-DE",
                      #亚洲
                      "storm-shuaizhang4476_area-SG",
                      "storm-shuaizhang4476_area-JP",
                      "storm-shuaizhang4476_area-KR",
                      "storm-shuaizhang4476_area-VN"]

#PROXY_PASSWORD = "zs19974476"'''


def get_proxy_username(device_id):
    proxy_username = ''

    if device_id in (1, 5):
        proxy_username = ["storm-shuaizhang4476"]
    elif device_id in (2, 6):
        proxy_username = ["storm-shuaizhang4476_area-US"]
    elif device_id(3, 7):
        proxy_username = ["storm-shuaizhang4476_area-SG",
                          "storm-shuaizhang4476_area-JP",
                          "storm-shuaizhang4476_area-KR",
                          "storm-shuaizhang4476_area-VN"]
    elif device_id in (4, 8):
        proxy_username = ["storm-shuaizhang4476_area-RU",
                          "storm-shuaizhang4476_area-GB",
                          "storm-shuaizhang4476_area-DE"]
    else:
        proxy_username = ["storm-shuaizhang4476"]

    return proxy_username;


def run(device_id):
    response = RequestsHandler.handle_task(device_id)

    if response.status_code not in (200, 201):
        return "skip"

    response_json = response.json()
    print(response_json)

    proxy_server = response_json["proxy"]["proxy_address"] + ":" + str(response_json["proxy"]["proxy_port"])
    proxy_username = response_json["proxy"]["proxy_username"]
    proxy_password = response_json["proxy"]["proxy_password"]
    new_count = response_json["new_user_count"]
    existing_user_count = response_json["existing_user_count"]
    existing_fb_users = response_json["existing_fb_users"]
    new_users_target_urls = response_json["new_users_target_urls"]
    existing_users_target_urls = response_json["existing_users_target_urls"]
    new_users_events = response_json["new_users_events"]
    existing_users_events = response_json["existing_users_events"]
    created_by_task_id = response_json["id"]

    # random_server = random.choice(proxy_server)

    if new_count > 0:
        for i in range(new_count):
            if device_id in (1, 2, 3, 4):
                ChromeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                    new_users_events, device_id, created_by_task_id)
            elif device_id in (5, 6, 7, 8):
                FirefoxProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                     new_users_events, device_id, created_by_task_id)
            else:
                SafariProxy.run_new(new_users_target_urls, new_users_events, device_id, created_by_task_id)

    if existing_user_count > 0:
        for i in range(existing_user_count):
            if device_id in (1, 2, 3, 4):
                ChromeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_users,
                                         existing_users_target_urls, existing_users_events)
            elif device_id in (5, 6, 7, 8):
                FirefoxProxy.run_new(proxy_server, proxy_username, proxy_password, existing_users_target_urls,
                                     existing_users_events,
                                     device_id, created_by_task_id)
            else:
                SafariProxy.run_new(existing_users_target_urls, existing_users_events, device_id, created_by_task_id)


# run(2)

while True:
    for i in range(1, 9):
        result = run(i)

        if result == 'skip':
            continue
