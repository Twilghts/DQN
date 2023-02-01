
_size = 500
data_by_one_time = 1024 * 1024 * _size / 2

def create_file(file_path, size):
    """
    # 快速生成大文件
    :param file_path: 文件路径
    :param size: 文件大小，本函数以GB为单位，也可以根据需求设置为KB或MB等
    :return:
    """
    # 首先以路径path新建一个文件，并设置模式为写
    lfile = open(file_path, 'w')
    # 根据文件大小，偏移文件写入位置；位置要减掉一个字节，因为后面要写入一个字节的数据
    lfile.seek(1024 * 1024 * size - 1)
    # 然后在当前位置写入任何内容，必须要写入，不然文件不会那么大哦
    lfile.write('\x00')  # lfile.write('')不会写入任何内容
    lfile.close()


if __name__ == '__main__':
    create_file("Test_1.txt", _size)
