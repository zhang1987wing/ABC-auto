import random

import ChromeProxy
import EdgeProxy
import FirefoxProxy
import RequestsHandler
import SafariProxy

def run(device_id):
    # 配置代理和用户信息

    #PROXY_SERVER = ["proxy.stormip.cn:1000", "us.stormip.cn:1000", "eu.stormip.cn:1000", "hk.stormip.cn:1000"]

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

    #PROXY_PASSWORD = "zs19974476"

    response = RequestsHandler.handle_task(device_id)

    if response.status_code not in (200, 201):
        return "skip"

    response_json = response.json()
    print(response_json)

    proxy_server = response_json["proxy"]["proxy_address"] + ":" + str(response_json["proxy"]["proxy_port"])
    #proxy_username = response["proxy_address"]
    proxy_password = response_json["proxy"]["proxy_password"]
    new_count = response_json["new_user_count"]
    existing_user_count = response_json["existing_user_count"]
    existing_fb_users = response_json["existing_fb_users"]
    target_url = response_json["target_urls"].split(";")[0]
    events = response_json["events"]
    created_by_task_id = response_json["id"]

    #random_server = random.choice(proxy_server)

    if new_count > 0:
        for i in range(new_count):
            if device_id in (1, 2, 3, 4):
                if device_id == 1:
                    PROXY_USERNAME = ["storm-shuaizhang4476"]
                elif device_id == 2:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-US"]
                elif device_id == 3:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-SG",
                      "storm-shuaizhang4476_area-JP",
                      "storm-shuaizhang4476_area-KR",
                      "storm-shuaizhang4476_area-VN"]
                else:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-RU",
                      "storm-shuaizhang4476_area-GB",
                      "storm-shuaizhang4476_area-DE"]

                ChromeProxy.run_new(proxy_server, random.choice(PROXY_USERNAME), proxy_password, target_url, events, device_id, created_by_task_id)
            else:
                if device_id == 1:
                    PROXY_USERNAME = ["storm-shuaizhang4476"]
                elif device_id == 2:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-US"]
                elif device_id == 3:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-SG",
                      "storm-shuaizhang4476_area-JP",
                      "storm-shuaizhang4476_area-KR",
                      "storm-shuaizhang4476_area-VN"]
                else:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-RU",
                      "storm-shuaizhang4476_area-GB",
                      "storm-shuaizhang4476_area-DE"]

                FirefoxProxy.run_new(proxy_server, random.choice(PROXY_USERNAME), proxy_password, target_url, events, device_id, created_by_task_id)

    ''' elif random_browser == 'firefox':
                    FirefoxProxy.run_new(proxy_server, random_username, proxy_password, target_url,
                                              events)
                else:
                    EdgeProxy.run_new(proxy_server, random_username, proxy_password, target_url,
                                           events)'''

    if existing_user_count > 0:
        for i in range(existing_user_count):
            if device_id in (1, 2, 3, 4):
                if device_id == 1:
                    PROXY_USERNAME = ["storm-shuaizhang4476"]
                elif device_id == 2:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-US"]
                elif device_id == 3:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-SG",
                                      "storm-shuaizhang4476_area-JP",
                                      "storm-shuaizhang4476_area-KR",
                                      "storm-shuaizhang4476_area-VN"]
                else:
                    PROXY_USERNAME = ["storm-shuaizhang4476_area-RU",
                                      "storm-shuaizhang4476_area-GB",
                                      "storm-shuaizhang4476_area-DE"]
                ChromeProxy.run_existing(proxy_server, random.choice(PROXY_USERNAME), proxy_password, existing_fb_users, target_url, events)
            else:
                FirefoxProxy.run_existing(proxy_server, random.choice(PROXY_USERNAME), proxy_password, existing_fb_users, target_url, events)

#run(2)

while True:
    for i in range(1, 9):
        result = run(i)

        if result == 'skip':
            continue

