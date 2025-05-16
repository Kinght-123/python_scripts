import subprocess
import datetime
import time
import os
from concurrent.futures import ThreadPoolExecutor



def ping_single_device(ip, ip_log_dir="ping-ip-logs", max_file_size=10 * 1024 * 1024):  # 默认最大文件大小为10MB
    """
    对单个IP地址进行ping操作, 并记录结果到单独的文件中
    """
    log_file_path = os.path.join(ip_log_dir, f"{'_'.join(ip.split('.'))}_ping.log")

    # 检查文件大小是否超过限制
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) >= max_file_size:
        # 如果超过大小限制，则清空文件
        open(log_file_path, 'w').close()

    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        begin_time = time.time()
        result = subprocess.run(['ping', '-c', '1', ip], capture_output=True, text=True, timeout=1)
        with open(log_file_path, 'a') as file:
            if result.returncode != 0:  # 如果ping不通
                log_message = f"{current_time} - 无法ping通 {ip} {result.stderr}\n"
                file.write(log_message)
            else:
                # 从输出中提取内容
                time_str = result.stdout.split('time=')[-1].split()[0]
                log_message = f"{current_time} - {ip} ping通, 延迟: {time_str}ms\n"
                file.write(log_message)

    except subprocess.TimeoutExpired:
        log_message = f"{current_time} - ping {ip} 超时\n"
        with open(log_file_path, 'a') as file:
            file.write(log_message)
    except Exception as e:
        log_message = f"{current_time} - ping {ip} 时发生错误：{e}\n"
        with open(log_file_path, 'a') as file:
            file.write(log_message)
    finally:
        run_time = time.time() - begin_time
        if run_time < 1:
            time.sleep(max(0, 0.9 - run_time))


def ping_device(ip_list, ip_log_dir="ping-ip-logs"):
    """
    使用线程池对IP列表中的设备进行ping操作
    """
    os.makedirs(ip_log_dir, exist_ok=True)
    # 创建一个最大线程数为200的线程池
    with ThreadPoolExecutor(max_workers=200) as executor:
        while True:  # 无限循环，持续监控
            # 使用线程池提交所有ping任务
            futures = [executor.submit(ping_single_device, ip, ip_log_dir) for ip in ip_list]
            # 等待所有任务完成
            for future in futures:
                future.result()


if __name__ == "__main__":
    ip_path = os.path.join(os.path.dirname(__file__), "ip_list.txt")
    with open(ip_path, 'r') as f:
        ip_list = [line.strip() for line in f if line.strip()]
    ping_device(ip_list)
