"""SVG图像处理"""
import os
import re


def InitSvg(color: str):
    """增加颜色填充，初始值为#2c2c2c，仅需运行一次"""
    pattern = r'/>'
    tt = re.compile(pattern)
    svgpath = ['icon/svgs/brands', 'icon/svgs/regular', 'icon/svgs/solid']
    for path in svgpath:
        file = os.listdir(path)
        for i in file:
            f = open(path + '/' + i, 'r')
            temp = f.read()
            f.close()
            f = open(path + '/' + i, 'w')
            f.write(re.sub(tt, ' fill="' + color + '"/>', temp))
            f.close()


def colorchange(path: str, color: str):
    """生成所需颜色图标"""
    pattern = re.compile(r'#\w+')
    f = open(path, 'r')
    temp = f.read()
    f.close()
    f = open(path, 'w')
    f.write(re.sub(pattern, color, temp))
    f.close()
    return path
