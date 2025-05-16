import time

import paramiko
import traceback
import shutil
import re

from pathlib import Path


# 生成日期作为文件名的前缀
def get_date_time():
    return time.strftime("%Y%m%d", time.localtime())


# 匹配不包含日期格式的文本
pattern = r'^(?!.*(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})).*$'

data = time.strftime("%Y-%m-%d", time.localtime())

basdir = Path(__file__).resolve().parent.parent / '实船作业日志' / f'{get_date_time()}实船作业日志'

path_logs = [f'path_dispather-{data}-info.log', f'path_dispather-{data}-error.log']

remote_log_names = ['tos-sim-service', 'ddtcs-service', 'path-dispatcher-service', 'qcc-service',
                    'taskmgr-service', 'ycc-service', 'tosc-service', 'tos-sim-service']

SERVICE_CONFIG = {
    'hostname': '10.188.73.104',
    'username': 'ubuntu',
    'password': 'ubuntu',
    'remote_log_names': remote_log_names,
    'local_folder': basdir
}


def _get_remote_path(service: str) -> str:
    """获取远程服务日志路径"""
    if service == 'taskmgr-service':
        return f'/opt/trunk/{service}/taskmgr-logs'
    if service == 'tos-sim-service':
        return f'/opt/trunk/{service}/tos-sim-logs'
    return f'/opt/trunk/{service}/logs'


# 从服务器上下载文件到本地
def download_folder_via_sftp(hostname, username, password, remote_log_names, local_folder):
    global ssh, sftp
    try:

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)

        sftp = ssh.open_sftp()
        for remote_log_name in remote_log_names:
            remote_folder = _get_remote_path(remote_log_name)
            # 新建本地的文件夹存储对应的日志文件
            local_folder_ = Path(f'{local_folder}/{remote_log_name}日志')
            local_folder_.mkdir(parents=True, exist_ok=True)
            # 下载文件夹
            print(f'{remote_log_name.center(77, "=")}')

            _download_folder(sftp, remote_folder, local_folder_)
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 确保关闭 SFTP 和 SSH 连接
        sftp.close()
        ssh.close()


def _download_folder(sftp, remote_folder, local_folder):
    try:
        # 由于windows系统和linux系统的文件路径的方式不一样, 故linux系统的文件命名需要单独处理
        local_base_folder = Path(local_folder)
        remote_items = sftp.listdir(remote_folder)
        for item in remote_items:
            # 如果匹配到不包含日期格式的文本
            if re.match(pattern, item) or ('path' in item and item in path_logs):

                # 找出具体的日志文件的路径
                remote_log_path = remote_folder + '/' + item
                local_log_path = local_base_folder / item

                b = time.time()
                sftp.get(remote_log_path, str(local_log_path))
                print(f"已下载文件：{item}".ljust(50) + f"耗时{time.time() - b:.2f}s")
    except Exception as e:
        print(f"处理文件夹 {remote_folder} 时发生错误：{e}")
        print(traceback.format_exc())


def compress_folder(source_folder_path):
    try:
        start_time = time.time()
        print('开始压缩'.center(77, '='))
        archive_name = str(source_folder_path).split('/')[-1]
        shutil.make_archive(archive_name, 'zip', source_folder_path)
        print(f"压缩完成: {archive_name}.zip, 总耗时: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"压缩文件夹时发生错误：{e}")
        print(traceback.format_exc())


def main():
    begin = time.time()
    basdir.mkdir(parents=True, exist_ok=True)
    # 复制服务器上的文件到本地
    download_folder_via_sftp(**SERVICE_CONFIG)
    # 将获取的文件夹进行压缩
    compress_folder(basdir)
    print(f"running_time: {time.time() - begin:.2f}s")


if __name__ == '__main__':
    main()
