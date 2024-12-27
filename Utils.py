def handle_target_url(target_urls):
    return target_urls.split(',')

def test():
    for id in range(1, 4):
        print(id)

def active_firefox_window():
    print()

def update_username(file_path, username):
    try:
        # 打开文件进行读取
        with open(file_path, 'r') as file:
            # 读取所有行
            lines = file.readlines()

        lines[0] = username  # 修改 Age 为 35

        # 打开文件进行写入并保存
        with open(file_path, 'w') as file:
            file.writelines(lines)
    except Exception as e:
        print(f"出错: {e}")

#update_erorr_logs()