#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
env_info.py
打印当前 Python 环境的路径和配置信息
"""

import sys
import os
import site
import sysconfig

def main():
    print("=" * 60)
    print("🐍 Python 环境信息")
    print("=" * 60)

    # 解释器路径
    print(f"\n[Python 可执行文件路径]\n{sys.executable}")

    # Python 版本
    print(f"\n[Python 版本]\n{sys.version}")

    # sys.path
    print("\n[sys.path 模块搜索路径]")
    for p in sys.path:
        print(" ", p)

    # site-packages 路径
    print("\n[site-packages 目录]")
    try:
        print("系统级 site-packages:", site.getsitepackages())
    except Exception as e:
        print("系统级 site-packages: (无法获取)", e)
    print("用户级 site-packages:", site.getusersitepackages())

    # sysconfig 路径
    print("\n[sysconfig 各类路径]")
    for k, v in sysconfig.get_paths().items():
        print(f" {k:15s}: {v}")

    # 环境变量
    print("\n[环境变量]")
    print("PATH:", os.environ.get("PATH", "未设置"))
    print("PYTHONPATH:", os.environ.get("PYTHONPATH", "未设置"))

    print("\n✅ 信息收集完成。")

if __name__ == "__main__":
    main()
