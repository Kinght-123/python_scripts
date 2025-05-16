import json
import subprocess
import datetime
import time
import os
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def write_ping_result(time, ip, result, log_file_name='total-ip-result.log'):
    """
    将ping结果写入文件,每次循环重新写入新内容
    """
    log_file_path = os.path.abspath(log_file_name)

    # 以追加模式打开文件
    with open(log_file_path, 'a') as f:
        f.write(f"{time} - {ip}: {result}\n")


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
                return (ip, "unreachable", 0)
            else:
                # 从输出中提取内容
                time_str = result.stdout.split('time=')[-1].split()[0]
                log_message = f"{current_time} - {ip} ping通, 延迟: {time_str}ms\n"
                file.write(log_message)
                return (ip, "success", time_str)

    except subprocess.TimeoutExpired:
        log_message = f"{current_time} - ping {ip} 超时\n"
        with open(log_file_path, 'a') as file:
            file.write(log_message)
            return (ip, "unreachable", 0)
    except Exception as e:
        log_message = f"{current_time} - ping {ip} 时发生错误：{e}\n"
        with open(log_file_path, 'a') as file:
            file.write(log_message)
            return (ip, "unreachable", 0)
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
            # 使用字典收集不同状态的IP
            results = defaultdict(list)
            # 使用线程池提交所有ping任务
            futures = [executor.submit(ping_single_device, ip, ip_log_dir) for ip in ip_list]

            # 收集所有结果
            for future in futures:
                ip, status, ping_time = future.result()
                if ping_time == 0:
                    results[status].append(ip)
                else:
                    results[status].append(f'{ip:<13}, 延迟: {ping_time}ms')

            success_ips, unreachable_ips = results['success'], results['unreachable']
            copy_unreachable_ips = unreachable_ips.copy()
            # 补全空缺值
            if len(success_ips) < len(unreachable_ips):
                success_ips.extend([''] * (len(unreachable_ips) - len(success_ips)))
            elif len(success_ips) > len(unreachable_ips):
                unreachable_ips.extend([''] * (len(success_ips) - len(unreachable_ips)))
            # 写入汇总结果
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('total-ip-result.log', 'w') as fp:
                fp.write(f"=== {current_time} 扫描结果汇总 ===\n")
                fp.write(
                    f"在线的IP列表 ({len(results['success'])}个):  \t\t\t 离线的IP列表 ({len(copy_unreachable_ips)}个):\n")
                for success_ip, unreachable_ip in zip(success_ips, unreachable_ips):
                    fp.write(f"{success_ip.ljust(42)}{unreachable_ip}\n")
                # f.write(f"可以ping通的IP列表 ({len(results['success'])}个):\n")
                # f.write('\n'.join(results['success']) + '\n')
                #
                # f.write(f"ping不通的IP列表 ({len(results['unreachable'])}个):\n")
                # f.write('\n'.join(results['unreachable']) + '\n')
                #
                # f.write(f"ping超时的IP列表 ({len(results['timeout'])}个):\n")
                # f.write('\n'.join(results['timeout']) + '\n')
                #
                # f.write(f"ping发生错误的IP列表 ({len(results['error'])}个):\n")
                # f.write('\n'.join(results['error']) + '\n')


if __name__ == "__main__":
    ip_path = os.path.join(os.path.dirname(__file__), "ip_list.txt")
    with open(ip_path, 'r') as f:
        ip_list = [line.strip() for line in f if line.strip()]
    ping_device(ip_list)
