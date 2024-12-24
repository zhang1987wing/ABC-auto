import random
import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.chrome.options import Options

import ReadCookie
import RequestsHandler


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
            existing_fb_users = ['_GA:GA1.1.1318980546.1734180344;_ga_HNRD6KMSBG:GS1.1.1734180344.1']
            events = ['click', 'send_message']
            random_cookie = random.choice(existing_fb_users)
            events_str = ','.join(events)

            cookies = [{
                'name': random_cookie.split(';')[0].split(':')[0],
                'value': random_cookie.split(';')[0].split(':')[1],
            }, {
                'name': random_cookie.split(';')[1].split(':')[0],
                'value': random_cookie.split(';')[1].split(':')[1],
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

def run_new():
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
        driver.get("https://testflight.sending.me/#/login")
        time.sleep(5)

        # 输入用户名和密码（使用 pyautogui 模拟输入）
        pyautogui.typewrite(random_username)
        time.sleep(0.5)
        pyautogui.press("tab")
        time.sleep(0.5)
        pyautogui.typewrite(PROXY_PASSWORD)
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(5)

        #设置新用户行为
        events = ['register', 'register_success', 'login', 'login_success', 'set_user_name',
                  'set_user_name_success', 'sync_start', 'sync_completed', 'room_join', 'room_join_success',
                  'send_message']

        events_str = ','.join(events)
        cookies = [{
            'name': "custom_incremented_d8e6cfd10abd4f3abadd4fd2d1b664e2",
            'value': events_str,
            'domain':'testflight.sending.me',
            'path':'/',
            'secure':True,
            'httpOnly':False
        }]

        for cookie in cookies:
            driver.add_cookie(cookie)

        cookies = driver.get_cookies()
        print(cookies)  # 打印所有当前的Cookies

        time.sleep(30)

        # 循环访问页面
        i = 1
        while i < 2:
            # 清除用户数据
            driver.delete_cookie("_ga")
            driver.delete_cookie("_ga_822RN0ZE72")

            # 访问目标URL
            url = f"https://testflight.sending.me/#/home"
            driver.get(url)
            print(f"访问 {url}")

            cookies = driver.get_cookies()
            print(cookies)  # 打印所有当前的Cookies

            cookie_string = ";".join([f"{cookie['name']}:{cookie['value']}" for cookie in cookies if
                                      cookie['name'] in ['_ga', '_ga_822RN0ZE72']])

            RequestsHandler.handle_fb_user(1, cookie_string, 300)

            i += 1
            time.sleep(5)

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        #driver.quit()
        print()

run_new()