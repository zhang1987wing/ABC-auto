import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 定义浏览器路径
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 启动 Chrome 浏览器，设置调试端口为 9222
subprocess.Popen([
    chrome_path,
    "--remote-debugging-port=9222",  # 开启远程调试端口
    "--user-data-dir=C:\\temp\\chrome_profile",  # 使用特定的用户配置文件
    "--disable-gpu",
    "--start-maximized",
    "--no-sandbox"
])

# 创建 ChromeOptions 以连接到远程调试端口
chrome_options = Options()
chrome_options.debugger_address = "127.0.0.1:9222"

# 通过 Selenium 连接到已打开的浏览器
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
driver.get("https://gmgn.ai/sol/address/814Yn73NNBk4ytagrugpG5qiUHXhXUTxVk1tDdeb2FUJ")

# 获取标题
print(driver.title)

# 执行自动化操作（示例：查找按钮并点击）
# button = driver.find_element("xpath", "//button[@id='submit']")
# button.click()

# 关闭浏览器
driver.quit()
