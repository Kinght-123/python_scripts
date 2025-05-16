import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def save_to_json_file(che_id, msg_type, msg_dict, cdi_id, create_time):
    bash_directory = BASE_DIR / 'monitordatas' / f'{create_time}_{cdi_id}' / msg_type
    bash_directory.mkdir(parents=True, exist_ok=True)
    file_name = bash_directory / f'{che_id}.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(msg_dict, json_file, ensure_ascii=False, indent=4)


def generate_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d-%H_%M_%S')
