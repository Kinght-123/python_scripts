import json
import time

import redis
import logging

# 测试redis
oy_fz_redis_settings = {
    'host': '10.188.73.101',
    'port': 6379,
    'password': 'Trunk@123',
    # 'decode_responses': True
}

# 生产redis
oy_sc_redis_settings = {
    'host': '10.188.73.102',
    'port': 6379,
    'password': 'Trunk@123',
    # 'decode_responses': True
}

# 青岛redis
qd_redis_settings = {
    'host': '10.11.1.51',
    'port': 6378,
    'password': 'Trunk@123',
}

host_redis_settings = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 2,  # 0-欧亚仿真; 1-青岛仿真; 2-欧亚生产
}


def copy(origin_redis_settings, target_redis_settings2):
    source_redis = redis.Redis(**origin_redis_settings)
    target_redis = redis.Redis(**target_redis_settings2)
    cursor = 0
    batch_size = 2000
    total_keys = 0
    while True:
        # 使用 scan 命令分批获取键
        cursor, keys = source_redis.scan(cursor, count=batch_size)
        if not keys:
            break
        # 针对每个键进行迁移
        for key in keys:
            # 获取键的类型
            key_type = source_redis.type(key).decode('utf-8')
            # 根据键的类型进行相应的迁移操作
            if key_type == 'string':
                value = source_redis.get(key)
                target_redis.set(key, value)
            elif key_type == 'hash':
                value = source_redis.hgetall(key)
                target_redis.hset(key, mapping=value)
            elif key_type == 'list':
                value = source_redis.lrange(key, 0, -1)
                target_redis.rpush(key, *value)
            elif key_type == 'set':
                value = source_redis.smembers(key)
                target_redis.sadd(key, *value)
            elif key_type == 'zset':
                value = source_redis.zrange(key, 0, -1, withscores=True)
                target_redis.zadd(key, {k: v for k, v in value})
            else:
                print(f"不支持的数据类型：{key_type}，跳过键：{key}")
            print(f"{key.decode('utf-8')} 迁移完成, 还有{len(keys) - total_keys}个键值待迁移")
            time.sleep(0.1)
            total_keys += 1
            if total_keys == len(keys):
                print(f'{total_keys}个键值已经迁移完成!!!')
                break
        break
    print('迁移完成')
    # 要迁移的key
    # key = 'machine_status:yc_id:Y312'
    # # 从第一个Redis实例中读取hash数据
    # hash_data = r2.hgetall(key)
    # # 将数据写入到第二个Redis实例
    # if hash_data:
    #     r1.hset(key, mapping=hash_data)
    #     print(f"数据已成功写入到第二个Redis实例的{key}中")
    # else:
    #     print(f"在第一个Redis实例中未找到{key}对应的数据")


def compare_data():
    r = redis.Redis(**qd_redis_settings)
    hash_data1 = r.hgetall('machine_status:qc_id:Q110')
    decoded_dict1 = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data1.items()}
    hash_data2 = r.hgetall('machine_status:qc_id:Q301')
    decoded_dict2 = {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_data2.items()}
    for key in decoded_dict1.keys():
        if key not in decoded_dict2.keys():
            print(decoded_dict1[key])
            print(f"Key '{key}' not found in Q301 hash")


def test_qctp_n(redis_settings):
    r = redis.Redis(**redis_settings)
    key = 'master:qctp-n:Q304'
    value = [566936.8856507122, 4317844.789024687]
    r.hset(key, mapping={'0': json.dumps(value)})


def delete_keys_by_pattern(r, pattern):
    cursor = '0'
    while cursor != 0:
        cursor, keys = r.scan(cursor=cursor, match=pattern, count=100000)
        for key in keys:
            try:
                r.delete(key)
                logging.info(f'Deleted key: {key}')
            except Exception as e:
                logging.error(f'Failed to delete key {key}: {e}')


def main(redis_settings):
    try:
        r = redis.Redis(**redis_settings)
        # patterns = [
        #     'sim:*',
        #     'master:*',
        #     'ecs:*',
        # ]
        patterns = [
            'sim', 'vessel', 'attendance_tos', 'ecs',
            'master:*:pstp:che_set:*', 'master:*:pstp:dsch_qpb_che_zset:*',
            'master:*:pstp:load_qpb_che_zset:*', 'master:cache_task:*',
            'master:qc_task:*', 'master:qctp-n:*', 'master:send_task:*',
            'master:yard_task:*', 'master:work_pool:ches'
        ]
        for pattern in patterns:
            delete_keys_by_pattern(r, pattern)
            print(f'Deleted keys matching pattern: {pattern}')
    except redis.RedisError as e:
        logging.error(f'Redis error: {e}')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
    finally:
        r.close()


if __name__ == '__main__':
    # test_qctp_n(qd_redis_settings)
    # compare_data()
    # main(qd_redis_settings)
    copy(oy_sc_redis_settings, host_redis_settings)
