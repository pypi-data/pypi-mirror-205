import os

def ftree(path, prefix=''):
    """
    输出目录树
    """
    items = os.listdir(path)
    # 对目录和文件按名称进行排序
    items.sort()
    # 遍历目录和文件
    for item in items:
        # 获取子项的完整路径
        new_path = os.path.join(path, item)
        # 判断是否是目录
        if os.path.isdir(new_path):
            # 输出目录名称，并递归地调用 ftree 函数输出其子目录和文件
            print(prefix + '+-- ' + item)
            ftree(new_path, prefix + '    ')
        else:
            # 输出文件名称
            print(prefix + '|-- ' + item)
