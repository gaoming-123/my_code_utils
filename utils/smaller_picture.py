# -*- coding: UTF-8 -*-
# Date   : 2020/1/17 17:10
# Editor : gmj
# Desc   : 压缩图片 文件

from PIL import Image
import os


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile


def compress_image(infile, outfile='', mb=200, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)


def resize_image(infile, outfile='', x_s=None):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度  1376
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    if x_s:
        y_s = int(y * x_s / x)
    else:
        x_s, y_s = x, y
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    outfile = get_outfile(infile, outfile)
    out.save(outfile)


if __name__ == '__main__':
    base_path = r'C:\Users\pop\Desktop\yssuo'
    out_path = r'C:\Users\pop\Desktop\outpic'
    files = os.listdir(base_path)
    # print(files)
    for file_name in files:
        try:
            org_file = os.path.join(base_path, file_name)
            out_file = os.path.join(out_path, file_name)
            # file_size = get_size(org_file)
            print(out_file)
            compress_image(infile=org_file, outfile=out_file)
            resize_image(infile=org_file, outfile=out_file)
        except Exception as e:
            print(e)
