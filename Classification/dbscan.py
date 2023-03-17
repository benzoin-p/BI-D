import math

import random


# 计算欧式距离
def get_euclidean_distance_3(data1, data2):
    distance = 0.0
    for i in range(3):
        distance += pow((data1[i] - data2[i]), 2)
    return math.sqrt(distance)


# 返回值为noise列表
def dbscan(data, r, min_count, noise_index_list):
    # 对临时变量进行初始化：
    # 核心对象集合core_set={},
    # 聚类簇数 k=0,
    # 未访问样本集合wait_set=D
    # 簇划分C={}
    # 为避免算法过于复杂，进行了部分变量的优化与省略
    core_set = []
    c = []

    # 对于xi∈D，按以下步骤找出核心对象：
    # 通过距离度量方式，找到样本xi的r-邻域子样本集N
    # 如果|N|>=min_count，则使core_set=core_set∪{xi}
    for i in range(len(data)):
        count = 0
        for j in range(len(data)):
            distance = get_euclidean_distance_3(data[i], data[j])
            if distance < r:
                count = count + 1
        if count >= min_count:
            core_set.append(data[i])

    # print("找到的核心对象为：")
    # print(core_set)

    # 如果core_set={},则算法结束

    # 从core_set={o1,o2,...,on}(n<=m)中随机选择一个对象oi，
    # 定义簇核心对象队列cluster_core_queue={oi}
    # （用于找到所有密度可达的对象），
    # 更新未访问样本集合wait_set=wait_set-{oi}，
    # 初始化类别序号k=k+1，
    # 初始化当前簇样本集合Ck={oi}

    # 更新核心对象集合core_set=core_set-Ck
    # 如果cluster_core_queue={}，则当前聚类簇Ck生成完毕，
    # 更新簇划分C=C∪{Ck}，
    # 转入步骤③，
    # 否则继续进行步骤⑥
    # 此处对簇的大小进行初始化，即实现簇核心队列的实质效果

    # 取出当前簇核心对象队列中的队首oj，获取oj的r-邻域子样本集N，
    # 令密度可达集合N’=N∩wait_set，
    # 更新当前簇样本集合Ck=Ck∪N’，
    # 更新未访问样本集合wait_set=wait_set-N’，
    # 更新簇核心对象队列为cluster_core_queue=(cluster_core_queue-oj)∪(N’∩core_set)，
    # 转入步骤⑤

    for i in range(len(core_set)):
        c.append([])
    # 此处对c的大小进行规定，实质上是实现了簇对象队列
    # 由于本题并不需要提取簇中心，只需要找出噪音，故不需要像算法一样使用密度可达集合
    # 直接通过获取每一个核心对象的直接密度可达集合，就能找出剩下的噪音

    for i in range(len(core_set)):
        for j in range(len(data)):
            if (data[j] != 0) and (get_euclidean_distance_3(core_set[i], data[j]) < r):
                c[i].append(data[j])
                # 通过将data赋0，实现wait_set的作用，即排除已经进入簇集中的对象
                data[j] = 0

    # 赋0的data值即为非噪声，其余为噪声，此处对data进行除0操作获得噪声，同时获取噪声的索引
    count = 0
    for i in range(len(data)):
        if data[i] == 0:
            count += 1
        else:
            noise_index_list.append(i)

    for i in range(count):
        data.remove(0)

    return data, noise_index_list


def get_noise(data, r, min_count, noise_index_list):
    noise, noise_index_list = dbscan(data, r, min_count, noise_index_list)
    if len(noise) == 0:
        print("无噪声")
        noise_index_list.append(-1)
    else:
        print(noise_index_list)
    return noise, noise_index_list

# if __name__ == "__main__":
#     # 生成随机数据
#     data_set = []
#     for i in range(100):
#         data_set.append([])
#         for j in range(3):
#             data_set[i].append(random.uniform(-50, 50))
#
#     print(data_set)
#
#     c = dbscan(data_set, 25, 5)
#     print(c)
