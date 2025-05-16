# Copyright 2020, trunk Inc. All rights reserved
# !--*-- coding:UTF-8 --*--
import matplotlib
import re

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import json
from matplotlib.patches import Rectangle
from matplotlib import cm
from datetime import datetime

cm.colors
import sys
import math

legends = []

timestamp = []
timestamp2 = []
timestamp3 = []
tar_ind = []
final_speed = []
tar_speed = []
cur_speed = []
throttle_brake = []
lon_status = []

x_ref = []
y_ref = []
yaw = []
yaw_rate_true = []
yaw_rate_fake = []
steering = []
tag_yrate_limit = []
tag_time = []
obstacle = []
ob_time = []
ref_x1 = []
ref_y1 = []

ref_x3 = []
ref_y3 = []

head_width = 3.3  # 完整的车的宽度
head_width1 = 2.9
# head_width = 3.1

half_head_width = head_width / 2  # 1.75  一半的车的宽度
half_head_width1 = 1.45

head_length = 16.4  # 完整的车的长度
head_length1 = 15.4

head_base_2_front = 7.8
head_base_2_rear = head_length / 2  # 一半的车的长度
head_base_2_rear1 = head_length1 / 2

fig = plt.figure(figsize=(11, 6))
# plt.rcParams['font.sans-serif'] = ['sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.subplots_adjust(left=0.09, right=1, wspace=0.25,
                    hspace=0.25, bottom=0.13, top=0.91)


class Point(object):
    def __init__(self, *args):
        super(Point, self).__init__(*args)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.heading = 0


def normalizeAngle(theta):
    modify_theta = 0.0
    modify_theta = math.fmod(theta, 2 * math.pi)
    if modify_theta < 0:
        modify_theta += 2 * math.pi

    return modify_theta


def call_back(event):
    axtemp = event.inaxes
    x_min, x_max = axtemp.get_xlim()
    fanwei = (x_max - x_min) / 10
    if event.button == 'up':
        axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
        # print('up')
    elif event.button == 'down':
        axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
        # print('down')
    fig.canvas.draw_idle()  # 绘图动作实时反映在图像上


fig.canvas.mpl_connect('scroll_event', call_back)
fig.canvas.mpl_connect('button_press_event', call_back)
LANE_NAMES = []


def draw_lanes():
    ref_x4 = []
    ref_y4 = []
    ref_x3 = []
    ref_y3 = []
    ref_x2 = []
    ref_y2 = []
    ref_x1 = []
    ref_y1 = []
    left_x, left_y = [], []
    stream_left_x, stream_left_y = [], []
    right_x, right_y = [], []
    stream_right_x, stream_right_y = [], []
    rail_x, rail_y = [], []
    station_x, station_y = [], []
    station = []
    # 加载地图，生成车道中心线
    # with open(r'C:\Users\trunk\Projects\地图文件\oy\tj_oy_infra_v1.2.9.json', 'r') as c_art:
    # with open(r'/home/trunk/public/maps/hf_v1.7.2.json', 'r') as c_art:
    # with open(r'/home/trunk/public/maps/tj_c_high.json', 'r') as c_art:
    # with open(r'/home/trunk/downloads/tj_c_v5.6.16.json', 'r') as c_art:
    with open(r'tj_oy_v2.0.6.json', 'r') as c_art:
        # with open(r'C:\Users\trunk\Projects\地图文件\oy\tj_oy_infra_v1.2.6.json', 'r') as c_art:
        # with open(r'C:\Users\trunk\Projects\地图文件\tc\tj_c_high.json', 'r') as c_art:
        c_art_data = json.load(c_art)
    roads = c_art_data['roads']
    currentAxis = plt.gca()
    l = []
    for road in roads:
        laneSections = road['laneSections']
        for laneSection in laneSections:
            lanes = laneSection['lanes']
            for lane in lanes:
                turn = lane['turnType']
                lane_type = lane['type']
                points = lane['centerLine']
                lane_name = lane.get("name", "")
                uid = lane.get('uid', '1213_01111')
                # turn == 'noTurn' and
                # 车道中心线
                for point in points:
                    if (lane_type not in ['hatchcover', 'emergency', 'latitude'] and
                            len(points) > 5):
                        # if lane_type == 'yard_work':
                        #     ref_x4.append(point['x'])
                        #     ref_y4.append(point['y'])
                        # else:
                        ref_x2.append(point['x'])
                        ref_y2.append(point['y'])
                        LANE_NAMES.append(lane_name)
                        # if lane_type == 'yard_incoming_cross':
                        # if lane_type == 'cross':
                        #     l.extend([
                        #         {
                        #             "pos": {
                        #                 "x": point['x'],
                        #                 "y": point['y'],
                        #                 "z": 0
                        #             },
                        #             "heading": point['heading'],
                        #             "laneId": 3,
                        #             "direction": 2
                        #         }
                        #     ])

                # 主干道
                # for point in points:
                #     if (lane_type not in ['hatchcover', 'emergency', 'yard_change', 'latitude'] and
                #             len(points) > 5):
                #         ref_x1.append(point['x'])
                #         ref_y1.append(point['y'])
                #     elif lane_type != 'hatchcover' and lane_type != 'emergency' and lane_type == "latitude":
                #         ref_x3.append(point['x'])
                #         ref_y3.append(point['y'])

                # 围栏线
                for point in points:
                    if lane_type in ["emergency"] and len(points) > 5:
                        # print(point)
                        rail_x.append(point['x'])
                        rail_y.append(point['y'])

                # left
                lps = lane['leftBorder']['pointSet']
                for point in lps:
                    if (turn == 'noTurn' and lane_type != 'hatchcover' and lane_type != 'emergency' and
                            len(points) > 5):
                        if lane_type == 'longitude':
                            stream_left_x.append(point['x'])
                            stream_left_y.append(point['y'])
                        else:
                            left_x.append(point['x'])
                            left_y.append(point['y'])

                # right
                lps = lane['rightBorder']['pointSet']
                for point in lps:
                    if (turn == 'noTurn' and lane_type != 'hatchcover' and lane_type != 'emergency' and
                            len(points) > 5):
                        if lane_type == 'longitude':
                            stream_right_x.append(point['x'])
                            stream_right_y.append(point['y'])
                        else:
                            right_x.append(point['x'])
                            right_y.append(point['y'])

                if lane_type == 'lockzone':
                    left_border = lane['leftBorder']
                    right_border = lane['rightBorder']
                    lock_station = []
                    if len(left_border) > 1 and len(right_border) > 1:
                        left_start_point = lane['leftBorder']['pointSet'][0]
                        left_end_point = lane['leftBorder']['pointSet'][-1]
                        right_start_point = lane['rightBorder']['pointSet'][0]
                        right_end_point = lane['rightBorder']['pointSet'][-1]
                        station.append(
                            [[left_start_point['x'], left_start_point['y']], [left_end_point['x'], left_end_point['y']],
                             [right_end_point['x'], right_end_point['y']],
                             [right_start_point['x'], right_start_point['y']]
                             ])
                        station_x.append(left_start_point['x'])
                        station_x.append(left_end_point['x'])
                        station_x.append(right_end_point['x'])
                        station_x.append(right_start_point['x'])

                        station_y.append(left_start_point['y'])
                        station_y.append(left_end_point['y'])
                        station_y.append(right_end_point['y'])
                        station_y.append(right_start_point['y'])
                        # head shape
                        # rect = Rectangle((right_rear_x, right_rear_y), head_length, head_width,
                        #                  color=rect_clr, fill=False, angle=utm_theta * 57.2958)  # alpha
                        # currentAxis.add_patch(rect)
                        # lock_station.append([left_start_point['x'], left_start_point['y']])
                        # lock_station.append([left_end_point['x'], left_end_point['y']])
                        # lock_station.append([right_end_point['x'], right_end_point['y']])
                        # lock_station.append([right_start_point['x'], right_start_point['y']])
                        # print("lock_station:")
                        # print(lock_station)

                    # self.lock_stations.append(lock_station)
    # with open('che_yard_zw.json', 'w') as f:
    #     f.write(json.dumps(l))
    plt.scatter(left_x, left_y, color='grey',
                alpha=0.2, s=1, label='left line')

    plt.scatter(right_x, right_y, color='grey',
                alpha=0.2, s=1, label='right line')

    plt.scatter(stream_left_x, stream_left_y, color='grey',
                alpha=0.2, s=1, label='left stream line')

    plt.scatter(stream_right_x, stream_right_y, color='grey',
                alpha=0.2, s=1, label='right stream line')

    plt.plot(rail_x, rail_y, 'm.', markersize=.8, label="rail line")
    plt.plot(ref_x1, ref_y1, 'g.', markersize=.8, label="center line")
    plt.plot(ref_x2, ref_y2, 'c.', markersize=.8, label="change line")
    plt.plot(ref_x4, ref_y4, 'r.', markersize=.8, label="change line")
    plt.plot(left_x, left_y, 'c.', markersize=.8, label="left line")
    plt.plot(right_x, right_y, 'c.', markersize=.8, label="right line")
    plt.plot(station_x, station_y, 'r.', markersize=1, label="right line")


