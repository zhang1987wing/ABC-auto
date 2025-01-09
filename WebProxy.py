import random
import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.firefox.options import Options

import RequestsHandler
import Utils


def handle_newuser(driver, target_urls, events, device_id, created_by_task_id):
    # 清除用户数据
    driver.delete_cookie("_ga")
    driver.delete_cookie("_ga_822RN0ZE72")

    # 设置用户行为
    cookies = [{
        'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
        'value': ','.join(events)
    }]

    for cookie in cookies:
        driver.add_cookie(cookie)

    cookies = driver.get_cookies()
    print(cookies)  # 打印所有当前的Cookies

    time.sleep(5)

    for target_url in target_urls:

        time.sleep(random.randint(1, 3))

        driver.get(target_url)
        print(target_url)

    time.sleep(5)
    cookies = driver.get_cookies()
    print(cookies)  # 打印所有当前的Cookies

    cookie_string = ";".join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies if
                              cookie['name'] in ['_ga', '_ga_822RN0ZE72']])
    if cookie_string != "":
        time.sleep(20)
        RequestsHandler.handle_fb_user(device_id, cookie_string, created_by_task_id)

def handle_existing(driver, existing_fb_users, target_urls, events):

    # 设置用户行为
    driver.add_cookie({
        'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
        'value': ','.join(events)
    })

    # 设置一个用户
    for existing_fb_user in existing_fb_users:

        # 清除用户Cookies
        driver.delete_cookie("_ga")
        driver.delete_cookie("_ga_822RN0ZE72")

        cookies = [{
            'name': existing_fb_user['data'].split(';')[0].split(':')[0],
            'value': existing_fb_user['data'].split(';')[0].split(':')[1],
        }, {
            'name': existing_fb_user['data'].split(';')[1].split(':')[0],
            'value': existing_fb_user['data'].split(';')[1].split(':')[1],
        }]
        for cookie in cookies:
            driver.add_cookie(cookie)

        # 确认是否已成功添加Cookie
        cookies = driver.get_cookies()
        print(cookies)  # 打印所有当前的Cookies

        for target_url in target_urls:
            time.sleep(random.randint(1, 3))

            driver.get(target_url)
            print(target_url)

        time.sleep(20)

def run():
    # 配置代理和用户信息
    PROXY_SERVER = ["proxy.stormip.cn:1000", "us.stormip.cn:1000", "eu.stormip.cn:1000", "hk.stormip.cn:1000"]
    PROXY_USERNAME = ["storm-shuaizhang4476",
                      # 美国
                      "storm-shuaizhang4476_area-US",
                      # 欧洲
                      "storm-shuaizhang4476_area-RU",
                      "storm-shuaizhang4476_area-GB",
                      "storm-shuaizhang4476_area-DE",
                      # 亚洲
                      "storm-shuaizhang4476_area-SG",
                      "storm-shuaizhang4476_area-JP",
                      "storm-shuaizhang4476_area-KR",
                      "storm-shuaizhang4476_area-VN"]
    PROXY_PASSWORD = "zs19974476"

    random_server = random.choice(PROXY_SERVER)
    random_username = random.choice(PROXY_USERNAME)

    # Chrome 浏览器选项
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument(f"--proxy-server=http://{random_server}")

    # 初始化 EdgeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://myip.ipip.net")
        time.sleep(5)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(random_username)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        # 循环访问页面
        i = 1
        while i < 2:
            # 清除所有Cookies
            driver.delete_all_cookies()

            # 访问目标URL
            url = f"https://testflight.sending.me/#/home"
            driver.get(url)
            print(f"访问 {url}")

            # 设置一个Cookie
            existing_fb_users = [{
            "id": 38017,
            "data": "_ga:GA1.1.1299481105.1736182112;_ga_822RN0ZE72:GS1.1.1736182111.1.0.1736182111.0.0.0",
            "sdn_user_id": "@sdn_25a2e8a5d448dc9b10466e4c6eeb1c3a42bb5a02:25a2e8a5d448dc9b10466e4c6eeb1c3a42bb5a02"
        }]
            events = ['click', 'send_message']
            random_cookie = random.choice(existing_fb_users)
            events_str = ','.join(events)

            cookies = [{
                'name': random_cookie['data'].split(';')[0].split(':')[0],
                'value': random_cookie['data'].split(';')[0].split(':')[1],
            }, {
                'name': random_cookie['data'].split(';')[1].split(':')[0],
                'value': random_cookie['data'].split(';')[1].split(':')[1],
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
        #driver.quit()
        print()

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id):
    global events_str

    Utils.update_username('C:\\Users\\wingzhang\\Desktop\\proxy_dialog_handler\\firefox-username.txt', PROXY_USERNAME)

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

        driver.switch_to.window(driver.current_window_handle)
        pyautogui.moveTo(100, 100)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        #pyautogui.typewrite(PROXY_USERNAME)
        #time.sleep(0.5)
        #pyautogui.press("tab")
        #time.sleep(0.5)
        #pyautogui.typewrite(PROXY_PASSWORD)
        #time.sleep(0.5)
        #pyautogui.press("enter")

        #time.sleep(0.5)

        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        handle_newuser(driver, target_urls, events, device_id, created_by_task_id)

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

#while(True):
#run()
