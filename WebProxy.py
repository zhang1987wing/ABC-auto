import random
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import pyautogui

import ReadCookie

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

    # Edge 浏览器选项
    edge_options = Options()

    # 设置代理
    edge_options.add_argument(f"--proxy-server=http://{random_server}")

    # 初始化 EdgeDriver
    driver = webdriver.Edge(options=edge_options)

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
        while i < 9:
            # 清除所有Cookies
            driver.delete_all_cookies()

            # 访问目标URL
            url = f"https://fb-test-sd.vercel.app/room/{i * 111}"
            driver.get(url)
            print(f"访问 {url}")

            # 设置一个Cookie
            random_cookie = ReadCookie.read_edge_cookie()
            cookies = [{
                'name': '_ga',
                'value': random_cookie['GA'],
            }, {
                'name': '_ga_HNRD6KMSBG',
                'value': random_cookie['GS'],
            }]
            for cookie in cookies:
                driver.add_cookie(cookie)

            # 确认是否已成功添加Cookie
            cookies = driver.get_cookies()
            print(cookies)  # 打印所有当前的Cookies

            i += 1
            time.sleep(2)

    except Exception as e:
        print(f"出错: {e}")

    finally:
        # 关闭浏览器
        driver.quit()

while(True):
    run()