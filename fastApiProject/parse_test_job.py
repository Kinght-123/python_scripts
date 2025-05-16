import xml.etree.ElementTree as ET
from datetime import datetime


tree = ET.parse('567.xml')
root = tree.getroot()


che_id = root.find('che').attrib.get('CHID')
msid = root.attrib.get('MSID')
timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
job_id = che_id + "_" + str(abs(int(msid))) + "_" + timestamp

job_status = ""
formId = root.attrib.get('formId')
if formId.endswith("_TO_ORIGIN") or formId.endswith("_TO_DEST"):
    job_status = "TO"
elif formId.endswith("_CONFIRM_TRUNK_LANE"):
    job_status = "TZ"
elif formId.endswith("_AT_ORIGIN") or formId.endswith("_LADEN_AT_DES"):
    job_status = "AT"

job_element = root.find('che/work/job')  # root.find('.//job') --- 查找根目录下的所有的job元素
move_kind = job_element.attrib.get('MVKD')
move_stage = job_element.attrib.get('moveStage')
pow = job_element.attrib.get('pow')
age = job_element.attrib.get('age')
ppos = [position.attrib.get('PPOS') for position in job_element.findall('position')]
type = [position.attrib.get('type') for position in job_element.findall('position')]
ref_id = [position.attrib.get('refID') for position in job_element.findall('position')]
area = [position.attrib.get('AREA') for position in job_element.findall('position')]
area_type = [position.attrib.get('AREA_TYPE') for position in job_element.findall('position')]
container_id = [container.attrib.get('EQID') for container in job_element.findall('container')]
container_length = [container.attrib.get('LNTH') for container in job_element.findall('container')]
container_weight = [container.attrib.get('QWGT') for container in job_element.findall('container')]
container_pos = [container.attrib.get('PUTJPOS') for container in job_element.findall('container')]
container_type = [container.attrib.get('EQTP') for container in job_element.findall('container')]
container_ishz = [container.attrib.get('ISHZ') for container in job_element.findall('container')]

print(f'job_id: {job_id}')
print(f'job_status: {job_status}')
print(f'move_kind: {move_kind}')
print(f'move_stage: {move_stage}')
print(f'pow: {pow}')
print(f'age: {age}')
print(f'ppos: {ppos}')
print(f'type: {type}')
print(f'ref_id: {ref_id}')
print(f'area: {area}')
print(f'area_type: {area_type}')
print(f'container_id: {container_id}')
print(f'container_length: {container_length}')
print(f'container_weight: {container_weight}')
print(f'container_pos: {container_pos}')
print(f'container_type: {container_type}')
print(f'container_ishz: {container_ishz}')
