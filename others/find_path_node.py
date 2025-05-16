import clickhouse_connect
import json
from datetime import datetime
import os

# 配置数据库连接参数
db_config = {
    'host': '10.188.73.102',
    'port': 28123,
    'user': 'root',
    'password': 'Trunk@123'
}


def find_task_id_path_node(che_id, task_id):
    formatted_date = datetime.now().strftime("%m-%d")
    day = datetime.now().strftime("%Y_%m_%d")
    file_name = f'{che_id}_{task_id}_waypoints_{formatted_date}.json'
    directory = os.path.join('json_files', day)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)  # 确保路径在不同的操作系统中都能正确处理

    # 定义SQL查询语句
    sql = f"""
    SELECT che_id, waypoints, che_timestamp
    FROM trunk_fms.navi
    WHERE task_id = '{task_id}'
    AND che_id = '{che_id}'
    ORDER BY che_timestamp DESC
    LIMIT 1;
    """

    try:
        with clickhouse_connect.get_client(**db_config) as client:
            result = client.command(sql)
            # 只有查询到结果的时候才执行下面的操作
            if isinstance(result, list):
                for i, row in enumerate(result):
                    if i == 1:
                        res = json.loads(row.replace("'", ''))
                        with open(file_path, 'w', encoding='utf-8') as fp:
                            json.dump(res, fp, ensure_ascii=False, indent=4)
                            print(f'{res} \n has been written to the file.')
                            fp.close()
            else:
                print("che_id and task_id is not matched")
    except Exception as e:
        print("An error occurred:", e)


def find_navi_id_path_node(che_id, navi_id):
    formatted_date = datetime.now().strftime("%m-%d")
    day = datetime.now().strftime("%Y_%m_%d")
    file_name = f'{che_id}_{navi_id}_waypoints_{formatted_date}.json'
    directory = os.path.join('json_files', day)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)  # 确保路径在不同的操作系统中都能正确处理

    # 定义SQL查询语句
    sql = f"""
    SELECT che_id, waypoints, che_timestamp
    FROM trunk_fms.navi
    WHERE navi_id = '{navi_id}'
    AND che_id = '{che_id}'
    ORDER BY che_timestamp DESC
    LIMIT 1;
    """

    try:
        with clickhouse_connect.get_client(**db_config) as client:
            result = client.command(sql)
            # 只有查询到结果的时候才执行下面的操作
            if isinstance(result, list):
                for i, row in enumerate(result):
                    if i == 1:
                        res = json.loads(row.replace("'", ''))
                        with open(file_path, 'w', encoding='utf-8') as fp:
                            json.dump(res, fp, ensure_ascii=False, indent=4)
                            print(f'{res} \n has been written to the file.')
                            fp.close()
            else:
                print("che_id and navi_id is not matched")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    che_id1 = input('enter che_id: ')
    id1 = input('enter id: ')
    # find_task_id_path_node(che_id=che_id1, task_id=id1)
    find_navi_id_path_node(che_id=che_id1, navi_id=id1)
