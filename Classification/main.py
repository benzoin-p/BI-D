import dbscan as ds
import file_reader as fr
import draw

data_num = 500

if __name__ == "__main__":
    data_set = fr.get_data_set(data_num + 1)
    for i in range(1, data_num + 1):
        origin_data = fr.get_origin_data(data_set[i])
        data, attr_dist, noise_index_list = fr.get_data(data_set[i])
        noise, noise_index_list = ds.get_noise(data, 0.12, 4, noise_index_list)
        draw.draw_xy_picture(origin_data, noise_index_list, attr_dist)
