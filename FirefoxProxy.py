import sys
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pyautogui

import Utils
import WebProxy

isMacOs = sys.platform == "darwin"

def run_existing(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, existing_fb_users, target_urls, events, need_proxy):
    if not isMacOs:
        Utils.update_username('C:\\Users\\wingzhang\\Desktop\\proxy_dialog_handler\\firefox-username.txt', PROXY_USERNAME)

    firefox_options = Options()

    if need_proxy:
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

        driver.switch_to.window(driver.current_window_handle)
        pyautogui.FAILSAFE = False

        if sys.platform == "darwin":
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

        WebProxy.handle_existing(driver, existing_fb_users, target_urls, events)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()

def run_new(PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD, target_urls, events, device_id, created_by_task_id, need_proxy):
    if not isMacOs:
        Utils.update_username('C:\\Users\\qmk\\Desktop\\proxy_dialog_handler\\firefox-username.txt', PROXY_USERNAME)

    # Firefox 浏览器选项
    firefox_options = Options()

    if need_proxy:
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
        pyautogui.FAILSAFE = False

        if isMacOs:
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

        WebProxy.handle_newuser(driver, target_urls, events, device_id, created_by_task_id)

    except Exception as e:
        print(f"出错: {e}")
        raise

    finally:
        # 关闭浏览器
        driver.quit()

#run_new("proxy.stormip.cn:1000", "storm-shuaizhang4476", "zs19974476", [], [], 1, 1)