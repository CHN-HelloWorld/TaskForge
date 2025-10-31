import time
import datetime
import importlib
import json
import sys


#任务管理器类，用于管理所有的任务对象
class TaskManager():
    task_group = []  #任务对象队列
    module_names = []  #任务模块队列,可动态修改
    loaded_task_group = []  #已加载的任务类队列
    remove_task_group = []  #需要删除的任务对象队列
    remove_loaded_task_group = []  #需要删除的任务类（模块）队列
    is_run = False  #是否运行print_modules方法

    @classmethod
    def Remove(cls):
        for i in cls.remove_task_group:  #删除任务对象
            cls.task_group.remove(i)
        for i in cls.remove_loaded_task_group:  #从已经导入的模块中删除应该删除的任务模块
            cls.loaded_task_group.remove(i)
            try:
                del sys.modules[i]
            except:
                print(
                    "###警告：删除任务模块失败！此模块仍在已加载的模块中，这意味着与此模块同名的新模块加载时，会导致新模块加载不成功"
                )

    @classmethod
    def Run(cls):

        #修改is_run的值
        def change_is_run():
            cls.is_run = True

        #打印导入的自定义模块信息
        def print_modules():
            if cls.is_run:
                cls.is_run = False
                print("\n当前导入的模块：")
                # 遍历 sys.modules
                for module_name, module in sys.modules.items():
                    try:
                        # 检查模块对象的字符串表示是否包含目标字符串
                        if "微信自动通知" in str(module):
                            # 输出模块信息
                            print(f"模块名称: {module_name}")
                            print(f"模块对象: {module}")
                            # 如果模块有 __file__ 属性，输出文件路径
                            if hasattr(module, '__file__'):
                                print(f"模块文件路径: {module.__file__}")
                            print("-" * 40)
                    except (TypeError, UnicodeEncodeError):
                        # 捕获可能的类型错误（如模块不是字符串可表示的对象）或编码错误
                        print("无法打印当前模块信息。")
                        continue
                print("\n")

        def load_and_instantiate_modules():
            # 读取JSON文件
            with open('config.json', 'r') as file:
                TaskManager.module_names = json.load(file)

            # 遍历模块名列表
            for module_name in TaskManager.module_names:
                # 动态导入模块
                try:
                    module = importlib.import_module(module_name)

                    # 尝试从模块中反射找到与模块名相同的类，并实例化
                    try:
                        # 假设类名与模块名相同
                        class_name = module_name
                        if class_name not in TaskManager.loaded_task_group:  #如果需要实例化的类未在已加载的任务队列中就实例化此类
                            cls = getattr(module, class_name)
                            instance = cls(
                            )  #这行代码的作用是调用通过getattr(module, class_name)获取的类cls的构造函数（默认是无参数的构造函数），从而创建一个该类的实例，并将这个实例赋值给变量instance
                            TaskManager.loaded_task_group.append(class_name)
                    except AttributeError as e:
                        print(
                            f"模块 {module_name} 没有名称为 {class_name} 的类！原因: {e}")
                        try:
                            print("\n正在删除模块：", module_name,
                                  "。当前导入的模块存在错误需要删除,请检查模块名和类名是否相同")
                            del sys.modules[module_name]  #从导入的模块中删除该模块
                            print("删除成功！\n")
                            change_is_run()

                        except:
                            print(
                                "###警告：删除 %s 失败！此模块仍在已加载的模块中，这意味着与此模块同名的新模块加载时，会导致新模块加载不成功"
                                % (module_name))
                except ImportError as e:
                    print(f"导入模块 {module_name} 失败！原因: {e}")
                    continue
            print_modules()

        while True:
            cls.remove_task_group = []
            cls.remove_loaded_task_group = []
            if datetime.datetime.now(
            ).second != 0:  #如果当前时间秒数不是0就将时间秒数对齐到0（一分钟执行一次循环）
                time.sleep(60 - datetime.datetime.now().second)
                try:
                    load_and_instantiate_modules()
                except Exception as e:
                    print("配置文件信息读取失败！原因：", e)

            for i in cls.task_group:
                try:
                    i.interceptor()

                except Exception as e:
                    print("%s 执行失败,原因：" % (i.name), e)
                    print(
                        "========================###!!!执行失败!!!###============================"
                    )
                    continue
            cls.Remove()  #统一删除需要删除的任务
            time.sleep(1)
