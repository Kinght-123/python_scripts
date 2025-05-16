import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(root_dir)
sys.path.append(root_dir)

from service.connecter.redis_cli import redis_conn

pattern_list = [
    'sim', 'vessel', 'attendance_tos', 'ecs',
    'master:*:pstp:che_set:*', 'master:*:pstp:dsch_qpb_che_zset:*',
    'master:*:pstp:load_qpb_che_zset:*', 'master:cache_task:*',
    'master:qc_task:*', 'master:qctp-n:*', 'master:send_task:*',
    'master:yard_task:*', 'master:work_pool:ches'
]

for p in pattern_list:
    pattern = p + '*'
    keys = redis_conn.scan_iter(pattern)
    for k in keys:
        redis_conn.delete(k)
