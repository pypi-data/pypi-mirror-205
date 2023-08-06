#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# coding: utf-8

import os
import sys
from typing import *

import tinify

SUPPORTED = ".jpg", ".jpeg", ".png", ".webp"
OPTED_PREFIX = "optimized"
tinify.key = "NvcmRhdbZ9DbS3h9W4w8H9wM84pZd4M0"


def clean_filenames(files: List[str]) -> List[str]:
    valid_files = []
    for f in files:
        if f and os.path.isfile(f):
            if os.path.splitext(f)[1].lower() in SUPPORTED:
                valid_files.append(f)
    return valid_files


def receive_filenames() -> List[str]:
    if len(sys.argv) > 1:
        image_files = clean_filenames(sys.argv[1:])
        if not image_files:
            input("没有拖入任何有效的图片文件，按回车关闭后请重试...")
            sys.exit(1)
        return image_files
    while True:
        names = input("请输入要压缩的图片名称(回车压缩当前文件夹)：")
        if names:
            image_files = clean_filenames(names.split())
        else:
            try:
                image_files = clean_filenames(os.listdir(os.curdir))
            except PermissionError:
                print("无法列举当前文件夹下的文件，请用其他方式指定...")
                continue
        if not image_files:
            print("没有找到符合要求的图片，请重新指定...")
            continue
        return image_files


def compression_config() -> Tuple[int, int]:
    width, height = 0, 0
    while True:
        input_str = input("请输入尺寸(宽度 高度)：")
        if not input_str:
            break
        config = input_str.split(" ", 1)
        if len(config) != 2:
            print("请以空格分隔宽度和高度数值...")
            continue
        try:
            width = int(config[0])
            height = int(config[1])
        except ValueError:
            print("请输入正确的宽度和高度数值...")
            continue
        if width >= 0 and height >= 0 and not (width == 0 and height == 0):
            break
        else:
            print("宽高数值必须大于等于零且不能同时等于零...")
    return width, height


def show_progress(func: Callable[[str], None]):
    def inner_func(files: List[str], width: int, height: int):
        length = len(files)
        for i, p in enumerate(files, 1):
            base = os.path.basename(p)
            print("(%d/%d)图片<%s>正在压缩处理中，请稍后..." % (i, length, base))
            func(os.path.abspath(p), width, height)
        print("全部处理完成 ~")

    return inner_func


@show_progress
def start_compression(filepath: str, width: int, height: int):
    count = 0
    parent, base = os.path.split(filepath)
    while True:
        new_name = "%s%d_%s" % (OPTED_PREFIX, count, base)
        new_fullpath = os.path.join(parent, new_name)
        if not os.path.exists(new_fullpath):
            break
        count += 1
    try:
        source = tinify.from_file(filepath)
        if width > 0 and height == 0:
            source = source.resize(method="scale", width=width)
        elif width == 0 and height > 0:
            source = source.resize(method="scale", height=height)
        elif width > 0 and height > 0:
            source = source.resize(method="fit", width=width, height=height)
        source.to_file(new_fullpath)
    except tinify.AccountError:
        print("帐户异常~")
    except tinify.ClientError:
        print("客户端异常~")
    except tinify.ServerError:
        print("服务器异常~")
    except tinify.ConnectionError:
        print("网络连接异常~")
    except Exception as e:
        print("未知异常：%s" % e)


def main():
    filenames = receive_filenames()
    config = compression_config()
    start_compression(filenames, *config)


if __name__ == "__main__":
    main()
    input("按回车退出...")

