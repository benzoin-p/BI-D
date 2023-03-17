import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import file_reader as fr


def draw_xy_picture(data, noise_index_list, attr_dist):
    # 设置中文字体
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = 'SimHei'

    # 画布
    fig = plt.figure(figsize=(6, 4), dpi=120, facecolor='white', frameon=True)
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    x = []
    y = []
    noise_x = []
    noise_y = []
    river_x = []
    river_y = []
    river = fr.river_point

    for i in range(len(data)):
        if i not in noise_index_list:
            x.append(data["now_x"][i])
            y.append(data["now_y"][i])
        else:
            noise_x.append(data["now_x"][i])
            noise_y.append(data["now_y"][i])

    for i in range(len(river)):
        river_x.append(river[i][0])
        river_y.append(river[i][1])

    area = np.pi * 3 ** 2
    area2 = np.pi * 30 ** 2
    plt.scatter(x, y, c="#003371", marker="p", label="航行轨迹", alpha=0.3, s=area)
    if len(noise_x) != 0 and len(noise_y) != 0:
        plt.scatter(noise_x, noise_y, c="#F2B345", marker="x", label="噪声", alpha=0.3, s=area)
    plt.scatter(river_x, river_y, c="#70F3FF", marker="o", alpha=0.2, s=area2)

    # 中文标题
    MMSI = data["MMSI"][0]
    time = data["time1"][0]
    # print("船舶[%s]在\n%s\n的航行轨迹图" % (MMSI, time))
    plt.title("船舶[%s]在 %s 的航行轨迹图" % (MMSI, time))

    # 字体字典
    font_dict = dict(fontsize=12,
                     color='k',
                     family='SimHei',
                     weight='light',
                     style='italic',
                     )

    # X轴标签
    plt.xlabel("船舶经度(单位：度)", loc='center', fontdict=font_dict)

    # Y轴标签
    plt.ylabel("船舶纬度(单位：度)", loc='center', fontdict=font_dict)

    # X轴范围
    x1 = attr_dist[1]
    x2 = attr_dist[0]
    # plt.xlim(114.196008, 114.847623)
    plt.xlim(x1, x2)
    plt.xticks(np.arange(x1, x2, (x2 - x1) * 0.2))

    # Y轴范围
    y1 = attr_dist[2]
    y2 = attr_dist[3]
    plt.ylim(y2, y1)
    # plt.ylim(30.440335, 30.70202)
    plt.yticks(np.arange(y1, y2, (y2 - y1) * 0.2))

    # 图例
    plt.legend()

    # 网格线
    plt.grid(axis='both')

    plt.show()
