import sys

import ChromeProxy
import EdgeProxy
import FirefoxProxy
import RequestsHandler
import SafariProxy

import LogUtils

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

    return proxy_username


def run(device, log_file_path):
    device_id = device["id"]
    platform = device["platform"]
    print(device_id)

    handle_new_user = 0
    handle_existing_user = 0

    with open(log_file_path, "a") as log_file:
        try:
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
            need_proxy = True

            log_file.write(f"task_id: {created_by_task_id}, platform: {platform}, new_count: {new_count}, existing_user_count: {existing_user_count}\n")

            if new_count > 0:
                for i in range(new_count):
                    if platform == "Chrome":
                        ChromeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                            new_users_events, device_id, created_by_task_id, False, need_proxy)
                    elif platform== "Firefox":
                        FirefoxProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                             new_users_events, device_id, created_by_task_id, need_proxy)
                    elif platform == "Edge":
                        EdgeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls, new_users_events,
                                          device_id, created_by_task_id, need_proxy)
                    elif platform == "Safari":
                        SafariProxy.run_new(new_users_target_urls, new_users_events, device_id, created_by_task_id)
                    else:
                        ChromeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                            new_users_events, device_id, created_by_task_id, False, need_proxy)
                    handle_new_user += 1

            if existing_user_count > 0:
                for i in range(existing_user_count):

                    existing_fb_user = existing_fb_users[i]

                    if platform == "Chrome":
                        ChromeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                 existing_users_target_urls, existing_users_events, need_proxy)
                    elif platform == "Firefox":
                        FirefoxProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                  existing_users_target_urls, existing_users_events, need_proxy)
                    elif platform == "Edge":
                        EdgeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                               existing_users_target_urls, new_users_events, need_proxy)
                    elif platform == "Safari":
                        SafariProxy.run_existing(existing_fb_user, existing_users_target_urls, existing_users_events)
                    else:
                        ChromeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                 existing_users_target_urls, existing_users_events, need_proxy)
                    handle_existing_user += 1

            log_file.write(f"task_id: {created_by_task_id}, all done\n")
        except Exception as e:
            log_file.write(f"An error occurred: {e}\n")
            log_file.write(f"task_id: {created_by_task_id}, handle_new_user: {handle_new_user}, handle_existing_user: {handle_existing_user}\n")

# run(2)
# MacOS/Safari/Windows，如果是Safari，固定是9

fileName = LogUtils.get_log_filename()
platform = "MacOS" if sys.platform == "darwin" else "Windows"

device_list = RequestsHandler.get_deviceid(platform)

while True:
    for device in device_list:
        result = run(device, fileName)

        if LogUtils.check_log_file_size(fileName):
            fileName = LogUtils.get_log_filename()

        if result == 'skip':
            continue