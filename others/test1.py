from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import clickhouse_connect
import os
import json
from datetime import datetime

app = FastAPI()

client = clickhouse_connect.get_client(host='10.188.63.104',
                                       port=28123,
                                       user='root',
                                       password='Trunk@123'
                                       )


@app.post("/download-json/")
async def download_json(che_id: str, task_id: str):
    formatted_date = datetime.now().strftime("%m-%d")
    file_name = f'{formatted_date}_{che_id}.json'
    directory = 'json_files'
    file_path = os.path.join(directory, file_name)  # 确保路径在不同的操作系统中都能正确处理
    os.makedirs(directory, exist_ok=True)

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
        result = client.command(sql)
        # 只有查询到结果的时候才执行下面的操作
        if type(result) is list:
            for i, row in enumerate(result):
                if i == 1:
                    res = json.loads(row.replace("'", ''))
                    with open(file_path, 'w', encoding='utf-8') as fp:
                        json.dump(res, fp, ensure_ascii=False, indent=4)
                        fp.close()
                    # return FileResponse(path=file_path, filename=file_name, media_type='application/json')
                    raise HTTPException(
                        status_code=404,
                        detail=f'{res} \n has been written to the file.',
                        headers={"Content-Type": "application/json"},
                        response=FileResponse(path=file_path, filename="error.json", media_type='application/json')
                    )
        else:
            raise HTTPException(status_code=404, detail="No data found for the given che_id and task_id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
