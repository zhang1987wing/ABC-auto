import csv
import re

# 读取txt文件内容
with open('firefox-cookie.txt', 'r') as file:
    text = file.readlines()

# 正则表达式匹配GA和GS
ga_pattern = r"GA\d+\.\d+\.\d+\.\d+"  # 匹配GA的格式
gs_pattern = r"GS\d+\.\d+\.\d+\.\d+"  # 匹配GS的格式

# 提取GA和GS的值
ga_values = re.findall(ga_pattern, ''.join(text))
gs_values = re.findall(gs_pattern, ''.join(text))

# 将GA和GS值配对并写入CSV文件
with open('firefox-cookie.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['GA', 'GS'])  # 写入表头
    for ga, gs in zip(ga_values, gs_values):
        writer.writerow([ga, gs])  # 写入GA和GS的配对值

print("文件已成功转换为firefox-cookie.csv")
