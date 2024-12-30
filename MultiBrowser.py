import threading
import time
from concurrent.futures import ThreadPoolExecutor
import ChromeProxy


def browser_task(task_id):
    print(f"Browser {task_id} started by thread {threading.current_thread().name}")

    time.sleep(20)

    ChromeProxy.run_new("proxy.stormip.cn:1000", "storm-shuaizhang4476", "zs19974476", ["https://chat.sending.me/#/home",
        "https://chat.sending.me/#/discover",], ["register",
        "register_success",
        "login",
        "login_success",
        "set_user_name",
        "set_user_name_success",
        "onboarding_success",
        "sync_start",
        "sync_completed",
        "read_message",
        "room_join",
        "room_join_success",
        "send_message",
        "send_message_success"], 10001, 10001, True, False)

    print(f"Browser {task_id} completed by thread {threading.current_thread().name}")

# 模拟服务端下发的任务数量
total_tasks = 1000  # 假设任务数量为10

# 任务分配的线程数
num_threads = 3

# 创建一个线程池来并行处理任务
def distribute_tasks(total_tasks, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 将任务分配给线程池
        executor.map(browser_task, range(1, total_tasks + 1))

distribute_tasks(total_tasks, num_threads)

print("All headless browsers have completed their tasks.")
