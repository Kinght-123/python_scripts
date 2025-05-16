from task_pb2 import Person, Gender
import sys
from google.protobuf.json_format import MessageToDict

# 创建一个Person的实例
p = Person()
p.id = 66666
p.name = 'John Alex'
p.email = 'alex@163.com'
p.gender = Gender.MALE
# print(f'type of p: {type(p)}')
# print(f'p: {p}')
# print(f'memory of p: {sys.getsizeof(p)}bytes')
# print()
# 序列化
serialized_data = p.SerializeToString()
# print(f'type of serialized_data: {type(serialized_data)}')
# print(f'serialized_data: {serialized_data}')
# print(f'memory of serialized_data: {sys.getsizeof(serialized_data)}bytes')
# 反序列化
p.ParseFromString(serialized_data)
# print(f'type of new_p: {type(new_p)}')
# print(f'new_p: {new_p}')
data = MessageToDict(
    p,
    preserving_proto_field_name=True,
    use_integers_for_enums=True
)
print(p)
# print(f'memory of new_p: {sys.getsizeof(new_p)}bytes')
# if new_p.gender == Gender.MALE:
#     print('It is a man')
# else:
#     print('It is a woman')