def graph_generate(tos_path, None_clr, stright_clr, turn_clr, lanechange_clr, rect_clr, yellow="y.", offset=1):
    # HUAWEI params

    if offset == 1:
        # C段
        offset_x = 565123
        offset_y = 4317123

        # 合肥
        # offset_x = 536297.95
        # offset_y = 3518336.344
    else:
        offset_x = 0
        offset_y = 0
    # offset_x = 536297.95
    # offset_y = 3518336.344
    x_pos = []
    y_pos = []
    x_pos_type1 = []
    y_pos_type1 = []
    x_pos_type2 = []
    y_pos_type2 = []
    x_pos_type3 = []
    y_pos_type3 = []
    x_pos_type4 = []
    y_pos_type4 = []
    x_pos_type5 = []
    y_pos_type5 = []
    x_pos_type6 = []
    y_pos_type6 = []
    delat_theta = 0.0125
    currentAxis = plt.gca()
    for path_point in tos_path:
        point = path_point.get(
            'pos', path_point)

        if point.get('longitude'):
            utm_x = point.get('longitude') + offset_x
            utm_y = point.get('latitude') + offset_y
        else:
            utm_x = point.get('x')
            utm_y = point.get('y')

        type = path_point.get('type')
        if type == 'STRAIGHT' or type == 1:
            x_pos_type1.append(utm_x)
            y_pos_type1.append(utm_y)
        elif type == 'TURN' or type == 2:
            x_pos_type2.append(utm_x)
            y_pos_type2.append(utm_y)
        elif type in ['LANECHANGE', "LANE_CHANGE_NORMAL", "LANE_CHANGE_ENTER_STATION", "ENTER_STATION_8",
                      "LANE_CHANGE_ENTER_WORKING_LANE"] or type == 3:
            x_pos_type3.append(utm_x)
            y_pos_type3.append(utm_y)
        elif type == "ART1":
            x_pos_type4.append(utm_x)
            y_pos_type4.append(utm_y)
        elif type == "ART2":
            x_pos_type5.append(utm_x)
            y_pos_type5.append(utm_y)
        elif type == "STOP":
            x_pos_type6.append(utm_x)
            y_pos_type6.append(utm_y)
        else:
            x_pos.append(utm_x)
            y_pos.append(utm_y)

        if offset:
            heading = path_point['heading'] * delat_theta * math.pi / 180
            utm_theta = 3.14 / 2 - normalizeAngle(heading)
        else:
            utm_theta = path_point['heading']
        # head contours
        right_rear_x = utm_x + half_head_width * \
                       math.sin(utm_theta) - head_base_2_rear * math.cos(utm_theta)
        right_rear_y = utm_y - half_head_width * \
                       math.cos(utm_theta) - head_base_2_rear * math.sin(utm_theta)

        # head shape
        if path_point.get('che_type', 0) == 1:
            rect = Rectangle((right_rear_x, right_rear_y), 10.49, 2.55,
                             color=rect_clr, fill=False, angle=utm_theta * 57.2958)  # alpha
        else:
            rect = Rectangle((right_rear_x, right_rear_y), head_length, head_width,
                             color=rect_clr, fill=False, angle=utm_theta * 57.2958)  # alpha
        currentAxis.add_patch(rect)
        # if type == 'STRAIGHT' or type == 1:
        #     # if type == 'LANECHANGE' or type == 3:
        #     currentAxis.add_patch(rect)

    plt.plot(x_pos, y_pos, None_clr, markersize=4.0, label='None points')
    plt.plot(x_pos_type1, y_pos_type1, stright_clr,
             markersize=6.0, label='straight')
    plt.plot(x_pos_type2, y_pos_type2, turn_clr, markersize=6.0, label='turn')
    plt.plot(x_pos_type3, y_pos_type3, lanechange_clr,
             markersize=6.0, label='lanechange')
    if x_pos_type4:
        plt.plot(x_pos_type4, y_pos_type4, yellow, markersize=6.0, label='ART1')
    if x_pos_type5:
        plt.plot(x_pos_type5, y_pos_type5, "g.", markersize=6.0, label='ART2')
    if x_pos_type6:
        plt.plot(x_pos_type6, y_pos_type6, "b.", markersize=6.0, label='STOP')


