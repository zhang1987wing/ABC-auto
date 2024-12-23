import random
import time
from selenium import webdriver
import subprocess

import RequestsHandler
import Utils


def run_existing(existing_fb_users, target_urls, events):

    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
        # 打开目标网址
        driver.get("https://myip.ipip.net")
        time.sleep(2)

        # 循环访问页面
        i = 1

        target_url_list = Utils.handle_target_url(target_urls)
        for target_url in target_url_list:
            time.sleep(random.randint(1, 10))

            while i < 4:
                # 清除所有Cookies
                driver.delete_all_cookies()

                # 访问目标URL
                driver.get(target_url)
                print(target_url)

                # 设置一个Cookie
                random_cookie = random.choice(existing_fb_users)
                events_str = ','.join(events)

                cookies = [{
                    'name': random_cookie["data"].split(';')[0].split(':')[0],
                    'value': random_cookie["data"].split(';')[0].split(':')[1],
                }, {
                    'name': random_cookie["data"].split(';')[1].split(':')[0],
                    'value': random_cookie["data"].split(';')[1].split(':')[1],
                }, {
                    'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
                    'value': events_str
                }]

                for cookie in cookies:
                    driver.add_cookie(cookie)

                # 确认是否已成功添加Cookie
                cookies = driver.get_cookies()
                print(cookies)  # 打印所有当前的Cookies

                i += 1
                time.sleep(5)

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

def run_new(target_urls, events, device_id, created_by_task_id):
    global events_str

    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
        # 打开目标网址
        driver.get("https://myip.ipip.net")
        time.sleep(2)

        # 循环访问页面
        i = 1

        target_url_list = Utils.handle_target_url(target_urls)
        for target_url in target_url_list:
            time.sleep(random.randint(1, 10))

            while i < 2:
                # 清除所有Cookies
                driver.delete_all_cookies()

                # 访问目标URL
                driver.get(target_url)
                print(target_url)

                time.sleep(5)

                cookies = driver.get_cookies()
                print(cookies)  # 打印所有当前的Cookies

                cookie_string = ";".join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies if
                                          cookie['name'] in ['_ga', '_ga_HNRD6KMSBG']])

                RequestsHandler.handle_fb_user(device_id, cookie_string, created_by_task_id)

                #设置event
                events_str = ','.join(events)

                cookies = [{
                    'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
                    'value': events_str
                }]

                for cookie in cookies:
                    driver.add_cookie(cookie)

                # 确认是否已成功添加Cookie
                cookies = driver.get_cookies()
                print(cookies)  # 打印所有当前的Cookies

                time.sleep(3)

                i += 1

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()