import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui

import WebProxy


def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events, need_proxy):
    global events_str

    # Chrome 浏览器选项
    chrome_options = Options()

    if need_proxy:
        # 设置代理
        chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 EdgeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        if need_proxy:
            pyautogui.FAILSAFE = False

            # 输入用户名和密码（使用 pyautogui 模拟输入）
            pyautogui.typewrite(PROXY_USERNAME)
            time.sleep(0.5)
            pyautogui.press("tab")
            time.sleep(0.5)
            pyautogui.typewrite(PROXY_PASSWORD)
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(0.5)

        WebProxy.handle_existing(driver, existing_fb_users, target_urls, events)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id, isHeadless, need_proxy):

    # Chrome 浏览器选项
    chrome_options = Options()

    if isHeadless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

    if need_proxy:
        # 设置代理
        chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        if not isHeadless and need_proxy:
            pyautogui.FAILSAFE = False

            # 输入用户名和密码（使用 pyautogui 模拟输入）
            pyautogui.typewrite(PROXY_USERNAME)
            time.sleep(0.5)
            pyautogui.press("tab")
            time.sleep(0.5)
            pyautogui.typewrite(PROXY_PASSWORD)
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(2)

        WebProxy.handle_newuser(driver, target_urls, events, device_id, created_by_task_id)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()

#run_new("eu.stormip.cn:1000", "storm-shuaizhang4476_area-TW", "zs19974476", [], [], 1, 1, False, True)