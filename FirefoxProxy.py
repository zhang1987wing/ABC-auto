import random
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pyautogui

import ReadCookie
import RequestsHandler
import Utils


def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events):
    # Firefox 浏览器选项
    global events_str
    firefox_options = Options()

    # 设置代理
    firefox_options.set_preference("network.proxy.type", 1)  # 1表示手动设置代理
    firefox_options.set_preference("network.proxy.http", PROXY_SERVER.split(':')[0])  # HTTP 代理地址
    firefox_options.set_preference("network.proxy.http_port", int(PROXY_SERVER.split(':')[1]))  # HTTP 代理端口
    firefox_options.set_preference("network.proxy.ssl", PROXY_SERVER.split(':')[0])  # SSL 代理地址
    firefox_options.set_preference("network.proxy.ssl_port", int(PROXY_SERVER.split(':')[1]))  # SSL 代理端口
    firefox_options.set_preference("network.proxy.ftp", PROXY_SERVER.split(':')[0])  # FTP 代理地址
    firefox_options.set_preference("network.proxy.ftp_port", int(PROXY_SERVER.split(':')[1]))  # FTP 代理端口
    firefox_options.set_preference("network.proxy.socks", PROXY_SERVER.split(':')[0])  # SOCKS 代理地址
    firefox_options.set_preference("network.proxy.socks_port", int(PROXY_SERVER.split(':')[1]))  # SOCKS 代理端口
    firefox_options.set_preference("network.proxy.share_proxy_settings", True)
    firefox_options.set_preference("javascript.enabled", True)  # 启用 JavaScript

    # 初始化 Firefox 浏览器
    driver = webdriver.Firefox(options=firefox_options)

    try:
        time.sleep(5)
        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(PROXY_USERNAME)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        # 设置用户行为
        events_str = ','.join(events)

        driver.add_cookie({
            'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
            'value': events_str
        })

        # 设置一个用户
        for existing_fb_user in existing_fb_users:

            # 清除用户Cookies
            driver.delete_cookie("_ga")
            driver.delete_cookie("_ga_822RN0ZE72")

            # random_cookie = random.choice(existing_fb_users)

            cookies = [{
                'name': existing_fb_user.split(';')[0].split(':')[0],
                'value': existing_fb_user.split(';')[0].split(':')[1],
            }, {
                'name': existing_fb_user.split(';')[1].split(':')[0],
                'value': existing_fb_user.split(';')[1].split(':')[1],
            }]
            for cookie in cookies:
                driver.add_cookie(cookie)

            # 确认是否已成功添加Cookie
            cookies = driver.get_cookies()
            print(cookies)  # 打印所有当前的Cookies

            for target_url in target_urls:
                time.sleep(random.randint(6, 10))

                # 循环访问页面
                i = 1
                while i < 2:
                    # 访问目标URL
                    driver.get(target_url)
                    print(target_url)

                    i += 1

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id):
    global events_str

    # Firefox 浏览器选项
    firefox_options = Options()

    # 设置代理
    firefox_options.set_preference("network.proxy.type", 1)  # 1表示手动设置代理
    firefox_options.set_preference("network.proxy.http", PROXY_SERVER.split(':')[0])  # HTTP 代理地址
    firefox_options.set_preference("network.proxy.http_port", int(PROXY_SERVER.split(':')[1]))  # HTTP 代理端口
    firefox_options.set_preference("network.proxy.ssl", PROXY_SERVER.split(':')[0])  # SSL 代理地址
    firefox_options.set_preference("network.proxy.ssl_port", int(PROXY_SERVER.split(':')[1]))  # SSL 代理端口
    firefox_options.set_preference("network.proxy.ftp", PROXY_SERVER.split(':')[0])  # FTP 代理地址
    firefox_options.set_preference("network.proxy.ftp_port", int(PROXY_SERVER.split(':')[1]))  # FTP 代理端口
    firefox_options.set_preference("network.proxy.socks", PROXY_SERVER.split(':')[0])  # SOCKS 代理地址
    firefox_options.set_preference("network.proxy.socks_port", int(PROXY_SERVER.split(':')[1]))  # SOCKS 代理端口
    firefox_options.set_preference("network.proxy.share_proxy_settings", True)
    firefox_options.set_preference("javascript.enabled", True)  # 启用 JavaScript

    # 初始化 Firefox 浏览器
    driver = webdriver.Firefox(options=firefox_options)

    try:
        time.sleep(3)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(PROXY_USERNAME)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")

        time.sleep(0.5)

        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        # 清除用户数据
        driver.delete_cookie("_ga")
        driver.delete_cookie("_ga_822RN0ZE72")

        # 设置用户行为
        events_str = ','.join(events)
        cookies = [{
            'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
            'value': events_str
        }]

        for cookie in cookies:
            driver.add_cookie(cookie)

        cookies = driver.get_cookies()
        print(cookies)  # 打印所有当前的Cookies

        time.sleep(5)

        for target_url in target_urls:
            time.sleep(random.randint(6, 10))

            # 循环访问页面
            i = 1

            while i < 2:
                # 访问目标URL
                driver.get(target_url)
                print(target_url)

                i += 1

        time.sleep(5)
        cookies = driver.get_cookies()
        print(cookies)  # 打印所有当前的Cookies

        cookie_string = ";".join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies if
                                  cookie['name'] in ['_ga', '_ga_822RN0ZE72']])
        if cookie_string != "":
            RequestsHandler.handle_fb_user(device_id, cookie_string, created_by_task_id)

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

#run_new("proxy.stormip.cn:1000", "storm-shuaizhang4476", "zs19974476", [], [], 1, 1)