import sys
import time
from selenium import webdriver

import RequestsHandler
import WebProxy


def run_existing(existing_fb_user, target_urls, events, task_page):
    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
        # 打开目标网址
        if task_page == "chat":
            driver.get("https://chat.sending.me/abc.html")
        else:
            driver.get("https://quest.sending.me/abc.html")

        time.sleep(2)

        WebProxy.handle_existing(driver, existing_fb_user, target_urls, events)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()


def run_new(target_urls, events, device_id, created_by_task_id, task_page):
    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
        # 打开目标网址
        if task_page == "chat":
            driver.get("https://chat.sending.me/abc.html")
        else:
            driver.get("https://quest.sending.me/abc.html")

        time.sleep(2)

        WebProxy.handle_newuser(driver, target_urls, events, device_id, created_by_task_id, task_page)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()


def controller(device_id, need_proxy):
    response = RequestsHandler.handle_task(device_id)

    if response.status_code not in (200, 201):
        return "skip"

    response_json = response.json()
    print(response_json)

    new_count = response_json["new_user_count"]
    existing_user_count = response_json["existing_user_count"]
    existing_fb_users = response_json["existing_fb_users"]
    new_users_target_urls = response_json["new_users_target_urls"]
    existing_users_target_urls = response_json["existing_users_target_urls"]
    new_users_events = response_json["new_users_events"]
    existing_users_events = response_json["existing_users_events"]
    created_by_task_id = response_json["id"]

    if new_count > 0:
        for i in range(new_count):
            run_new(new_users_target_urls, new_users_events, device_id, created_by_task_id)

    if existing_user_count > 0:
        for i in range(existing_user_count):
            existing_fb_user = existing_fb_users[i]

            run_existing(existing_fb_users, existing_users_target_urls, existing_fb_user)


if __name__ == "__main__":

    device_id = 0

    if len(sys.argv) > 1:
        device_id = int(sys.argv[1:][0])
        print("Command-line arguments:", device_id)

        while True:
            result = controller(device_id, False)

            if result == 'skip':
                continue
    else:
        print("No command-line arguments provided.")