def graph_generate1(tos_path, None_clr, stright_clr, turn_clr, lanechange_clr, rect_clr, yellow="y.", offset=1):
    # HUAWEI params

    if offset == 1:
        # C段
        offset_x = 565123
        offset_y = 4317123

        # 合肥
        # offset_x = 536297.95
        # offset_y = 3518336.344
    else:
        offset_x = 0
        offset_y = 0
    # offset_x = 536297.95
    # offset_y = 3518336.344
    x_pos = []
    y_pos = []
    x_pos_type1 = []
    y_pos_type1 = []
    x_pos_type2 = []
    y_pos_type2 = []
    x_pos_type3 = []
    y_pos_type3 = []
    x_pos_type4 = []
    y_pos_type4 = []
    x_pos_type5 = []
    y_pos_type5 = []
    x_pos_type6 = []
    y_pos_type6 = []
    delat_theta = 0.0125
    currentAxis = plt.gca()
    for path_point in tos_path:
        point = path_point.get(
            'pos', path_point)

        if point.get('longitude'):
            utm_x = point.get('longitude') + offset_x
            utm_y = point.get('latitude') + offset_y
        else:
            utm_x = point.get('x')
            utm_y = point.get('y')

        type = path_point.get('type')
        if type == 'STRAIGHT' or type == 1:
            x_pos_type1.append(utm_x)
            y_pos_type1.append(utm_y)
        elif type == 'TURN' or type == 2:
            x_pos_type2.append(utm_x)
            y_pos_type2.append(utm_y)
        elif type in ['LANECHANGE', "LANE_CHANGE_NORMAL", "LANE_CHANGE_ENTER_STATION", "ENTER_STATION_8",
                      "LANE_CHANGE_ENTER_WORKING_LANE"] or type == 3:
            x_pos_type3.append(utm_x)
            y_pos_type3.append(utm_y)
        elif type == "ART1":
            x_pos_type4.append(utm_x)
            y_pos_type4.append(utm_y)
        elif type == "ART2":
            x_pos_type5.append(utm_x)
            y_pos_type5.append(utm_y)
        elif type == "STOP":
            x_pos_type6.append(utm_x)
            y_pos_type6.append(utm_y)
        else:
            x_pos.append(utm_x)
            y_pos.append(utm_y)

        if offset:
            heading = path_point['heading'] * delat_theta * math.pi / 180
            utm_theta = 3.14 / 2 - normalizeAngle(heading)
        else:
            utm_theta = path_point['heading']
        # head contours
        right_rear_x = utm_x + half_head_width1 * \
                       math.sin(utm_theta) - head_base_2_rear1 * math.cos(utm_theta)
        right_rear_y = utm_y - half_head_width1 * \
                       math.cos(utm_theta) - head_base_2_rear1 * math.sin(utm_theta)

        # head shape
        if path_point.get('che_type', 0) == 1:
            rect = Rectangle((right_rear_x, right_rear_y), 10.49, 2.55,
                             color=rect_clr, fill=False, angle=utm_theta * 57.2958)  # alpha
        else:
            rect = Rectangle((right_rear_x, right_rear_y), head_length1, head_width1,
                             color=rect_clr, fill=False, angle=utm_theta * 57.2958)  # alpha
        currentAxis.add_patch(rect)
        # if type == 'STRAIGHT' or type == 1:
        #     # if type == 'LANECHANGE' or type == 3:
        #     currentAxis.add_patch(rect)

    plt.plot(x_pos, y_pos, None_clr, markersize=4.0, label='None points')
    plt.plot(x_pos_type1, y_pos_type1, stright_clr,
             markersize=6.0, label='straight')
    plt.plot(x_pos_type2, y_pos_type2, turn_clr, markersize=6.0, label='turn')
    plt.plot(x_pos_type3, y_pos_type3, lanechange_clr,
             markersize=6.0, label='lanechange')
    if x_pos_type4:
        plt.plot(x_pos_type4, y_pos_type4, yellow, markersize=6.0, label='ART1')
    if x_pos_type5:
        plt.plot(x_pos_type5, y_pos_type5, "g.", markersize=6.0, label='ART2')
    if x_pos_type6:
        plt.plot(x_pos_type6, y_pos_type6, "b.", markersize=6.0, label='STOP')


def knn(index, data, k):
    labels, distances = index.knn_query(data, k=k, num_threads=1)
    return labels, distances


def read_and_process_file(file_path, offset, color, tag=1):
    x_pos1 = []
    y_pos1 = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(data)
    # tos_path = data['body']['pathGuidance']
    if tag == 1:
        draw_lanes()
        graph_generate(data if type(data) is list else data['body']["pathGuidance"]["points"], 'r.', 'k.', 'm.', 'b.',
                       color,
                       "y.", int(offset))
    elif tag == 0:
        draw_lanes()
        graph_generate1(data if type(data) is list else data['body']["pathGuidance"]["points"], 'r.', 'k.', 'm.', 'b.',
                        color,
                        "y.", int(offset))


if __name__ == "__main__":
    offset = 0
    day = datetime.now().strftime("%Y_%m_%d")
    fname = f'json_files/{day}/A532_A532_ab1231b1-ffc7-46a7-a38f-22852bbb326d_32_waypoints_05-14.json'
    # fname = 'json_files/a.json'
    read_and_process_file(fname, offset, 'green', tag=1)
    fname1 = f'json_files/{day}/A534_A534_fa7ab996-a45c-4143-bc20-c591ec5610a7_23_waypoints_05-14.json'
    read_and_process_file(fname1, offset, 'red', tag=1)
    plt.axis('equal')
    plt.legend(loc="upper right")
    plt.grid()
    plt.title(fname)
    plt.show()
    # tos_path = data['body']['pathGuidance']

    # if len(sys.argv) > 3:
    #     fname = sys.argv[3]
    #     offset = 1
    #     if len(sys.argv) > 4:
    #         offset = sys.argv[4]
    #     with open(fname) as f:
    #         data = json.load(f)
    #         graph_generate(data if type(data) is list else data["pathGuidance"]["points"], 'darkcyan', '', '', '',
    #                        'blueviolet', "y.", int(offset))
    # graph_generate(data, 'darkcyan', '', '', '', 'blueviolet', 1)

    # if len(sys.argv) > 2:a
    #     fname = sys.argv[2]

    #     with open(fname) as f:
    #         data = json.load(f)
    #     tos_path = data['body']['pathGuidance']
    #     graph_generate(tos_path, 'b.', x_pos1, y_pos1, offset)

    # legends.append("position")
    # legends.append("vehicle traj")

    # plt.legend(legends, loc="upper right")

    # save_name = os.path.join('轨迹图', os.path.basename(fname)[:-5] + '.png')
    # plt.savefig(save_name)
    # plt.get_current_fig_manager().window.state('zoomed')

