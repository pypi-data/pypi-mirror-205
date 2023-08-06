#! /usr/bin/python
# -*- coding: utf-8 -*-
# @author izhangxm
# @date 2021/12/29
# @fileName decode_simplepro_file.py
# Copyright 2017 izhangxm@gmail.com. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import base64
import glob
import lzma
import os
import re
import struct

import rsa


def main(app_full_path=None):
    if app_full_path is None:
        try:
            from simplepro import conf

            app_full_path = os.path.dirname(conf.__file__)
        except ImportError:
            raise Exception("请安装simplepro或指定包位置")
    py_file_list = glob.glob(os.path.join(app_full_path, "**/*.py"), recursive=True)
    re_p = r"b64decode\(b'([\s\S]*?)\)\)\)$"
    for py_file in py_file_list:
        with open(py_file, "r") as f:
            content = f.read()
        res = re.search(re_p, content)
        if not res:
            continue
        print(f"decoding {py_file}")
        mm_code = res.group(1)
        code = lzma.decompress(base64.b64decode(mm_code.encode())).decode(
            encoding="utf8"
        )
        with open(py_file, "w+") as f:
            f.write(code)
    print("all py file decoded")

    so_file_path = glob.glob(os.path.join(app_full_path, "**/.core.so"), recursive=True)
    if len(so_file_path) == 0:
        print("not found core.so")
        return ""
    so_file_path = so_file_path[0]
    so_file = open(so_file_path, "rb")
    buffer = so_file.read(2)
    (r,) = struct.unpack("h", buffer)
    buffer = so_file.read(r)
    pri = buffer
    strs = bytearray()
    while True:
        temp = so_file.read(4)
        if len(temp) == 0:
            so_file.close()
            break
        (size,) = struct.unpack("i", temp)
        d = so_file.read(size)
        privkey = rsa.PrivateKey.load_pkcs1(pri)
        strs.extend(rsa.decrypt(d, privkey))
    code = strs.decode(encoding="utf8")
    so_file_dir = os.path.dirname(so_file_path)

    so_py_file = os.path.join(so_file_dir, "core.py")

    with open(so_py_file, "w+") as f:
        f.write(code)

    print("so file decoded, please modify handler file: from .core import *")


if __name__ == "__main__":
    # main("/Users/izhangxm/Downloads/aaa/simplepro-5.0")
    main()
