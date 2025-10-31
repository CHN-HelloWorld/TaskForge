import Task
import 自动打卡


class Task1(Task.Task):

    def __init__(self):
        super().__init__(__class__.__name__, "自动打卡", 1, 21, 30)

    def run(self):
        自动打卡.MainRun.main()
