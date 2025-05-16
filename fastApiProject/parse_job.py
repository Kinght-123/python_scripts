import xml.etree.ElementTree as ET
from datetime import datetime


def _generate_job_id(root):
    che_id = root.find('che').attrib.get('CHID')
    msid = root.attrib.get('MSID')
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{che_id}_{abs(int(msid))}_{timestamp}"


def _get_job_status(root):
    formId = root.attrib.get('formId')
    if formId.endswith("_TO_ORIGIN") or formId.endswith("_TO_DEST"):
        return "TO"
    elif formId.endswith("_CONFIRM_TRUNK_LANE"):
        return "TZ"
    elif formId.endswith("_AT_ORIGIN") or formId.endswith("_LADEN_AT_DES"):
        return "AT"
    else:
        return ""


class JobInfo:
    def __init__(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        self.job_id = _generate_job_id(root)
        self.job_status = _get_job_status(root)

        job_element = root.find('che/work/job')
        self.move_kind = job_element.attrib.get('MVKD')
        self.move_stage = job_element.attrib.get('moveStage')
        self.pow = job_element.attrib.get('pow')
        self.age = job_element.attrib.get('age')

        self.ppos = [position.attrib.get('PPOS') for position in job_element.findall('position')]
        self.type = [position.attrib.get('type') for position in job_element.findall('position')]
        self.ref_id = [position.attrib.get('refID') for position in job_element.findall('position')]
        self.area = [position.attrib.get('AREA') for position in job_element.findall('position')]
        self.area_type = [position.attrib.get('AREA_TYPE') for position in job_element.findall('position')]

        self.container_id = job_element.find('container').attrib.get('EQID')
        self.container_length = job_element.find('container').attrib.get('LNTH')
        self.container_weight = job_element.find('container').attrib.get('QWGT')
        self.container_pos = job_element.find('container').attrib.get('PUTJPOS')
        self.container_type = job_element.find('container').attrib.get('EQTP')
        self.container_ishz = job_element.find('container').attrib.get('ISHZ')

    def __str__(self):
        return (
            f'job_id: {self.job_id}\n'
            f'job_status: {self.job_status}\n'
            f'move_kind: {self.move_kind}\n'
            f'move_stage: {self.move_stage}\n'
            f'pow: {self.pow}\n'
            f'age: {self.age}\n'
            f'ppos: {self.ppos}\n'
            f'type: {self.type}\n'
            f'ref_id: {self.ref_id}\n'
            f'area: {self.area}\n'
            f'area_type: {self.area_type}\n'
            f'container_id: {self.container_id}\n'
            f'container_length: {self.container_length}\n'
            f'container_weight: {self.container_weight}\n'
            f'container_pos: {self.container_pos}\n'
            f'container_type: {self.container_type}\n'
            f'container_ishz: {self.container_ishz}'
        )


# 使用示例
if __name__ == "__main__":
    job_info = JobInfo('567.xml')
    print(job_info)
