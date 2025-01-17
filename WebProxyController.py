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


def run(device, log_file_path, task_page):
    device_id = device["id"]
    platform = device["platform"]
    print(device_id)

    handle_new_user = 0
    handle_existing_user = 0

    with open(log_file_path, "a") as log_file:
        try:

            if task_page == "chat":
                response = RequestsHandler.handle_chat_task(device_id)
            else:
                response = RequestsHandler.handle_quest_task(device_id)

            if response is None or response.status_code not in (200, 201):
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
            need_proxy = False

            log_file.write(f"task_id: {created_by_task_id}, platform: {platform}, new_count: {new_count}, "
                           f"existing_user_count: {existing_user_count}\n")

            if new_count > 0:
                for i in range(new_count):
                    if platform == "Chrome":
                        ChromeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                            new_users_events, device_id, created_by_task_id, False, need_proxy,
                                            task_page)
                    elif platform == "Firefox":
                        FirefoxProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                             new_users_events, device_id, created_by_task_id, need_proxy, task_page)
                    elif platform == "Edge":
                        EdgeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                          new_users_events, device_id, created_by_task_id, need_proxy, task_page)
                    elif platform == "Safari":
                        SafariProxy.run_new(new_users_target_urls, new_users_events, device_id, created_by_task_id,
                                            task_page)
                    else:
                        ChromeProxy.run_new(proxy_server, proxy_username, proxy_password, new_users_target_urls,
                                            new_users_events, device_id, created_by_task_id, False, need_proxy,
                                            task_page)
                    handle_new_user += 1

            if existing_user_count > 0:
                for i in range(existing_user_count):

                    existing_fb_user = existing_fb_users[i]

                    if platform == "Chrome":
                        ChromeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                 existing_users_target_urls, existing_users_events, need_proxy,
                                                 task_page)
                    elif platform == "Firefox":
                        FirefoxProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                  existing_users_target_urls, existing_users_events, need_proxy,
                                                  task_page)
                    elif platform == "Edge":
                        EdgeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                               existing_users_target_urls, new_users_events, need_proxy, task_page)
                    elif platform == "Safari":
                        SafariProxy.run_existing(existing_fb_user, existing_users_target_urls, existing_users_events,
                                                 task_page)
                    else:
                        ChromeProxy.run_existing(proxy_server, proxy_username, proxy_password, existing_fb_user,
                                                 existing_users_target_urls, existing_users_events, need_proxy,
                                                 task_page)
                    handle_existing_user += 1

            log_file.write(f"task_id: {created_by_task_id}, all done\n")
        except Exception as e:
            log_file.write(f"An error occurred: {e}\n")
            log_file.write(
                f"task_id: {created_by_task_id}, handle_new_user: {handle_new_user}, handle_existing_user: {handle_existing_user}\n")


# run(2)
# MacOS/Safari/Windows，如果是Safari，固定是9

if __name__ == "__main__":

    task_page = ""

    if len(sys.argv) > 1:
        task_page = sys.argv[1:][0]
        print("Command-line arguments:", task_page)
    else:
        print("No command-line arguments provided.")

    if task_page not in ("chat", "quest"):
        print("Only chat or quest")
        exit(0)

    fileName = LogUtils.get_log_filename()
    platform = "MacOS" if sys.platform == "darwin" else "Windows"
    device_list = []

    while True:
        if device_list is None or len(device_list) == 0:
            device_list = RequestsHandler.get_deviceid(platform)
        else:
            for device in device_list:
                result = run(device, fileName, task_page)

                if LogUtils.check_log_file_size(fileName):
                    fileName = LogUtils.get_log_filename()

                if result == 'skip':
                    continue
