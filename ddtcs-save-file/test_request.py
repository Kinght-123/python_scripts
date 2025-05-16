import paramiko
import os
import traceback
from pathlib import Path
import stat


def download_folder_via_sftp(hostname, port, username, password, remote_folder, local_folder):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)

        sftp = ssh.open_sftp()
        temp = remote_folder.split('/')[-1].replace(':', '_')
        local_dir_path = os.path.join(local_folder, temp)
        os.makedirs(local_dir_path, exist_ok=True)

        _download_folder(sftp, remote_folder, local_dir_path)

    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 确保关闭 SFTP 和 SSH 连接
        sftp.close()
        ssh.close()


def _download_folder(sftp, remote_folder, local_folder):
    try:
        remote_base_folder = Path(remote_folder)
        local_base_folder = Path(local_folder)
        remote_items = sftp.listdir(str(remote_base_folder).replace('\\', '/'))

        for item in remote_items:
            remote_path = remote_base_folder / item
            remote_dir_path = str(remote_path).replace('\\', '/')
            local_path = local_base_folder / item
            # 获取远程路径的信息
            try:
                file_attr = sftp.lstat(remote_dir_path)
            except FileNotFoundError:
                print(f"文件 {remote_path} 不存在，跳过...")
                continue

            # 如果是文件夹，则递归下载
            if stat.S_ISDIR(file_attr.st_mode):
                # 创建本地文件夹
                os.makedirs(str(local_path), exist_ok=True)
                print(f"正在下载文件夹：{remote_path}")
                _download_folder(sftp, remote_dir_path, str(local_path))
            else:
                # 下载文件
                print(f"正在下载文件：{remote_path}")
                sftp.get(remote_dir_path, str(local_path))
    except Exception as e:
        print(f"处理文件夹 {remote_folder} 时发生错误：{e}")
        print(traceback.format_exc())


# 示例用法
hostname = '10.188.73.101'
port = 22
username = 'root'
password = 'Trunk@123'
remote_folder = '/opt/trunk/ddtcs/monitordatas/2025-02-17-11:05:32_8ae663c6-ff59-4886-aee9-c1c83dea791f'
local_folder = 'C:\\Users\\trunk\\Desktop\\ddtcs-save-file\\che_info'

download_folder_via_sftp(hostname, port, username, password, remote_folder, local_folder)
