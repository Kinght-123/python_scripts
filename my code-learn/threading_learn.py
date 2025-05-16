import threading
import time
from time import sleep

'''
    重写父类Threading.Thread
'''


# myThread继承父类，并进行重写
class myThread(threading.Thread):
    def __init__(self, number, item):
        threading.Thread.__init__(self)
        self.number = number
        self.item = item

    def run(self):
        print(f'[线程开始]: {self.name}')
        task1(self.name, self.number, self.item)
        print(f'[线程结束]: {self.name}')

    def __del__(self):
        print(f'[线程销毁释放内存]: {self.name}')


def task1(thread_name, number, item):
    a = 0
    while a < number:
        sleep(1)
        a += 1
        current_time = time.strftime('%H:%M:%S', time.localtime())
        print(f'[{current_time}] {thread_name}输出{item}')


thread1 = myThread(4, "book")
thread2 = myThread(2, "ball")

thread1.start()
thread2.start()

thread1.join()
thread2.join()
