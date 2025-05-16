import xml.etree.ElementTree as ET
from datetime import datetime


def _get_work_status(form_id):
    if form_id.endswith('_TO_ORIGIN') or form_id.endswith('_AT_ORIGIN'):
        return "RECV"
    elif form_id.endswith('_LADEN_TO_DEST') or form_id.endswith('_LADEN_AT_DES'):
        return "DELIVER"
    elif form_id.endswith('_CONFIRM_TRUCK_LANE'):
        return form_id
    else:
        return "FREE"


class WorkElement:
    def __init__(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        self.cur_form_id = root.attrib.get('formId')

        che_element = root.find('che')
        self.che_id = che_element.attrib.get('CHID')

        self.msid = root.attrib.get('MSID')
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

        self.work_id = f"{self.che_id}_{abs(int(self.msid))}_{self.timestamp}"

        work_element = che_element.find('work')
        self.move_stage = work_element.attrib.get('moveStage')

        self.work_status = _get_work_status(self.cur_form_id)

        job_element = work_element.find('job')
        container_element = job_element.find('container')
        self.acrr = container_element.attrib.get('ACRR')
        self.dcrr = container_element.attrib.get('DCRR')

        self.count = work_element.attrib.get('count')
        self.planning_intent = work_element.attrib.get('planningIntent')

        self.pool = che_element.find('pool').attrib.get('name')

        self.display_msg = che_element.find('displayMsg').text

    def __str__(self):
        return (
            f'work_id: {self.work_id}\n'
            f'cur_form_id: {self.cur_form_id}\n'
            f'che_id: {self.che_id}\n'
            f'move_stage: {self.move_stage}\n'
            f'work_status: {self.work_status}\n'
            f'acrr: {self.acrr}\n'
            f'dcrr: {self.dcrr}\n'
            f'count: {self.count}\n'
            f'planning_intent: {self.planning_intent}\n'
            f'pool: {self.pool}\n'
            f'display_msg: {self.display_msg}'
        )


# 使用示例
if __name__ == "__main__":
    work = WorkElement('567.xml')
    print(work)
