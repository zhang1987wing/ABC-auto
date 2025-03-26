import os
import subprocess
import sys
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def test_chrome(wallet):
    # 创建 ChromeOptions 以连接到远程调试端口
    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"

    # 通过 Selenium 连接到已打开的浏览器
    driver = webdriver.Chrome(options=chrome_options)
    results = []

    try:
        driver.get(f"https://gmgn.ai/sol/address/{wallet}")

        time.sleep(2)

        # 关闭tele连接
        driver.find_element("xpath",
                            "/html[1]/body[1]/div[2]/div[1]/div[3]/*[name()='svg'][1]").click()

        # 切换为30d
        driver.find_element("xpath",
                            "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div["
                            "1]/div[1]/div[3]").click()
        time.sleep(2)

        # 获取30d利润
        profit_str = driver.find_element("xpath",
                                         "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div["
                                         "2]/div[1]/div[1]/div[1]/div[2]/div[1]").text

        # 获取30d交易笔数
        buy_count_str = driver.find_element("xpath",
                                            "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div["
                                            "3]/div[1]/div[1]/div[3]/div[2]/div[1]/p[1]").text
        sell_count_str = driver.find_element("xpath",
                                             "/html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[1]/div[2]/div["
                                             "3]/div[1]/div[1]/div[3]/div[2]/div[1]/p[2]").text

        # 滚动页面加载更多交易
        last_height = driver.execute_script("return document.body.scrollHeight")
        # 翻页次数
        page = 1

        while page < 6:
            # 滚动页面到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # 等待页面加载更多内容

            # 获取新的页面高度
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # 如果页面高度没有变化，说明已经加载完所有内容
                break
            last_height = new_height
            page = page + 1

        table = driver.find_element("xpath",
                                    "/html/body/div[1]/div/div/main/div[2]/div[2]/div/div[2]/div[3]/div/div["
                                    "2]/div/div/div/div/div/table/tbody")
        # 获取所有行
        rows = table.find_elements(By.TAG_NAME, "tr")
        data = []

        # 遍历每一行，提取数据
        for row in rows:
            # 获取当前行的所有列
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text for col in cols]
            data.append(row_data)

        relation = trade_relation(data)
        profit = convert_number(profit_str)
        buy_count = convert_number(buy_count_str)
        sell_count = convert_number(sell_count_str)

        if profit < 0:
            result = f'最近30天负盈利'
        elif 0 <= profit < 2000:
            result = f'最近30天盈利{profit}，未达到标准'
        else:
            total_count = buy_count + sell_count
            if total_count <= 500:
                result = f'最近30天盈利{profit}，总交易数{total_count}笔{relation}'
            elif 500 < total_count < 1000:
                result = f'最近30天盈利{profit}，总交易数{total_count}笔, 可能是机器人'
            else:
                result = f'最近30天盈利{profit}，总交易数{total_count}笔，机器人'

        print(f'{wallet}：{result}')
        results.append({'wallet': wallet, 'result': result})

    except Exception as e:
        print(f"出错: {wallet}, {e}")
        results.append({'wallet': wallet, 'result': "未获取到足够信息，分析失败"})

    finally:
        # 关闭浏览器
        driver.quit()

    save_excel(results)


def convert_number(profit_str):
    profit_str = profit_str.replace('$', '').replace(',', '')  # 去掉 $ 和逗号
    multiplier = 1

    if profit_str.startswith('+'):
        profit_str = profit_str[1:]  # 去掉正号
    elif profit_str.startswith('-'):
        profit_str = profit_str[1:]
        multiplier = -1

    if 'K' in profit_str:
        value = float(profit_str.replace('K', '')) * 1000
    elif 'M' in profit_str:
        value = float(profit_str.replace('M', '')) * 1_000_000
    elif 'B' in profit_str:
        value = float(profit_str.replace('B', '')) * 1_000_000_000
    else:
        value = float(profit_str)

    return multiplier * value


def trade_relation(data):
    # 记录买入和卖出的状态
    trade_map = {}

    # 统计买入和卖出的次数
    for trade in data:
        action, stock = trade[0], trade[1]

        if stock not in trade_map:
            trade_map[stock] = {'买入': 0, '卖出': 0}

        if action == '买入':
            trade_map[stock]['买入'] += 1
        elif action == '卖出':
            trade_map[stock]['卖出'] += 1

    # 统计成对和不成对的数量
    paired_count = 0
    unpaired_count = 0

    for stock, counts in trade_map.items():
        buy_count = counts['买入']
        sell_count = counts['卖出']

        if buy_count == sell_count:
            # print(f"{stock} 的买入和卖出是成对的，次数：{buy_count}")
            paired_count += 1
        else:
            # print(f"{stock} 的买入和卖出不成对，买入次数：{buy_count}，卖出次数：{sell_count}")
            unpaired_count += 1

    total_stocks = len(trade_map)
    profit_ratio = unpaired_count / (paired_count + unpaired_count)
    # print(f"{profit_ratio}")

    if total_stocks < 4:
        return ", 交易品种少于4个，可能是庄家"

    if profit_ratio < 0.12:
        return ", 大部分交易成对出现，可能是机器人"

    return ''


def save_excel(data):
    # 将结果转换为DataFrame
    df = pd.DataFrame(data)

    # 文件名
    file_name = 'wallet_report.xlsx'

    if os.path.exists(file_name):
        # 文件存在时追加数据
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            start_row = writer.sheets['Sheet1'].max_row  # 获取已有数据的最后一行
            df.to_excel(writer, index=False, header=False, startrow=start_row)
    else:
        # 文件不存在时创建新文件
        df.to_excel(file_name, index=False)

    print("\n结果已追加到 wallet_report.xlsx ✅")


if __name__ == "__main__":

    platform = "MacOS" if sys.platform == "darwin" else "Windows"

    # https://docs.google.com/spreadsheets/d/1huVQKRhJQuRKiqf_85ATSEe8PfmDXWJEdRCR5qhmQ1Y/edit?gid=17904009#gid=17904009
    # 定义浏览器路径
    if platform == "MacOS":
        chrome_path = r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        user_data_dir = "/Users/qmk/Library/Application Support/Google/Chrome/Profile 1"
    else:
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        user_data_dir = "C:\\temp\\chrome_profile"

    # 启动 Chrome 浏览器，设置调试端口为 9222
    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",  # 开启远程调试端口
        f"--user-data-dir={user_data_dir}",  # 使用特定的用户配置文件
        "--disable-gpu"
    ])

    file_path = 'wallet.csv'
    for row in pd.read_csv(file_path, chunksize=1):
        wallet = row['wallet'].iloc[0]

        test_chrome(wallet)
        time.sleep(5)

    # convert_profit("-$32.5K")