# if __name__ == "__main__":
#     # with open("/home/trunk/downloads/t.log", "r") as f:
#     #     data = f.readlines()
#     # ['566844.5469669513', ' 4317790.820849643', ' 0.227783962354661', ' 54.49083628195245', ' 566903.8991543683',
#     #  ' 4317784.09108331', ' -0.5845919354015865', ' 566896.275701371', ' 4317795.17444032']
#     data = [
#         "2024-11-18 13:59:27,211[handler.py][line:865][INFO]: 缓停-A527-A531-DDTCS-5b76140ab60d46b0853b8835f7092a53{'x': 566904, 'y': 4317793} 31.805481751874623[566892.8638223228, 4317815.6102249, -1.3489832212136788, 31.805481751874623, 566922.1405278797, 4317797.032039717, 0.22808697474984824, 566906.3059049528, 4317793.369020077] 执行急停车->执行缓停，距离停车点31.805481751874623m [[566904.7607860889, 4317793.070002846]]"
#     ]
#     l = []
#     for line in data[::-1]:
#         li = []
#         # points = line.split("]:")[1].split('[')[0].split({')[1].split('})[0].split(',')
#         #
#         # l_points = line.split("]:")[1].split('[')[1].split(']')[0].split(',')
#         # stop_point = line.split({')[1].split('})[0]
#         # che1_points = [float("{:.2f}".format(float(l_points[0]))), float("{:.2f}".format(float(l_points[1])))]
#
#         coordinates = re.search(r"\{'x': (\d+), 'y': (\d+)\}", line)
#         numbers =  re.findall(r"-?\d+\.\d+", line)
#         values = re.findall(r"\[([\d., -]+)\]", line)
#         coordinates = eval(coordinates.group())
#         # if l == che1_points:
#         #     continue
#         #
#         # l = che1_points
#         print(numbers, type(numbers))
#         che1 = {
#             "pos": {
#                 "x": float(numbers[1]),
#                 "y": float(numbers[2]),
#             },
#             "type": "ART1",
#             "heading": float(numbers[3])
#         }
#         che2 = {
#             "pos": {
#                 "x": float(numbers[5]),
#                 "y": float(numbers[6]),
#             },
#             "type": "ART2",
#             "heading": float(numbers[7])
#         }
#
#         pz = {
#             "pos": {
#                 "x": float(numbers[8]),
#                 "y": float(numbers[9]),
#             },
#             "type": "STOP",
#             "heading": float(numbers[7])
#         }
#         stop = {
#             "pos": {
#                 'x': float(coordinates['x']), 'y': float(coordinates['y'])
#             },
#             "type": "STOP",
#             "heading": float(numbers[7])
#         }
#         # stop_1 = {
#         #     "pos": {
#         #         'x': 566912.6031537441,  'y': 4317916.186104838
#         #     },
#         #     "type": 5,
#         #     "heading": float(numbers[7])
#         # }
#         li.extend([stop, che1, che2])
#         li.extend([{"driving_direction":1,"heading":-1.3431687247133155,"id":"1899_0","lane_type":7,"pos":{"x":566892.6852805645,"y":4317816.419179646,"yaw":-1.3431687247133155,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3431686349271121,"id":"1900_0","lane_type":7,"pos":{"x":566892.8007804541,"y":4317815.92056643,"yaw":-1.3431686349271121,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3431694982896094,"id":"1900_0","lane_type":7,"pos":{"x":566892.9160266585,"y":4317815.423048373,"yaw":-1.3431694982896094,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.343168336696528,"id":"1900_0","lane_type":7,"pos":{"x":566893.031284034,"y":4317814.925482087,"yaw":-1.343168336696528,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3431691006983244,"id":"1900_0","lane_type":7,"pos":{"x":566893.1465409562,"y":4317814.42791776,"yaw":-1.3431691006983244,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3431691395407979,"id":"1900_0","lane_type":7,"pos":{"x":566893.2617965956,"y":4317813.930358969,"yaw":-1.3431691395407979,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775583240488,"id":"1073_0","lane_type":3,"pos":{"x":566893.3770533329,"y":4317813.432771988,"yaw":-1.3417775583240488,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417777661150843,"id":"1073_0","lane_type":3,"pos":{"x":566893.4942335924,"y":4317812.930086443,"yaw":-1.3417777661150843,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775880435352,"id":"1073_0","lane_type":3,"pos":{"x":566893.6114264699,"y":4317812.42734677,"yaw":-1.3417775880435352,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776309107237,"id":"1073_0","lane_type":3,"pos":{"x":566893.7286152837,"y":4317811.924624527,"yaw":-1.3417776309107237,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775253805602,"id":"1073_0","lane_type":3,"pos":{"x":566893.8458055742,"y":4317811.421895951,"yaw":-1.3417775253805602,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417779079259542,"id":"1073_0","lane_type":3,"pos":{"x":566893.9629942543,"y":4317810.919174282,"yaw":-1.3417779079259542,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417777034632943,"id":"1073_0","lane_type":3,"pos":{"x":566894.0801840137,"y":4317810.416447984,"yaw":-1.3417777034632943,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775979335278,"id":"1073_0","lane_type":3,"pos":{"x":566894.1973739528,"y":4317809.913720915,"yaw":-1.3417775979335278,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417773835615932,"id":"1073_0","lane_type":3,"pos":{"x":566894.314563652,"y":4317809.410994875,"yaw":-1.3417773835615932,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775914768213,"id":"1901_0","lane_type":3,"pos":{"x":566894.4317477054,"y":4317808.9082930535,"yaw":-1.3417775914768213,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775027403942,"id":"1901_0","lane_type":3,"pos":{"x":566894.5440612368,"y":4317808.426485175,"yaw":-1.3417775027403942,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417777277799705,"id":"1901_0","lane_type":3,"pos":{"x":566894.6563924971,"y":4317807.9446012415,"yaw":-1.3417777277799705,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776988849388,"id":"1901_0","lane_type":3,"pos":{"x":566894.7687217661,"y":4317807.46272585,"yaw":-1.3417776988849388,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417774676820429,"id":"1901_0","lane_type":3,"pos":{"x":566894.8810563372,"y":4317806.980827715,"yaw":-1.3417774676820429,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.341777566762417,"id":"1901_0","lane_type":3,"pos":{"x":566894.9933828982,"y":4317806.498963941,"yaw":-1.341777566762417,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775419893885,"id":"1901_0","lane_type":3,"pos":{"x":566895.1057148302,"y":4317806.017077126,"yaw":-1.3417775419893885,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776513933861,"id":"1901_0","lane_type":3,"pos":{"x":566895.2180407504,"y":4317805.5352161005,"yaw":-1.3417776513933861,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417777091990348,"id":"1901_0","lane_type":3,"pos":{"x":566895.330369901,"y":4317805.053341217,"yaw":-1.3417777091990348,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776018564762,"id":"1901_0","lane_type":3,"pos":{"x":566895.4426993986,"y":4317804.571464846,"yaw":-1.3417776018564762,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775461200419,"id":"1901_0","lane_type":3,"pos":{"x":566895.5550289217,"y":4317804.089588365,"yaw":-1.3417775461200419,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417775853346656,"id":"1901_0","lane_type":3,"pos":{"x":566895.6673582498,"y":4317803.60771272,"yaw":-1.3417775853346656,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776410719842,"id":"1901_0","lane_type":3,"pos":{"x":566895.779683877,"y":4317803.125852952,"yaw":-1.3417776410719842,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417776080566761,"id":"1901_0","lane_type":3,"pos":{"x":566895.8920136244,"y":4317802.643975509,"yaw":-1.3417776080566761,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3417773830265587,"id":"1901_0","lane_type":3,"pos":{"x":566896.0043472255,"y":4317802.162081534,"yaw":-1.3417773830265587,"z":0},"speeds":{"vmax":20,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":-1.3822212091916148,"id":"1916_0","lane_type":4,"pos":{"x":566896.1166668963,"y":4317801.680247324,"yaw":-1.3822212091916148,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3798002401674905,"id":"1916_0","lane_type":4,"pos":{"x":566896.2157159407,"y":4317801.161285852,"yaw":-1.3798002401674905,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3761850309029426,"id":"1916_0","lane_type":4,"pos":{"x":566896.3190125279,"y":4317800.633520164,"yaw":-1.3761850309029426,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.374180052661498,"id":"1916_0","lane_type":4,"pos":{"x":566896.4229343208,"y":4317800.10989708,"yaw":-1.374180052661498,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3734791738845493,"id":"1916_0","lane_type":4,"pos":{"x":566896.5278307656,"y":4317799.5851568915,"yaw":-1.3734791738845493,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3742053508322853,"id":"1916_0","lane_type":4,"pos":{"x":566896.6328209715,"y":4317799.060005568,"yaw":-1.3742053508322853,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3763893149637296,"id":"1916_0","lane_type":4,"pos":{"x":566896.7368992099,"y":4317798.535317272,"yaw":-1.3763893149637296,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3799224488262924,"id":"1916_0","lane_type":4,"pos":{"x":566896.8394113216,"y":4317798.010535691,"yaw":-1.3799224488262924,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3854615214553365,"id":"1916_0","lane_type":4,"pos":{"x":566896.9397425095,"y":4317797.485177567,"yaw":-1.3854615214553365,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3935351093108979,"id":"1916_0","lane_type":4,"pos":{"x":566897.036250964,"y":4317796.959843374,"yaw":-1.3935351093108979,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4031280984404368,"id":"1916_0","lane_type":4,"pos":{"x":566897.129830084,"y":4317796.422690822,"yaw":-1.4031280984404368,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4154893368641204,"id":"1916_0","lane_type":4,"pos":{"x":566897.2139837521,"y":4317795.907783525,"yaw":-1.4154893368641204,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4289373485008317,"id":"1916_0","lane_type":4,"pos":{"x":566897.2930132824,"y":4317795.377673287,"yaw":-1.4289373485008317,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.440560264225289,"id":"1916_0","lane_type":4,"pos":{"x":566897.364697766,"y":4317794.850879942,"yaw":-1.440560264225289,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.451381688211446,"id":"1916_0","lane_type":4,"pos":{"x":566897.4315835055,"y":4317794.3183452,"yaw":-1.451381688211446,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4620093080609877,"id":"1916_0","lane_type":4,"pos":{"x":566897.49123094,"y":4317793.794010833,"yaw":-1.4620093080609877,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4703817255799152,"id":"1916_0","lane_type":4,"pos":{"x":566897.5467964938,"y":4317793.262255479,"yaw":-1.4703817255799152,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.476094900605073,"id":"1916_0","lane_type":4,"pos":{"x":566897.5975753046,"y":4317792.737862504,"yaw":-1.476094900605073,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.482992305802851,"id":"1916_0","lane_type":4,"pos":{"x":566897.6471938086,"y":4317792.205121413,"yaw":-1.482992305802851,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4904015346760413,"id":"1916_0","lane_type":4,"pos":{"x":566897.6912554317,"y":4317791.672409056,"yaw":-1.4904015346760413,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4926057025573258,"id":"1916_0","lane_type":4,"pos":{"x":566897.7329366163,"y":4317791.141138633,"yaw":-1.4926057025573258,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5111267825019006,"id":"1916_0","lane_type":4,"pos":{"x":566897.774513094,"y":4317790.610169258,"yaw":-1.5111267825019006,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5447389587659346,"id":"1916_0","lane_type":4,"pos":{"x":566897.7960078748,"y":4317790.07686324,"yaw":-1.5447389587659346,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5615179217512625,"id":"1916_0","lane_type":4,"pos":{"x":566897.8021885867,"y":4317789.542769296,"yaw":-1.5615179217512625,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5678281236056857,"id":"1916_0","lane_type":4,"pos":{"x":566897.8060855214,"y":4317789.00885755,"yaw":-1.5678281236056857,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5634752342216858,"id":"1916_0","lane_type":4,"pos":{"x":566897.8052290597,"y":4317788.474531072,"yaw":-1.5634752342216858,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5397997976371092,"id":"1916_0","lane_type":4,"pos":{"x":566897.8144322037,"y":4317787.94024873,"yaw":-1.5397997976371092,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.5130761437943336,"id":"1916_0","lane_type":4,"pos":{"x":566897.8388039478,"y":4317787.407415781,"yaw":-1.5130761437943336,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4825651874880712,"id":"1916_0","lane_type":4,"pos":{"x":566897.8761647546,"y":4317786.876431657,"yaw":-1.4825651874880712,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4484936396420816,"id":"1916_0","lane_type":4,"pos":{"x":566897.9329805605,"y":4317786.348608141,"yaw":-1.4484936396420816,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.4072521473533814,"id":"1916_0","lane_type":4,"pos":{"x":566898.0057025389,"y":4317785.823624929,"yaw":-1.4072521473533814,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.3475739267800895,"id":"1916_0","lane_type":4,"pos":{"x":566898.1054505175,"y":4317785.303541361,"yaw":-1.3475739267800895,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.2787922747496414,"id":"1916_0","lane_type":4,"pos":{"x":566898.2394892487,"y":4317784.791354036,"yaw":-1.2787922747496414,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.212957143276633,"id":"1916_0","lane_type":4,"pos":{"x":566898.408860844,"y":4317784.28981977,"yaw":-1.212957143276633,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.1515643498298318,"id":"1916_0","lane_type":4,"pos":{"x":566898.609367152,"y":4317783.798145732,"yaw":-1.1515643498298318,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.0797324501518382,"id":"1916_0","lane_type":4,"pos":{"x":566898.8392814472,"y":4317783.320699647,"yaw":-1.0797324501518382,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-1.0071110863661574,"id":"1916_0","lane_type":4,"pos":{"x":566899.1063576662,"y":4317782.862117761,"yaw":-1.0071110863661574,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.9405193720699073,"id":"1916_0","lane_type":4,"pos":{"x":566899.4050444628,"y":4317782.4205627665,"yaw":-0.9405193720699073,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.8709707634760558,"id":"1916_0","lane_type":4,"pos":{"x":566899.7316296608,"y":4317782.000650557,"yaw":-0.8709707634760558,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.8029071833426005,"id":"1916_0","lane_type":4,"pos":{"x":566900.0879405951,"y":4317781.604351567,"yaw":-0.8029071833426005,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.7351621591690728,"id":"1916_0","lane_type":4,"pos":{"x":566900.469592098,"y":4317781.232319836,"yaw":-0.7351621591690728,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.6676637417612383,"id":"1916_0","lane_type":4,"pos":{"x":566900.8764381157,"y":4317780.887023408,"yaw":-0.6676637417612383,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.600669047190639,"id":"1916_0","lane_type":4,"pos":{"x":566901.3055526197,"y":4317780.569447841,"yaw":-0.600669047190639,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.5304641033588772,"id":"1916_0","lane_type":4,"pos":{"x":566901.7551902868,"y":4317780.281575829,"yaw":-0.5304641033588772,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.4629725178801371,"id":"1916_0","lane_type":4,"pos":{"x":566902.2242113708,"y":4317780.02671014,"yaw":-0.4629725178801371,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.4021724897460829,"id":"1916_0","lane_type":4,"pos":{"x":566902.7089141301,"y":4317779.802328697,"yaw":-0.4021724897460829,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.33313458218196024,"id":"1916_0","lane_type":4,"pos":{"x":566903.2070349571,"y":4317779.606788233,"yaw":-0.33313458218196024,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.25638796706017125,"id":"1916_0","lane_type":4,"pos":{"x":566903.7162302758,"y":4317779.45066876,"yaw":-0.25638796706017125,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.1863936290312516,"id":"1916_0","lane_type":4,"pos":{"x":566904.2378918766,"y":4317779.333247892,"yaw":-0.1863936290312516,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.12498167215095164,"id":"1916_0","lane_type":4,"pos":{"x":566904.7656045386,"y":4317779.25019441,"yaw":-0.12498167215095164,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":-0.06367167034225399,"id":"1916_0","lane_type":4,"pos":{"x":566905.2972580795,"y":4317779.19833217,"yaw":-0.06367167034225399,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.008255404457393228,"id":"1916_0","lane_type":4,"pos":{"x":566905.8306450159,"y":4317779.180640823,"yaw":0.008255404457393228,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.08127495296271096,"id":"1916_0","lane_type":4,"pos":{"x":566906.3634208934,"y":4317779.204402866,"yaw":0.08127495296271096,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.13369432366073936,"id":"1916_0","lane_type":4,"pos":{"x":566906.8923939816,"y":4317779.26411151,"yaw":0.13369432366073936,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.1629913698754237,"id":"1916_0","lane_type":4,"pos":{"x":566907.4193544255,"y":4317779.344561923,"yaw":0.1629913698754237,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.17899625081957632,"id":"1916_0","lane_type":4,"pos":{"x":566907.94541858,"y":4317779.436269181,"yaw":0.17899625081957632,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.18838210993612486,"id":"1916_0","lane_type":4,"pos":{"x":566908.4711968533,"y":4317779.534351245,"yaw":0.18838210993612486,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.19513078737033587,"id":"1916_0","lane_type":4,"pos":{"x":566909.0002077197,"y":4317779.637119513,"yaw":0.19513078737033587,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2068001661937584,"id":"1916_0","lane_type":4,"pos":{"x":566909.4893782784,"y":4317779.735475182,"yaw":0.2068001661937584,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.21547964774884742,"id":"1916_0","lane_type":4,"pos":{"x":566910.0326290121,"y":4317779.852396745,"yaw":0.21547964774884742,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22085849948424946,"id":"1916_0","lane_type":4,"pos":{"x":566910.5518264188,"y":4317779.967590166,"yaw":0.22085849948424946,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22447298070956315,"id":"1916_0","lane_type":4,"pos":{"x":566911.0769975337,"y":4317780.086611402,"yaw":0.22447298070956315,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22673063359701506,"id":"1916_0","lane_type":4,"pos":{"x":566911.5929602243,"y":4317780.205133845,"yaw":0.22673063359701506,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2280927638990894,"id":"1916_0","lane_type":4,"pos":{"x":566912.1201645448,"y":4317780.327178993,"yaw":0.2280927638990894,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22901601689916046,"id":"1916_0","lane_type":4,"pos":{"x":566912.6393528533,"y":4317780.447986702,"yaw":0.22901601689916046,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22960207490255638,"id":"1916_0","lane_type":4,"pos":{"x":566913.1641965411,"y":4317780.570520956,"yaw":0.22960207490255638,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22995060712121568,"id":"1916_0","lane_type":4,"pos":{"x":566913.6849111052,"y":4317780.692344546,"yaw":0.22995060712121568,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2300969881629322,"id":"1916_0","lane_type":4,"pos":{"x":566914.2068915891,"y":4317780.814600045,"yaw":0.2300969881629322,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.23005539210406373,"id":"1916_0","lane_type":4,"pos":{"x":566914.7292673934,"y":4317780.936977897,"yaw":0.23005539210406373,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2298256824215265,"id":"1916_0","lane_type":4,"pos":{"x":566915.2519858431,"y":4317781.059362505,"yaw":0.2298256824215265,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22938206958078666,"id":"1916_0","lane_type":4,"pos":{"x":566915.7712003491,"y":4317781.180747019,"yaw":0.22938206958078666,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2286921209051039,"id":"1916_0","lane_type":4,"pos":{"x":566916.2984598223,"y":4317781.303699773,"yaw":0.2286921209051039,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.22808936922424297,"id":"1443_0","lane_type":61,"pos":{"x":566916.8090088924,"y":4317781.422299073,"yaw":0.22808936922424297,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280897918028493,"id":"1443_0","lane_type":61,"pos":{"x":566917.2969322235,"y":4317781.535560183,"yaw":0.2280897918028493,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.228089741859539,"id":"1443_0","lane_type":61,"pos":{"x":566917.7850105008,"y":4317781.648857261,"yaw":0.228089741859539,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280892917326761,"id":"1443_0","lane_type":61,"pos":{"x":566918.2731774633,"y":4317781.762174925,"yaw":0.2280892917326761,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808955210534196,"id":"1443_0","lane_type":61,"pos":{"x":566918.7612317912,"y":4317781.875466444,"yaw":0.22808955210534196,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808965156076313,"id":"1443_0","lane_type":61,"pos":{"x":566919.2493102492,"y":4317781.988763562,"yaw":0.22808965156076313,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808928593946132,"id":"1443_0","lane_type":61,"pos":{"x":566919.7374188603,"y":4317782.102067681,"yaw":0.22808928593946132,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280892545511175,"id":"1443_0","lane_type":61,"pos":{"x":566920.2254449375,"y":4317782.215352641,"yaw":0.2280892545511175,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808944326367542,"id":"1443_0","lane_type":61,"pos":{"x":566920.7136167267,"y":4317782.328671426,"yaw":0.22808944326367542,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808894375747077,"id":"1443_0","lane_type":61,"pos":{"x":566921.2016420381,"y":4317782.441956209,"yaw":0.22808894375747077,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280897820761068,"id":"1443_0","lane_type":61,"pos":{"x":566921.6897221782,"y":4317782.555253718,"yaw":0.2280897820761068,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808930483652312,"id":"1443_0","lane_type":61,"pos":{"x":566922.1778322635,"y":4317782.668558179,"yaw":0.22808930483652312,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280892447288475,"id":"1443_0","lane_type":61,"pos":{"x":566922.6658866119,"y":4317782.781849703,"yaw":0.2280892447288475,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808935539016098,"id":"1443_0","lane_type":61,"pos":{"x":566923.1539497036,"y":4317782.895143256,"yaw":0.22808935539016098,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808927427023848,"id":"1443_0","lane_type":61,"pos":{"x":566923.642073648,"y":4317783.008450933,"yaw":0.22808927427023848,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808950488732818,"id":"1443_0","lane_type":61,"pos":{"x":566924.1301164496,"y":4317783.121739777,"yaw":0.22808950488732818,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808932864695802,"id":"1443_0","lane_type":61,"pos":{"x":566924.6182156634,"y":4317783.235041713,"yaw":0.22808932864695802,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808924807121161,"id":"1443_0","lane_type":61,"pos":{"x":566925.1062909176,"y":4317783.348338088,"yaw":0.22808924807121161,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280891397247924,"id":"1443_0","lane_type":61,"pos":{"x":566925.5943663705,"y":4317783.461634511,"yaw":0.2280891397247924,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808924370410544,"id":"1443_0","lane_type":61,"pos":{"x":566926.0824557398,"y":4317783.574934163,"yaw":0.22808924370410544,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808963560749207,"id":"1443_0","lane_type":61,"pos":{"x":566926.570535443,"y":4317783.6882315725,"yaw":0.22808963560749207,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808954152020086,"id":"1443_0","lane_type":61,"pos":{"x":566927.0586162254,"y":4317783.801529231,"yaw":0.22808954152020086,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280894686547862,"id":"1443_0","lane_type":61,"pos":{"x":566927.5466974347,"y":4317783.914826989,"yaw":0.2280894686547862,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808944286113644,"id":"1443_0","lane_type":61,"pos":{"x":566928.0347693623,"y":4317784.028122593,"yaw":0.22808944286113644,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280893771564143,"id":"1443_0","lane_type":61,"pos":{"x":566928.5228644359,"y":4317784.141423568,"yaw":0.2280893771564143,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808951935129954,"id":"1443_0","lane_type":61,"pos":{"x":566929.0109445751,"y":4317784.254721079,"yaw":0.22808951935129954,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808916810798158,"id":"1443_0","lane_type":61,"pos":{"x":566929.4990092661,"y":4317784.368015002,"yaw":0.22808916810798158,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808926710715005,"id":"1443_0","lane_type":61,"pos":{"x":566929.9871164225,"y":4317784.481318784,"yaw":0.22808926710715005,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808942491792936,"id":"1443_0","lane_type":61,"pos":{"x":566930.4751578907,"y":4317784.594607317,"yaw":0.22808942491792936,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808997446560786,"id":"1443_0","lane_type":61,"pos":{"x":566930.963280281,"y":4317784.707914635,"yaw":0.22808997446560786,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808926158163145,"id":"1443_0","lane_type":61,"pos":{"x":566931.4513584088,"y":4317784.821211677,"yaw":0.22808926158163145,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808912737001125,"id":"1443_0","lane_type":61,"pos":{"x":566931.9394052767,"y":4317784.934501464,"yaw":0.22808912737001125,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808942034593915,"id":"1443_0","lane_type":61,"pos":{"x":566932.4274650743,"y":4317785.047794251,"yaw":0.22808942034593915,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.2280893768731642,"id":"1443_0","lane_type":61,"pos":{"x":566932.9155725923,"y":4317785.161098117,"yaw":0.2280893768731642,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.22808922623817818,"id":"1443_0","lane_type":61,"pos":{"x":566933.4037046838,"y":4317785.274407686,"yaw":0.22808922623817818,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":1},{"driving_direction":1,"heading":0.26752967257025023,"id":"1644_0","lane_type":4,"pos":{"x":566933.8916847552,"y":4317785.387681967,"yaw":0.26752967257025023,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.27296352818673797,"id":"1644_0","lane_type":4,"pos":{"x":566934.4081791614,"y":4317785.529273117,"yaw":0.27296352818673797,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.2890096417822709,"id":"1644_0","lane_type":4,"pos":{"x":566934.9215254015,"y":4317785.676039357,"yaw":0.2890096417822709,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.3074639284798972,"id":"1644_0","lane_type":4,"pos":{"x":566935.4352098298,"y":4317785.834705625,"yaw":0.3074639284798972,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.33823654065401276,"id":"1644_0","lane_type":4,"pos":{"x":566935.9451221547,"y":4317786.001126098,"yaw":0.33823654065401276,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.395968696639526,"id":"1644_0","lane_type":4,"pos":{"x":566936.4469496277,"y":4317786.191396152,"yaw":0.395968696639526,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.45951130596930084,"id":"1644_0","lane_type":4,"pos":{"x":566936.932646194,"y":4317786.415261541,"yaw":0.45951130596930084,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.5146112594780772,"id":"1644_0","lane_type":4,"pos":{"x":566937.4071709261,"y":4317786.667336488,"yaw":0.5146112594780772,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.5708181015020354,"id":"1644_0","lane_type":4,"pos":{"x":566937.8645413354,"y":4317786.943274177,"yaw":0.5708181015020354,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.6289000398374989,"id":"1644_0","lane_type":4,"pos":{"x":566938.3066152309,"y":4317787.2463440485,"yaw":0.6289000398374989,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.6892214536716222,"id":"1644_0","lane_type":4,"pos":{"x":566938.7309829269,"y":4317787.575155735,"yaw":0.6892214536716222,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.7486844767678505,"id":"1644_0","lane_type":4,"pos":{"x":566939.1309617738,"y":4317787.92777718,"yaw":0.7486844767678505,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.8034100665870626,"id":"1644_0","lane_type":4,"pos":{"x":566939.5127770142,"y":4317788.303097906,"yaw":0.8034100665870626,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.8630500827140412,"id":"1644_0","lane_type":4,"pos":{"x":566939.8731208481,"y":4317788.699246494,"yaw":0.8630500827140412,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.9230756615651824,"id":"1644_0","lane_type":4,"pos":{"x":566940.2060751247,"y":4317789.11627494,"yaw":0.9230756615651824,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":0.9864822640727969,"id":"1644_0","lane_type":4,"pos":{"x":566940.5167654373,"y":4317789.551845539,"yaw":0.9864822640727969,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.0565260517858244,"id":"1644_0","lane_type":4,"pos":{"x":566940.793038494,"y":4317790.008133316,"yaw":1.0565260517858244,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.1151141368821618,"id":"1644_0","lane_type":4,"pos":{"x":566941.040549578,"y":4317790.481393935,"yaw":1.1151141368821618,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.1722531102654243,"id":"1644_0","lane_type":4,"pos":{"x":566941.2619465468,"y":4317790.967292507,"yaw":1.1722531102654243,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.230583496505281,"id":"1644_0","lane_type":4,"pos":{"x":566941.453179325,"y":4317791.464896472,"yaw":1.230583496505281,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.286402500769971,"id":"1644_0","lane_type":4,"pos":{"x":566941.6168596789,"y":4317791.972688081,"yaw":1.286402500769971,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.3464680865459688,"id":"1644_0","lane_type":4,"pos":{"x":566941.7513457895,"y":4317792.488118835,"yaw":1.3464680865459688,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.4076000543605254,"id":"1644_0","lane_type":4,"pos":{"x":566941.8528590363,"y":4317793.010806499,"yaw":1.4076000543605254,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2},{"driving_direction":1,"heading":1.4602309295463745,"id":"1644_0","lane_type":4,"pos":{"x":566941.9238674229,"y":4317793.538403846,"yaw":1.4602309295463745,"z":0},"speeds":{"vmax":15,"vmax_dev":0},"time_window":None,"type":2}])
#         print(li)
#         draw_lanes()
#         graph_generate(li, 'r.', 'k.', 'm.', 'b.', 'lightcoral', "y.", int(0))
#         plt.axis('equal')
#
#         plt.legend(loc="upper right")
#         plt.grid()
#         plt.title("show")
#         plt.show()

