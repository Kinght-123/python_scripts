import xml.etree.ElementTree as ET


def create_element(tag, attrib=None, text=None):
    """Helper function to create an XML element."""
    element = ET.Element(tag, attrib=attrib)
    if text:
        element.text = text
    return element


def create_container_element(eqid, lnth, qwgt, **kwargs):
    """Create a container XML element with given attributes."""
    attrib = {'EQID': eqid, 'LNTH': str(lnth), 'QWGT': str(qwgt)}
    attrib.update(kwargs)
    return create_element('container', attrib)


def create_position_element(ppos, refid, area, area_type, position_type, door, vbay=None):
    """Create a position XML element with given attributes."""
    attrib = {'PPOS': ppos, 'refID': refid, 'AREA': area, 'AREA_TYPE': area_type, 'type': position_type, 'DOOR': door}
    if vbay:
        attrib['VBAY'] = vbay
    return create_element('position', attrib)


def create_job_element(mvkd, pow_name, age, priority, shift, container, position_from, position_to):
    """Create a job XML element with given attributes and sub-elements."""
    job = create_element('job',
                         {'MVKD': mvkd, 'pow': pow_name, 'age': str(age), 'priority': priority, 'shift': str(shift)})
    job.append(container)
    job.append(position_from)
    job.append(position_to)
    return job


def create_task(
        che_id='A999',
        eqid='',
        lnth=0,
        qwgt=0,
        putjpos='',
        target='',
        from_ppos='',
        from_area='',
        from_area_type='YardRow',
        to_ppos='',
        to_area='',
        to_area_type='Vessel',
        from_id='',
        mvkd='',
        vbay='',
) -> str:
    """Create an XML string for a single task."""
    # Parameter validation
    if lnth < 0 or qwgt < 0:
        raise ValueError("Length and weight must be non-negative.")

    message = create_element("message", {"formId": from_id, "ack": "N", "MSID": "-5953245"})
    che = create_element("che", {
        "CHID": che_id,
        "equipType": "TRUCK",
        "MTEU": "2",
        "DSTA": "ICTY",
        "OPMD": "TRUCK",
        "CHASSIS": "BOMBCART",
        "status": "Working",
        "locale": "en_US",
        "location": target,
        "userID": "465006",
    })
    pool = create_element("pool", {"name": f"POOL_{target}"})
    pool_list = create_element("list", {"count": "1", "type": "pow"})
    pool_pow = create_element("pow", {"name": target, "mode": "TrucksOnly"})
    pool_list.append(pool_pow)
    pool.append(pool_list)
    work = create_element("work", {"count": "1", "moveStage": "PLANNED", "planningIntent": "SINGLE"})
    job = create_job_element(mvkd, target, 916, "N", "0",
                             create_container_element(eqid, lnth, qwgt, PUTJPOS=putjpos),
                             create_position_element(from_ppos, "Y.TECT:01B.56.01.1", from_area, from_area_type, "from",
                                                     "A"),
                             create_position_element(to_ppos, "V.WANGJLT_002:A.46.07.82", to_area, to_area_type, "to",
                                                     "Y", vbay))
    work.append(job)
    display_msg = create_element("displayMsg", {"msgID": "0"})
    display_msg.text = "No Error"
    che.append(pool)
    che.append(work)
    che.append(display_msg)
    message.append(che)
    xml_string = ET.tostring(message, encoding="unicode", method="xml")
    return xml_string


def create_two_tasks(
        che_id='A999',
        eqid_0='',
        eqid_1='',
        lnth_0=0,
        lnth_1=0,
        qgwt_0=0,
        qgwt_1=0,
        putjpos_0='',
        putjpos_1='',
        from_ppos='',
        from_area='',
        from_area_type='YardRow',
        to_ppos='',
        to_area='',
        to_area_type='Vessel',
        from_id='',
        mvkd='',
        target='',
        vbay='',
) -> str:
    """Create an XML string for two tasks."""
    # Parameter validation
    if lnth_0 < 0 or qgwt_0 < 0 or lnth_1 < 0 or qgwt_1 < 0:
        raise ValueError("Lengths and weights must be non-negative.")

    message = create_element("message", {"formId": from_id, "ack": "N", "MSID": "-106447"})
    che = create_element("che", {
        "CHID": che_id,
        "equipType": "TRUCK",
        "MTEU": "2",
        "DSTA": "ICTY",
        "OPMD": "TRUCK",
        "CHASSIS": "BOMBCART",
        "status": "Working",
        "locale": "en_US",
        "location": target,
        "userID": "160134",
    })
    pool = create_element("pool", {"name": f"{target} POOL"})
    pool_list = create_element("list", {"count": "1", "type": "pow"})
    pool_pow = create_element("pow", {"name": target, "mode": "TrucksOnly"})
    pool_list.append(pool_pow)
    pool.append(pool_list)
    work = create_element("work", {"count": "2", "moveStage": "PLANNED", "planningIntent": "TWIN"})

    job_0 = create_job_element(mvkd, target, 1164, "N", "7",
                               create_container_element(eqid_0, lnth_0, qgwt_0, PUTJPOS=putjpos_0),
                               create_position_element(f"{from_ppos}.1", "Y.FICT:B08.73.05.2", from_area,
                                                       from_area_type, "from", "Y"),
                               create_position_element(to_ppos, "V.XINDD_010:B.17.03.06", to_area, to_area_type, "to",
                                                       "Y", vbay))
    job_1 = create_job_element(mvkd, target, 1164, "N", "8",
                               create_container_element(eqid_1, lnth_1, qgwt_1, PUTJPOS=putjpos_1),
                               create_position_element(f"{from_ppos}.2", "Y.FICT:B08.73.05.1", from_area,
                                                       from_area_type, "from", "Y"),
                               create_position_element(to_ppos, "V.XINDD_010:B.19.03.06", to_area, to_area_type, "to",
                                                       "Y", vbay))

    work.append(job_0)
    work.append(job_1)
    display_msg = create_element("displayMsg", {"msgID": "0"})
    display_msg.text = "0 No Error"
    che.append(pool)
    che.append(work)
    che.append(display_msg)
    message.append(che)
    xml_string = ET.tostring(message, encoding="unicode", method="xml")
    return xml_string


# Example usage
if __name__ == "__main__":
    print(create_task())
    print(create_two_tasks())
