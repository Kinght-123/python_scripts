"""
    - 用于构建可能需要的生成器
"""
import itertools

import basic
import parse_navis_works


# 生成器函数 ---- 生成平板车
def generate_cycled_truck_ids(num_iterations=600):
    # 创建无限循环的迭代器
    truck_id_iterators = [itertools.cycle(ids) for ids in basic.WORK_LINE.values()]

    # 使用zip组合迭代器，并使用islice来限制结果数量
    for sublist in itertools.islice(zip(*truck_id_iterators), num_iterations):
        for item in sublist:
            yield item


# 生成器函数 ---- 生成岸桥对应的任务列表
def xml_line_generator(xml_line, key):
    if key in xml_line:
        for xml_ls in xml_line[key]:
            yield xml_ls
    else:
        raise KeyError(f"Key {key} not found in WORK_LINE")


# # 创建生成器对象
# generator = generate_cycled_truck_ids()
#
# for truck in generator:
#     print(truck)

# print(str(uuid.uuid4()))


# 负责生成岸桥的生成器
gen = itertools.cycle(parse_navis_works.bridges)


# 测试的列表
ls = {
    'a': [[1, 2, 3, 4], [1, 2], [3, 4]],
    'b': [[1, 2], [1, 2], [1, 2, 3, 4]],
    'c': [[1, 2, 3, 4], [1, 2, 3, 4], [3, 4]],
    'd': [[1, 2], [1, 2, 3, 4], [3, 4]],
}
