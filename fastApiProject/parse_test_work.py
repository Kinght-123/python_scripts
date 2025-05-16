import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse('567.xml')
root = tree.getroot()

work_id = ""

cur_form_id = root.attrib.get('formId')

che_element = root.find('che')
che_id = che_element.attrib.get('CHID')

msid = root.attrib.get('MSID')
timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
work_id = che_id + "_" + str(abs(int(msid))) + "_" + timestamp

work_element = che_element.find('work')
move_stage = work_element.attrib.get('moveStage')

work_status = ""
if cur_form_id[-10:] == '_TO_ORIGIN' or cur_form_id[-10:] == '_AT_ORIGIN':
    work_status = "RECV"
elif cur_form_id[-14:] == '_LADEN_TO_DEST' or cur_form_id[-13:] == '_LADEN_AT_DES':
    work_status = "DELIVER"
elif cur_form_id[-19:] == '_CONFIRM_TRUCK_LANE':
    work_status = work_status
else:
    work_status = "FREE"

job_element = work_element.find('job')
container_element = job_element.find('container')
acrr = container_element.attrib.get('ACRR')
dcrr = container_element.attrib.get('DCRR')

count = work_element.attrib.get('count')

planning_intent = work_element.attrib.get('planningIntent')

pool = che_element.find('pool').attrib.get('name')

display_msg = che_element.find('displayMsg').text

print(f'work_id: {work_id}')
print(f'cur_form_id: {cur_form_id}')
print(f'che_id: {che_id}')
print(f'move_stage: {move_stage}')
print(f'work_status: {work_status}')
print(f'acrr: {acrr}')
print(f'dcrr: {dcrr}')
print(f'count: {count}')
print(f'planning_intent: {planning_intent}')
print(f'pool: {pool}')
print(f'display_msg: {display_msg}')






# 找到所有的<job>标签
jobs = root.findall('.//job')
# 将每个<job>标签转换为字典形式并添加到列表中
jobs_list = []
for job in jobs:
    job_dict = {
        'MVKD': job.attrib.get('MVKD', ''),
        'pow': job.attrib.get('pow', ''),
        'age': job.attrib.get('age', ''),
        'priority': job.attrib.get('priority', ''),
        'shift': job.attrib.get('shift', ''),
        'moveStage': job.attrib.get('moveStage', '')
        # 添加其他属性需要的键值对
    }
    jobs_list.append(job_dict)
# 打印结果
print(f'jobs_list: {jobs_list}')


# 将每个<job>标签及其子元素转换为字典形式并添加到列表中
jobs_list1 = []
for job in jobs:
    job_dict1 = {
        'MVKD': job.attrib.get('MVKD', ''),
        'pow': job.attrib.get('pow', ''),
        'age': job.attrib.get('age', ''),
        'priority': job.attrib.get('priority', ''),
        'shift': job.attrib.get('shift', ''),
        'moveStage': job.attrib.get('moveStage', '')
        # 添加其他属性需要的键值对
    }

    # 添加<container>和<position>的信息
    container = job.find('container')
    if container is not None:
        container_dict = {
            'EQID': container.attrib.get('EQID', ''),
            'LNTH': container.attrib.get('LNTH', ''),
            'QWGT': container.attrib.get('QWGT', ''),
            'MNRS': container.attrib.get('MNRS', ''),
            'QCAT': container.attrib.get('QCAT', ''),
            'EQTP': container.attrib.get('EQTP', ''),
            'HGHT': container.attrib.get('HGHT', ''),
            'LOPR': container.attrib.get('LOPR', ''),
            'TRKC': container.attrib.get('TRKC', ''),
            'ACRR': container.attrib.get('ACRR', ''),
            'DCRR': container.attrib.get('DCRR', ''),
            'RLSE': container.attrib.get('RLSE', ''),
            'RFRT': container.attrib.get('RFRT', ''),
            'CCON': container.attrib.get('CCON', ''),
            'ISHZ': container.attrib.get('ISHZ', ''),
            'DWTS': container.attrib.get('DWTS', ''),
            'ISGP': container.attrib.get('ISGP', ''),
            'GRAD': container.attrib.get('GRAD', ''),
            'RMRK': container.attrib.get('RMRK', ''),
            'JPOS': container.attrib.get('JPOS', ''),
            'PUTJPOS': container.attrib.get('PUTJPOS', '')
        }
        job_dict1['container'] = container_dict

    positions = job.findall('position')
    position_list = []
    for position in positions:
        position_dict = {
            'PPOS': position.attrib.get('PPOS', ''),
            'refID': position.attrib.get('refID', ''),
            'AREA': position.attrib.get('AREA', ''),
            'AREA_TYPE': position.attrib.get('AREA_TYPE', ''),
            'type': position.attrib.get('type', ''),
            'DOOR': position.attrib.get('DOOR', ''),
            'TKPS': position.attrib.get('TKPS', ''),
            'VBAY': position.attrib.get('VBAY', '')
        }
        position_list.append(position_dict)

    job_dict1['positions'] = position_list

    jobs_list1.append(job_dict1)

# 打印结果
print(f'jobs_list1: {jobs_list1}')
