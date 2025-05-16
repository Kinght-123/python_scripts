from _collections import deque

list = [1, 2, 3, 4, 5]
deque_list = deque(list, maxlen=5)
deque_list.rotate(-2)
print(deque_list)