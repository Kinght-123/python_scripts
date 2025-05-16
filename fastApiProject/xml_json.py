import xmltodict
import json

'''
    xml转json
'''


# 递归函数，用于删除键中的特殊字符


def clean_keys(d):
    if isinstance(d, dict):
        new_dict = {}
        for k, v in d.items():
            new_key = k.lstrip('@#')  # 去掉键中的@和#
            new_dict[new_key] = clean_keys(v)
        return new_dict
    elif isinstance(d, list):
        return [clean_keys(i) for i in d]
    else:
        return d


# 读取XML文件并解析为字典
with open('567.xml', 'r') as xml_file:
    xml_data = xmltodict.parse(xml_file.read(), dict_constructor=dict)

# 清理字典中的键
cleaned_data = clean_keys(xml_data)

# 将字典转换为JSON格式并写入文件
with open('123.json', 'w') as json_file:
    json.dump(cleaned_data, json_file, indent=4)

print("处理完成，转换后的json数据已保存到123.json")
