from study_oneof_pb2 import ContactInfo

contact = ContactInfo()
contact.email = "123@qq.com"

# 使用HasField检查字段是否设置
is_phone_number = contact.HasField("phone_number")
is_email = contact.HasField("email")
print(is_phone_number, is_email)
encode_data = contact.SerializeToString()
print(encode_data)

contact.ParseFromString(encode_data)
print(contact.phone_number)
print(contact.email)
