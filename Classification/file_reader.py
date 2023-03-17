import sys
import math
import pandas as pd
import numpy as np

path = "..\\data\\20161017 "
names = ["time1", "time2", "MMSI", "now_x", "now_y", "pre_x", "pre_y", "speed", "direction", "code"]
# 长江水域的采样点
river_point = [[114.208369, 30.450547], [114.232803, 30.476446], [114.25235, 30.493376],
               [114.275595, 30.519182], [114.288569, 30.538924], [114.306679, 30.572759],
               [114.320477, 30.598128], [114.340887, 30.622496], [114.360146, 30.642383],
               [114.380556, 30.655556], [114.407577, 30.664503], [114.438622, 30.671709],
               [114.461907, 30.6814], [114.482891, 30.685127], [114.403265, 30.682642],
               [114.438622, 30.698046], [114.481454, 30.699039], [114.512499, 30.686618],
               [114.533196, 30.680158], [114.551306, 30.666243], [114.561079, 30.650834],
               [114.571428, 30.632689], [114.580052, 30.611556], [114.586663, 30.598874],
               [114.596149, 30.582709], [114.610235, 30.570769], [114.628632, 30.564799],
               [114.648467, 30.568779], [114.632817, 30.56485], [114.6607, 30.574552],
               [114.67996, 30.579029], [114.69692, 30.583009], [114.713305, 30.585993],
               [114.729403, 30.594698], [114.744351, 30.603899], [114.417224, 30.666294],
               [114.446832, 30.676233], [114.292183, 30.55133], [114.261928, 30.509274],
               [114.279463, 30.525327], [114.759373, 30.613138], [114.77892, 30.621094],
               [114.795593, 30.622089], [114.814565, 30.622089], [114.826063, 30.611149],
               [114.839287, 30.595731], [114.844461, 30.571854], [114.218953, 30.461844],
               [114.298578, 30.563894], [114.314676, 30.585037], [114.331349, 30.609657],
               [114.350896, 30.634767], [114.566777, 30.640982], [114.847623, 30.575586],
               [114.603137, 30.572468]]


def d2s(date):
    h, m, s = date.strip().split(":")
    return 3600 * int(h) + 60 * int(m) + int(s)


# 计算平面距离
def get_euclidean_distance_2(data1, data2):
    distance = 0.0
    for i in range(2):
        distance += pow((data1[i] - data2[i]), 2)
    return math.sqrt(distance)


def normalization(num, max, min):
    return (num - min) / (max - min)


def data_frame_to_list(data):
    list = []
    time_list = []
    x_list = []
    y_list = []

    for i in range(len(data)):
        list_element = []

        time = d2s(data["time2"][i])
        x = data["now_x"][i]
        y = data["now_y"][i]

        list_element.append(time)
        list_element.append(x)
        list_element.append(y)

        time_list.append(time)
        x_list.append(x)
        y_list.append(y)

        # print(list_element)
        list.append(list_element)

    return list, time_list, x_list, y_list


def is_in_river(data):
    for i in range(len(river_point)):
        distance = get_euclidean_distance_2(river_point[i], data)
        if distance <= 0.018:
            return True
    return False


# 对数据进行预处理,排除明显不在长江上的点
def data_operation(list, time_list, x_list, y_list):
    max_time = max(time_list)
    min_time = min(time_list)
    max_x = max(x_list)
    min_x = min(x_list)
    max_y = max(y_list)
    min_y = min(y_list)
    new_list = []
    attr_dist = []
    noise_index_list = []

    for i in range(len(list)):
        list_element = []
        origin_x = list[i][1]
        origin_y = list[i][2]
        origin_data = [origin_x, origin_y]

        # 排除远离长江的点
        if is_in_river(origin_data) is not True:
            noise_index_list.append(i)

        # 数据归一化处理
        time = normalization(list[i][0], max_time, min_time)
        x = normalization(list[i][1], max_x, min_x)
        y = normalization(list[i][2], max_y, min_y)

        list_element.append(time)
        list_element.append(x)
        list_element.append(y)

        # 用于绘图边缘参数
        attr_dist = [max_x + (max_x - min_x) * 0.1, min_x - (max_x - min_x) * 0.1,
                     max_y + (max_y - min_y) * 0.1, min_y - (max_y - min_y) * 0.1]

        new_list.append(list_element)

    return new_list, attr_dist, noise_index_list


def get_data(data):
    list, time_list, x_list, y_list = data_frame_to_list(data)
    # print(list)
    new_list, attr_dist, noise_index_list = data_operation(list, time_list, x_list, y_list)
    return new_list, attr_dist, noise_index_list
    # print(new_list)
    # print(list)
    # print(type(data))


def get_origin_data(data):
    return data


def get_data_set(data_num):
    data_set = []
    for i in range(1, data_num + 1):
        integrated_path = "%s(%d).txt" % (path, i)
        data = pd.read_csv(integrated_path, encoding="utf-8", delim_whitespace=True, header=None, names=names,
                           usecols=["time1", "time2", "MMSI", "now_x", "now_y"])
        data_set.append(data)
    return data_set

# if __name__ == "__main__":
#     data = pd.read_csv(path, encoding="utf-8", delim_whitespace=True, header=None, names=names,
#                        usecols=["time2", "now_x", "now_y"])
#     list, time_list, x_list, y_list = data_frame_to_list(data)
#     print(list)
#     new_list = data_operation(list, time_list, x_list, y_list)
#     print(new_list)
#     # print(list)
#     print(type(data))
