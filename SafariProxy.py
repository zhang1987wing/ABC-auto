import time
from selenium import webdriver

import WebProxy

def run_existing(existing_fb_users, target_urls, events):

    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
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

def run_new(target_urls, events, device_id, created_by_task_id):

    # Safari 浏览器选项
    safari_options = webdriver.SafariOptions()

    # 设置代理（Safari 不直接支持命令行代理设置，需通过系统代理进行配置）
    # Safari 使用系统代理，无法通过命令行直接设置代理，建议在系统偏好设置中配置代理
    # 初始化 SafariDriver
    driver = webdriver.Safari(options=safari_options)

    try:
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