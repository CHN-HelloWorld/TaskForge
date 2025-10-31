import json
import threading
from datetime import datetime  # 新增datetime模块导入

import 自动打卡.PunchCard


def run_punch_card(name):
    try:
        # 输出线程开始的日志
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {name}: 线程开始执行打卡操作"
        )
        # 创建PunchCard对象并调用Main方法
        自动打卡.PunchCard.PunchCard(name).Main()
        # 输出线程结束的日志
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {name}: 线程完成打卡操作"
        )
    except Exception as e:
        # 输出线程执行过程中的异常日志
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] {name}: 线程执行过程中出现异常: {e}"
        )


def main():
    try:
        import os
        # 扫描自动打卡/Tokens目录下的所有JSON文件
        tokens_dir = "自动打卡/Tokens"
        if not os.path.exists(tokens_dir):
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 未找到Tokens目录，正在创建..."
            )
            os.makedirs(tokens_dir)
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Tokens目录创建完成"
            )
            return
        
        # 获取所有.json文件
        json_files = [f for f in os.listdir(tokens_dir) if f.endswith('.json')]
        
        if not json_files:
            print(
                f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] Tokens目录下没有找到任何配置文件"
            )
            return
        
        threads = []
        # 为每个用户创建一个线程
        for json_file in json_files:
            # 去掉.json后缀得到用户名
            name = json_file[:-5]
            thread = threading.Thread(target=run_punch_card, args=(name,))
            threads.append(thread)
            thread.start()

        # 等待所有线程完成
        # for thread in threads:
        # thread.join()

    except FileNotFoundError as e:
        # 输出文件未找到的异常日志
        print(
            f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 文件未找到: {e}"
        )
    except Exception as e:
        # 输出其他异常的日志
        print(f"[{datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}] 发生未知异常: {e}")
