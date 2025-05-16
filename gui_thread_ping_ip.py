import datetime
import time
import os
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import paramiko
import tkinter as tk
from tkinter import ttk, scrolledtext


def write_ping_result(time, ip, result, log_file_name='total-ip-result.log'):
    """
    将ping结果写入文件,每次循环重新写入新内容
    """
    log_file_path = os.path.abspath(log_file_name)

    # 以追加模式打开文件
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(f"{time} - {ip}: {result}\n")


def ping_single_device(ip, ssh_client, ip_log_dir="ping-ip-logs", max_file_size=10 * 1024 * 1024):  # 默认最大文件大小为10MB
    """
    通过SSH连接到远程服务器并对单个IP地址进行ping操作, 并记录结果到单独的文件中
    """
    log_file_path = os.path.join(ip_log_dir, f"{'_'.join(ip.split('.'))}_ping.log")

    # 检查文件大小是否超过限制
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) >= max_file_size:
        # 如果超过大小限制，则清空文件
        open(log_file_path, 'w', encoding='utf-8').close()

    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        begin_time = time.time()

        # 通过SSH执行ping命令
        stdin, stdout, stderr = ssh_client.exec_command(f'ping -c 1 -W 1 {ip}')
        result_output = stdout.read().decode()
        error_output = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()

        with open(log_file_path, 'a', encoding='utf-8') as file:
            if exit_status != 0:  # 如果ping不通
                log_message = f"{current_time} - 无法ping通 {ip} {error_output}\n"
                file.write(log_message)
                return (ip, "unreachable", 0)
            else:
                # 从输出中提取内容
                time_str = result_output.split('time=')[-1].split()[0]
                log_message = f"{current_time} - {ip} ping通, 延迟: {time_str}ms\n"
                file.write(log_message)
                return (ip, "success", time_str)

    except Exception as e:
        log_message = f"{current_time} - ping {ip} 时发生错误：{e}\n"
        with open(log_file_path, 'a', encoding='utf-8') as file:
            file.write(log_message)
            return (ip, "unreachable", 0)
    finally:
        run_time = time.time() - begin_time
        if run_time < 1:
            time.sleep(max(0, 0.9 - run_time))


class PingMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Ping监控")

        # 创建左右两个主框架
        left_frame = ttk.Frame(self.root)
        right_frame = ttk.Frame(self.root)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 配置根窗口的网格权重
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 配置左右框架的网格权重
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=1)

        # 在左框架中创建可以ping通的IP文本框
        self.create_text_area("可以ping通的IP:", left_frame)
        self.success_text = self.text_area

        # 在右框架中创建ping不通的IP文本框
        self.create_text_area("ping不通的IP:", right_frame)
        self.unreachable_text = self.text_area

    def create_text_area(self, label, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        ttk.Label(frame, text=label).grid(row=0, column=0, sticky="w")
        self.text_area = scrolledtext.ScrolledText(frame)  # 移除固定高度
        self.text_area.grid(row=1, column=0, sticky="nsew", pady=2)

    def update_display(self, results):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 更新成功ping通的IP
        self.success_text.delete(1.0, tk.END)
        self.success_text.insert(tk.END, f"=== {current_time} ===\n")
        self.success_text.insert(tk.END, f"总数: {len(results['success'])}个\n")
        self.success_text.insert(tk.END, '\n'.join(results['success']))

        # 更新ping不通的IP
        self.unreachable_text.delete(1.0, tk.END)
        self.unreachable_text.insert(tk.END, f"=== {current_time} ===\n")
        self.unreachable_text.insert(tk.END, f"总数: {len(results['unreachable'])}个\n")
        self.unreachable_text.insert(tk.END, '\n'.join(results['unreachable']))

        # 更新GUI
        self.root.update()


def ping_device(ip_list, ip_log_dir="ping-ip-logs"):
    """
    使用线程池对IP列表中的设备进行ping操作
    """
    os.makedirs(ip_log_dir, exist_ok=True)

    # 创建GUI窗口
    root = tk.Tk()
    root.geometry("1600x900")  # 设置更大的初始窗口大小
    gui = PingMonitorGUI(root)

    # 创建SSH客户端连接
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 连接到远程服务器，这里需要填写实际的用户名和密码
        ssh_client.connect('**.***.**.***', username='user', password='password')

        # 创建一个最大线程数为200的线程池
        with ThreadPoolExecutor(max_workers=200) as executor:
            while True:  # 无限循环，持续监控
                # 使用字典收集不同状态的IP
                results = defaultdict(list)

                # 使用线程池提交所有ping任务
                futures = [executor.submit(ping_single_device, ip, ssh_client, ip_log_dir) for ip in ip_list]

                # 收集所有结果
                for future in futures:
                    ip, status, ping_time = future.result()
                    if ping_time == 0:
                        results[status].append(ip)
                    else:
                        results[status].append(f'{ip}, 延迟: {ping_time}ms')

                print(f'99: {results["success"]}')
                print(f'66: {results["unreachable"]}')
                # 更新GUI显示
                # gui.update_display(results)
                # 写入日志文件
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open('total-ip-result.log', 'w', encoding='utf-8') as f:
                    f.write(f"=== {current_time} 扫描结果汇总 ===\n")
                    f.write(f"可以ping通的IP列表 ({len(results['success'])}个):\n")
                    f.write('\n'.join(results['success']) + '\n')

                    f.write(f"ping不通的IP列表 ({len(results['unreachable'])}个):\n")
                    f.write('\n'.join(results['unreachable']) + '\n')

                root.update()

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        ssh_client.close()


if __name__ == "__main__":
    ip_path = os.path.join(os.path.dirname(__file__), "ip_list.txt")
    with open(ip_path, 'r') as f:
        ip_list = [line.strip() for line in f if line.strip()]
    ping_device(ip_list)
