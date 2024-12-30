import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.edge.options import Options

import WebProxy


def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events, need_proxy):
    global events_str

    # Edge 浏览器选项
    edge_options = Options()

    if need_proxy:
        # 设置代理
        edge_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 Edge 浏览器
    driver = webdriver.Edge(options=edge_options)

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

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id, need_proxy):
    global events_str

    # Edge 浏览器选项
    edge_options = Options()

    if need_proxy:
        # 设置代理
        edge_options.add_argument(f"--proxy-server=http://{PROXY_SERVER}")

    # 初始化 Edge 浏览器
    driver = webdriver.Edge(options=edge_options)

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
            time.sleep(2)

        WebProxy.handle_newuser(driver, target_urls, events, device_id, created_by_task_id)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()

#run_new("proxy.stormip.cn:1000", "storm-shuaizhang4476", "zs19974476", [], [], 1, 1)