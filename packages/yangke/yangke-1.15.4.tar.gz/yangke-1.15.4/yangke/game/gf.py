# game frame
import os.path
import sys
import time

from yangke.common.win.win_x64 import (get_all_window, find_window, capture_pic_undecorated, post_key, do_click,
                                       get_size_of_window, find_pic)
from yangke.objDetect.ocr import ocr
from yangke.base import show_pic
from yangke.common.config import logger


class Step:
    def __init__(self, op, target, judge, condition, wait_method=None):
        """
        定义步骤，示例：
        Step("press", "Ctrl+C", "until", Exist("人物"))

        :param wait_method: 条件不满足时，调用的方法，repeat表示重复执行op，如果取值为None，则等待而不重复操作
        """
        self.op = op

        # 按键操作则为键名，鼠标时间则为鼠标点击位置，鼠标点击位置可以通过Position类或Align定义
        self.target: Position | Align | str | tuple = target

        self.judge = judge
        self.condition: "Exist" = condition
        self.wait_method = wait_method

        self.pos = None  # 该步骤执行后，until后条件中判断的位置会保存在该变量中，便于后续使用
        self.obj = None  # 该步骤执行后，until后条件中判断的对象名会保存在该变量中，便于后续使用

    def pre_do(self, last_step):
        if last_step is None:
            return

        if isinstance(self.target, Align):
            self.target = self.target.get_window_pos(last_step.pos[0], last_step.pos[1])

    def _action(self, win_frame: "Frame"):
        if self.op == "press":
            post_key(win_frame.window, self.target)
        elif self.op == "left-click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                do_click(x, y, win_frame.window)
            elif isinstance(self.target, tuple):
                import pydirectinput
                x, y = self.target
                do_click(x, y, win_frame.window)

    def do(self, win_frame: "Frame"):
        logger.debug(f"执行步骤：{self.__str__()}")
        self._action(win_frame)
        satisfied = self.condition.satisfied(win_frame)
        while not satisfied:  # 如果结束条件不满足，则继续执行本步骤定义的操作
            if self.wait_method is None:
                time.sleep(0.5)
            else:
                self._action(win_frame)
                time.sleep(1)
            satisfied = self.condition.satisfied(win_frame)
        self.pos = self.condition.pos
        self.obj = self.condition.obj
        return True

    def __str__(self):
        return f"{self.op} {self.target} {self.judge} {self.condition.__str__()}"


class Steps:
    def __init__(self, steps):
        """
        定义游戏内操作的步骤
        """
        self.steps = steps

    def run(self, win_frame):
        """
        逐步执行Steps对象中记录的步骤
        """
        last_step: Step | None = None
        for step in self.steps:
            step: Step = step
            step.pre_do(last_step)  # 在步骤执行前进行的操作
            success = step.do(win_frame)  # 执行步骤，可能执行失败，如点击某个按钮但画面上找不到就会失败
            if not success and last_step is not None:  # 如果执行失败，就尝试再次执行上一个步骤
                last_step.do(win_frame)
                success = step.do(win_frame)

            if success:  # 如果当前步骤执行结束，就记录当前步骤
                last_step = step


class Frame:
    def __init__(self, title, game_path=None):
        """
        游戏图像识别框架

        :@param title: 游戏窗口标题，为标题的子字符串，但需要唯一确定的窗口
        :@param game_path: 游戏文件路径，如果不存在游戏窗口，则启动该可执行文件
        """
        self.set_window_size_steps = None  # 设置窗口尺寸的步骤
        self.title = title
        self.snapshot = None
        self.window = find_window(title, exact=False)
        if isinstance(self.window, dict) and len(self.window) == 1:
            _ = list(self.window.keys())[0]
            self.window_title = self.window[_]
            self.window = _
        else:
            if len(self.window) > 1:
                _ = list(self.window.keys())[0]
                self.window_title = self.window[_]
                self.window = _
                logger.warning(f"找到多个包含{title}的窗口，默认使用第一个:{self.window_title}")
            else:
                logger.error(f"未找到或找到多个包含{title}的窗口，目前不支持这种情况！")
                sys.exit()
        self.window_size = get_size_of_window(self.window, True)  # 不包括标题栏的大小
        self.udf_steps = {}

    def show_snapshot(self):
        show_pic(self.snapshot)

    def define_set_window_size(self, steps: Steps):
        self.set_window_size_steps = steps

    def define_steps(self, steps_name, steps):
        self.udf_steps.update({steps_name: steps})

    def capture_window(self, x1=0, y1=0, x2=0, y2=0):
        self.snapshot = capture_pic_undecorated(self.window)
        return self.snapshot

    def set_window_size(self, width=None, height=None):
        """
        将游戏窗口设置为指定大小
        @return:
        """
        # show_pic(self.capture_window())
        self.run_steps(self.set_window_size_steps)

    def run_steps(self, steps: Steps | str):
        if isinstance(steps, Steps):
            steps.run(self)
        else:
            if self.udf_steps.get(steps) is not None:
                self.run_steps(self.udf_steps.get(steps))

    def get_text(self, region=None):
        if region is None:
            self.capture_window()
        else:
            self.capture_window(*region)
        return ocr(self.snapshot, paragraph=True)

    def get_text_position(self, text, region=None):
        """
        获取给定文字在画面上的位置
        """
        if region is not None:
            pic = self.capture_window(*region)
        else:
            pic = self.capture_window()

    def get_window_size(self, refresh=False):
        if refresh:
            self.window_size = get_size_of_window(self.window)
        return self.window_size


