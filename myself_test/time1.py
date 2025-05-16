from datetime import datetime


def generate_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d--%H:%M:%S')


print(generate_time())
