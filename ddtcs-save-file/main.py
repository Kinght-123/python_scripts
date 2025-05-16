"""
    - 要求python版本3.8及以上
    - 提供用户获取车辆的actstatus, navi, cdi数据以及当时的屏幕截图保存到与当前目录同级的che_infos目录下
    - 运行这个文件的时候需要电脑中运行着地图监控的浏览器即可
    - 使用的时候启动这个文件, 然后运行api接口即可
"""
import time
import httpx
import paramiko
import traceback
import json
import concurrent.futures
import shutil
import pygetwindow as gw
import pyautogui
import mss
import mss.tools

from fastapi import FastAPI
from pathlib import Path

app = FastAPI()

basdir = Path(__file__).resolve().parent / 'mqtt_sub'
url = 'http://10.188.73.101:8085/save/che_info'


# 从服务器上下载文件到本地
def download_folder_via_sftp(hostname, port, username, password, remote_folder, local_folder):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)

        sftp = ssh.open_sftp()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            futures.append(executor.submit(_download_folder, sftp, remote_folder, local_folder))
        for future in concurrent.futures.as_completed(futures):
            future.result()
        # _download_folder(sftp, remote_folder, local_folder)
    except Exception as e:
        print(f"发生错误：{e}")
    finally:
        # 确保关闭 SFTP 和 SSH 连接
        sftp.close()
        ssh.close()


def _download_folder(sftp, remote_folder, local_folder):
    try:
        # 由于windows系统和linux系统的文件路径的方式不一样, 故linux系统的文件命名需要单独处理
        remote_base_folder = Path(remote_folder)
        local_base_folder = Path(local_folder)
        remote_items = sftp.listdir(str(remote_base_folder).replace('\\', '/'))
        for item in remote_items:
            # 单独处理linux系统的路径
            remote_path_linux = remote_base_folder / item
            remote_dir_path = str(remote_path_linux).replace('\\', '/')
            local_dir_path = local_base_folder / item
            local_dir_path.mkdir(parents=True, exist_ok=True)
            remote_specific_file_paths = sftp.listdir(remote_dir_path)
            for specific_file in remote_specific_file_paths:
                remote_specific_file_path = remote_dir_path + '/' + specific_file
                local_specific_file_path = local_dir_path / specific_file
                # print(local_specific_file_path)
                # 下载文件
                # print(local_specific_file_path)
                # print(f"正在下载文件: {'/'.join(remote_specific_file_path.split('/')[-3::])}")
                sftp.get(remote_specific_file_path, str(local_specific_file_path))
    except Exception as e:
        print(f"处理文件夹 {remote_folder} 时发生错误：{e}")
        print(traceback.format_exc())


def capture_screen(output_path="screenshot.png", key_word='TRUNK FIT'):
    # 获取所有浏览器窗口
    browser_windows = [window for window in gw.getAllWindows() if "Chrome" in window.title or "Edge" in window.title]
    # 遍历每个浏览器窗口
    for window in browser_windows:
        window.activate()
        target_found = False  # 标志目标标签页是否找到
        initial_title = window.title
        for i in range(0, 10):  # 假设最多切换 10 次标签页
            pyautogui.hotkey('ctrl', 'tab')  # 切换到下一个标签页
            current_window = gw.getActiveWindow()
            if current_window.title == initial_title and key_word not in initial_title:
                break
            # 检查标题是否包含目标关键字
            if key_word in current_window.title:
                current_window.activate()
                time.sleep(0.3)
                # 获取当前窗口的边界
                left = current_window.left
                top = current_window.top
                width = current_window.width
                height = current_window.height
                # 截图当前窗口
                with mss.mss() as sct:
                    monitor = {
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height
                    }
                    img = sct.grab(monitor)
                    mss.tools.to_png(img.rgb, img.size, output=output_path)
                    target_found = True
                break
        if target_found:
            break


def compress_folder(source_folder_path):
    try:
        archive_name = str(source_folder_path).split('/')[-1]
        shutil.make_archive(archive_name, 'zip', source_folder_path)
    except Exception as e:
        print(f"压缩文件夹时发生错误：{e}")
        print(traceback.format_exc())


def send_post(url):
    with httpx.Client() as client:
        response = client.post(url)
        bytes_text = response.content
        return response.status_code, json.loads(bytes_text.decode('utf-8')).get('msg')


@app.get("/ddtcs/save_screenshoot")
async def save_screenshoot():
    begin = time.time()
    # 截图,调用服务器上的api并保存到本地
    code, dir_name = send_post(url=url)
    total_name = dir_name.replace(':', '_')
    bash_directory = basdir / f'{total_name}'
    bash_directory.mkdir(parents=True, exist_ok=True)
    photo_path = bash_directory / 'screenshot.png'
    capture_screen(str(photo_path))

    # 复制服务器上的文件到本地
    download_folder_via_sftp(hostname='10.188.73.101',
                             port=22,
                             username='root',
                             password='Trunk@123',
                             remote_folder=f'/opt/trunk/ddtcs/monitordatas/{dir_name}',
                             local_folder=bash_directory)
    # 将获取的文件夹进行压缩
    compress_folder(bash_directory)
    return {
        'file_name': dir_name,
        'api_status': code,
        'status': 200,
        "running_time": f"{time.time() - begin:.2f}s"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
