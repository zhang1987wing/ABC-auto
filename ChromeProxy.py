import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui

import RequestsHandler
import Utils
import WebProxy


def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events):
    global events_str

    # Chrome 浏览器选项
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 EdgeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        pyautogui.moveTo(100, 100)

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

    finally:
        # 关闭浏览器
        driver.quit()

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id):

    # Chrome 浏览器选项
    chrome_options = Options()

    # 设置代理
    chrome_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # 打开目标网址
        driver.get("https://chat.sending.me/abc.html")
        time.sleep(2)

        pyautogui.moveTo(100, 100)

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

    finally:
        # 关闭浏览器
        driver.quit()
