import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui

import RequestsHandler
import Utils


def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events):
    # Chrome 浏览器选项
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 EdgeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://myip.ipip.net")
        time.sleep(2)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(PROXY_USERNAME)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        # 循环访问页面
        i = 1
       # target_url_list = Utils.handle_target_url(target_urls)

        for target_url in target_urls:
            time.sleep(random.randint(1, 10))

            while i < 2:
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

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id):
    global events_str

    # Chrome 浏览器选项
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://myip.ipip.net")
        time.sleep(2)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(PROXY_USERNAME)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(0.5)

        # 设置新用户行为
        events = ['register', 'register_success', 'login', 'login_success', 'set_user_name',
                  'set_user_name_success', 'sync_start', 'sync_completed', 'room_join', 'room_join_success',
                  'send_message']

        events_str = ','.join(events)
        cookies = [{
            'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
            'value': events_str
        }]

        for cookie in cookies:
            driver.add_cookie(cookie)

        # 循环访问页面
        i = 1

        for target_url in target_urls:
            time.sleep(random.randint(1, 10))

            while i < 2:
                # 清除用户数据
                driver.delete_cookie("_ga")
                driver.delete_cookie("_ga_822RN0ZE72")

                # 访问目标URL
                driver.get(target_url.replace('chat', 'testflight'))
                print(target_url)

                time.sleep(5)

                cookies = driver.get_cookies()
                print(cookies)  # 打印所有当前的Cookies

                cookie_string = ";".join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies if cookie['name'] in ['_ga', '_ga_822RN0ZE72']])

                RequestsHandler.handle_fb_user(device_id, cookie_string, created_by_task_id)

                '''
                # 设置event
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
                '''

                time.sleep(3)

                i += 1

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()
