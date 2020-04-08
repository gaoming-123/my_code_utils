# -*- coding: UTF-8 -*-
# Date   : 2020/3/27 15:05
# Editor : gmj
# Desc   : 
import os
import re
import time
import requests
import cairosvg
import shutil
from PIL import Image
from aip import AipOcr
import zipfile
import hashlib
import json

# 百度通用文字识别接口配置参数
APP_ID = '***'
API_KEY = '***'
SECRET_KEY = '***'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 下载字体文件
def down_woff(woff_url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    res = requests.get(woff_url, headers=header)
    # print(res.text)
    file_name = woff_url.split('/')[-1]
    with open(file_name, 'wb') as fw:
        fw.write(res.content)
    return file_name


# 从字客网将woff文件转换为svg文件
def get_svg(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as fr:
        content = fr.read()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    }
    m.update(content)
    md5_text = m.hexdigest()
    # 字客网
    url = f'https://www.fontke.com/?g=Font&m=Tool&a=exists&toolId=convfont&md5={md5_text}'
    res = requests.get(url)
    res = json.loads(res.text)
    if res['exists'] == 'yes':
        url2 = 'https://www.fontke.com/tool/convfont/'
        # 并没有上传文件 而是文件的md5值，因此如果返回不存在，人工上传一次即可
        data = {
            'name': file_path.split('/')[-1].split('.')[0],
            'filemd5': md5_text,
            'oldFormat': 'woff',
            'newformats': 'svg',
        }
        res2 = requests.post(url2, data=data, headers=header)
        res2 = json.loads(res2.text)
        down_url = 'https://www.fontke.com' + res2['downloadUrl']
        zip_res = requests.get(down_url, headers=header)
        with open('tmp.zip', 'wb') as fw:
            fw.write(zip_res.content)
        z = zipfile.ZipFile('./tmp.zip', 'r')
        for f in z.namelist():
            if 'svg' in f:
                return z.read(f).decode('utf-8')
    else:
        print(res['exists'])


# 根据svg画png图
def draw_png(data, png_path):
    try:
        cc = "\\u" + data[0][3:7]
        print_key = cc.encode('utf-8').decode('unicode_escape')
        key = cc.encode('utf-8').decode('unicode_escape')
    except:
        print_key = data[0]
        # key = f'{data[0]}'
    # 构造svg文件内容
    org_text = f"""<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg id="_" width="128" height="128" style="width:192px;height:256px;" version="1.1" xmlns="http://www.w3.org/2000/svg" viewBox="1 1 1024 1024" enable-background="new 1 1 1024 1024" xml:space="preserve"><path fill="#black" d="{data[1]}"/></svg>"""
    # svg转换为png图片
    exportPath = os.path.join(png_path, f'{data[0]}.png')
    with open(exportPath, 'w') as fw:
        cairosvg.svg2png(bytestring=org_text, write_to=exportPath)
    return exportPath, data[0][3:7], print_key


# 处理原始png图片
def deal_pic(exportPath):
    im = Image.open(exportPath)
    # 对图片镜像上下镜像处理
    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    x, y = im.size
    try:
        # 对图片进行添加白色背景
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(exportPath)
    except:
        print(f'{exportPath}图片处理失败')


# 从api接口获取解析结果
def get_word(file_path, accurate=True):
    # 读取图片
    with open(file_path, 'rb') as fp:
        image = fp.read()

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    options["probability"] = "true"
    if accurate:
        # 通用文字识别（高精度版）
        res = client.basicAccurate(image, options)
    else:
        # 通用文字识别
        res = client.basicGeneral(image, options)
    try:
        word_res = res['words_result'][0]['words']
        print_res = word_res
    except:
        print_res = res
        word_res = None
    return print_res, word_res


# 获得解析结果字典
def get_words_dict(pattern, png_path, svg_content, accurate=True):
    """
    :param png_path: 保存png图片的文件路径
    :param svg_content: svg内容
    :return: 返回解析字典 但还需要人工检查
    """
    if os.path.exists(png_path):
        # 删除文件夹
        shutil.rmtree(png_path, ignore_errors=True)
        os.mkdir(png_path)
    else:
        os.mkdir(png_path)
    svg_list = re.findall(pattern, svg_content, re.S)
    print('共有字数：', len(svg_list), '个')
    t_ = {}
    for i in svg_list:
        t_[i[0]] = ''
    print(t_)
    # 解析结果字典 key值为 被替换的字， value为替换字
    result = {}
    result_list = []
    num = 0
    for i in svg_list:
        if i[1] == 'M0 0v0v0v0z':
            continue
        try:
            exportPath, key, print_key = draw_png(i, png_path)
            deal_pic(exportPath)
            print_res, word_res = get_word(exportPath, accurate)
            result[key] = word_res
            result_list.append(''.join([print_key, '*:* ', print_res]))
            # print(print_key, '*:* ', print_res)
            exportPath2 = os.path.join(png_path, f'{i[0]}--{key}.png')
            # 重命名 方便检查
            os.rename(exportPath, exportPath2)
            time.sleep(3)
            num += 1
        except Exception as e:
            result[key] = ''
            print(i)
            try:
                print(print_res)
            except:
                pass
    print('解析完成：', num, '个')
    return result, result_list


def main(woff_url):
    # 字体链接
    # woff_url = 'https://staticv3.youzy.cn/ToC.PC/fonts/cn_5.woff'
    file_name = down_woff(woff_url)
    print('woff文件下载成功')
    svg_content = get_svg(file_name)
    if svg_content: print('svg转换成功')
    png_path = './tupian'
    # 提取svg数据的正则
    pattern = r'''<glyph .*? unicode="(.*?)" .*?d="?(.*?)"? />'''
    # result={'被替换字':'替换字'}
    result, result_list = get_words_dict(pattern, png_path, svg_content)
    # 解析结果字典 key值为 被替换的字， value为替换字
    print(result)
    with open('result.txt', 'w', encoding='utf-8') as fw:
        fw.write('\n'.join(result_list))


if __name__ == '__main__':
    woff_url = 'https://staticv3.youzy.cn/ToC.PC/fonts/cn_5.woff'
    main(woff_url)