class Exist:
    def __init__(self, value: str | list = "查找的文字或列表", type_="text", op="or", region: tuple | None = None):
        """
        判断画面中是否存在某个元素的类，如果条件判断过之后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息

        @param type_: 元素的类型，可取值为text或pic，分别表示文字与图片
        @param value: 元素的值的列表
        @param op: 元素值列表存在于画面中的条件是 与还是或
        @param region: 可以通过该参数指定画面区域
        """
        self.type_ = type_
        self.value = value if isinstance(value, list) else [value]
        self.op = op
        self.region = region
        self.pos = None
        self.obj = None

    def satisfied(self, win_frame: "Frame"):
        """
        画面中存在某个元素的条件是否满足，该方法执行后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息

        @param win_frame:
        @return:
        """
        if self.type_ == "text":
            text = win_frame.get_text(self.region)
            if self.op == "or":
                for v in self.value:
                    if v in text:
                        return True
                return False
            else:
                for v in self.value:
                    if v not in text:
                        return False
                return True
        elif self.type_ == "pic":
            if self.region is None:
                pic = win_frame.capture_window()
            else:
                pic = win_frame.capture_window()

            if len(self.value) == 1:
                small_pic_path = os.path.abspath(self.value[0])
                res = find_pic(small_pic_path, pic)
                self.pos = res[1]
                self.obj = self.value[0]
                return res[0]
            else:
                if self.op == "or":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        if res[0]:
                            self.obj = v
                            self.pos = res[1]
                            return True
                    return False
                elif self.op == "and":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        if not res[0]:
                            return False
                        self.obj = v
                        self.pos = res[1]
                    return True

    def __str__(self):
        return f"exist {self.value}"


class Align:
    def __init__(self, x_offset, y_offset=0):
        """
        ALign对象记录了一个元素相对另一个元素的偏移量或其他对齐信息
        """
        self.dx = x_offset
        self.dy = y_offset

    def get_window_pos(self, rx, ry):
        """
        rx, ry是Align对象参考的其他元素的坐标
        """
        x = self.dx + rx
        y = self.dy + ry
        return x, y

    def get_screen_pos(self, rx, ry):
        return 0, 0


class Position:
    def __init__(self, value, align: str | Align = 'center', region=None):
        """
        定义画面上的位置对象

        @param value:
        @param align:
        """
        self.value = value
        self.region = region

    def get_point(self, win_frame: "Frame"):
        """
        获取位置在画面上的相对坐标
        @param win_frame:
        @return:
        """
        if isinstance(self.value, str):
            pos = win_frame.get_text_position(self.value)
            return pos
        else:
            return None


class Region:
    def __init__(self, win_frame: "Frame"):
        """
        定义窗口中的某个区域，通过该类可以获取(x,y,w,h)这种类型的相对区域坐标
        """
        self.frame = win_frame
        self.width_window, self.height_window = win_frame.get_window_size()

    def get_region(self, align="center", width_child=0, height_child=0):
        """
        根据传入的区域定义，获取区域的数字范围，例如：
        region.get_region("center", 100, 100)  # 表示窗口中间100*100范围的(x,y,w,h)定义
        """
        if width_child == 0:  # 如果不指定区域的宽和高，则默认宽和高等于窗口的宽和高
            width_child = self.width_window
        if height_child == 0:
            height_child = self.height_window
        if align == "center":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "left":
            left_pad = 0
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "right":
            left_pad = self.width_window - width_child
            top_pad = int((self.height_window - height_child) / 2)
        elif align == "top":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = 0
        elif align == "bottom":
            left_pad = int((self.width_window - width_child) / 2)
            top_pad = self.height_window - height_child
        else:
            left_pad = 0
            top_pad = 0
        return left_pad, top_pad, width_child, height_child


if __name__ == "__main__":
    # logger.debug(ocr("temp.png", paragraph=False))
    # frame = Frame('天谕-无束缚3D')
    frame = Frame('天谕-无束缚3D幻想网游')
    # frame = Frame('记事本')
    # frame = Frame('炎火前哨, 宁梦')
    r = Region(frame)
    # steps_1 = Steps(
    #     steps=[
    #         # 按Esc键，直到窗口中心区域(317, 532)大小范围内出现文字"游戏设置"
    #         Step("press", "escape", "until", Exist(value="游戏设置", region=r.get_region("center", 317, 532))),
    #
    #         # 单击中心区域的【游戏设置】，直到中心区域(874, 609)出现【分辨率】
    #         Step("left-click", Position("游戏设置", region=r.get_region("center", 874, 609)), "until",
    #              Exist(value="分辨率", region=r.get_region("center", 874, 609))),
    #
    #         # 单机
    #         Step("left-click", Position("分辨率", align=Align(20)), "until", Exist())
    #     ])
    # frame.define_set_window_size(steps=steps_1)
    # frame.set_window_size()

    steps_2 = Steps(
        steps=[
            Step("press", "numpad0", "until", Exist(value='pic1.png', type_='pic'), wait_method="repeat"),
            Step("left-click", Align(397, 16), "until", Exist("门派"), wait_method="repeat"),
            Step("left-click", Align(0, 0), "until", Exist("苏澜郡"), wait_method="repeat"),
            Step("left-click", Align(0, 0), "until", Exist("汐族"), wait_method="repeat"),
        ]
    )
    frame.define_steps("打开苏澜郡声望面板", steps_2)
    frame.run_steps("打开苏澜郡声望面板")

    # frame.capture_window()
    # logger.debug(frame.get_text())