#     # with open("/var/log/trunk/vcs/vcs.yangxiang.yangxiang.log.INFO.20221115-172839.1090") as f:
#     with open("/var/log/trunk/vcs/vcs.yangxiang.yangxiang.log.INFO.20221202-095043.18496") as f:
#         data = f.readlines()
#     for line in data:
#         if "header" in line:
#             li = []
#             l = line.split("] ")[1].split("\n")[0]
#             json_d = json.loads(l)
#             point_info = json_d["body"]
#             pz = {
#                 "pos": point_info["stop"],
#                 "type": "STOP",
#                 "heading": 4.9
#             }
#             che1 = {
#                 "pos": point_info["agent_second_id"],
#                 "type": "ART1",
#                 "heading": 4.9
#             }
#             che2 = {
#                 "pos": point_info["agent_first_id"],
#                 "type": "ART2",
#                 "heading": 4.9
#             }
#             li.extend([pz, che1, che2])
#             draw_lanes()
#             graph_generate(li, 'r.', 'k.', 'm.', 'b.', 'lightcoral', "y.", int(0))
#             plt.axis('equal')
#
#             plt.legend(loc="upper right")
#             plt.grid()
#             plt.title(point_info["agent_second_id"]["truck_id"])
#             plt.show()


# if __name__ == "__main__":
#     with open('json_files/11-14_A525.json', 'r') as f:
#         navi_paths = json.load(f)
#     for i in navi_paths:
#         print(i)
#         print(type(i))
#         fms_navi_json, calib_navi_json = i[0], i[1]
#         print(fms_navi_json, calib_navi_json)
#
#         with open(calib_navi_json) as f:
#             data2 = json.load(f)
#         draw_lanes()
#         graph_generate(data2 if type(data2) is list else data2["pathGuidance"]["points"], 'r.', 'k.', 'm.', 'b.', 'green',
#                        "y.", 0)
#
#         with open(fms_navi_json) as f:
#             data1 = json.load(f)
#         graph_generate(data1 if type(data1) is list else data1['body']["pathGuidance"]["points"], 'r.', 'k.', 'm.', 'b.', 'green',
#                        "y.", 1)
#
#         plt.axis('equal')
#         plt.legend(loc="upper right")
#         plt.grid()
#         plt.title('navis')
#         plt.show()
