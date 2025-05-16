import pandas as pd
from clickhouse_connect import get_client, Client

# 连接ClickHouse数据库
client = get_client(host='10.188.63.104',
                    port=28123,
                    user='root',
                    password='Trunk@123')

# 定义SQL查询语句
query = """
SELECT *
FROM trunk_fms.act_status
WHERE che_id = 'A534' AND
      che_timestamp >= '2024-12-27 14:53:00' AND
      che_timestamp <= '2024-12-27 14:54:59'
ORDER BY che_timestamp ASC;
"""

result = client.query(query)
columns = result.columns
print(columns)

# df = pd.DataFrame(result)
# df.to_excel('output.xlsx', index=False, engine='openpyxl')
