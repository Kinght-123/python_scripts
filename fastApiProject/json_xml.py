import xmltodict
import json

'''
    json转xml
'''
# 读取 JSON 文件
with open('123.json', 'r') as json_file:
    json_data = json.load(json_file)

# 将 JSON 数据转换为 XML
xml_data = xmltodict.unparse(json_data, pretty=True)

# 手动删除 XML 声明部分
if xml_data.startswith('<?xml'):
    xml_data = xml_data.split('?>', 1)[1].strip()

# 保存 XML 数据到文件
with open('output.xml', 'w', encoding='utf-8') as xml_file:
    xml_file.write(xml_data)

print("处理完成，转换后的XML数据已保存到output.xml")
