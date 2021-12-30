# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import time
from typing import Set
from functools import partial

from .functions_main_window import *
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.core.qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

from gui.core.json_status import Status

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from .functions_main_window import MainFunctions
from .ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from .functions_main_window import *

from .flow_layout import *


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon": "icon_folder_open.svg",
            "btn_id": "btn_my_album",
            "btn_text": "我的相册",
            "btn_tooltip": "我的相册",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_restore.svg",
            "btn_id": "btn_basic_function",
            "btn_text": "图片处理",
            "btn_tooltip": "图片处理",
            "show_top": True,
            "is_active": False
        },

        {
            "btn_icon": "icon_dustbin.svg",
            "btn_id": "btn_dust_bin",
            "btn_text": "回收站",
            "btn_tooltip": "回收站",
            "show_top": False,
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "打开设置",
            "btn_tooltip": "打开设置",
            "show_top": False,
            "is_active": False
        }
    ]

    # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = []

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
        elif self.ui.left_column.menus.page_my_album_grid_layout.sender() is not None:
            return self.ui.left_column.menus.page_my_album_grid_layout.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        # self.setWindowTitle("Our Project")

        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # 禁止最大化按钮
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        # 禁止拉伸窗口大小
        # self.setFixedSize(self.width(), self.height());

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to Our Project")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_my_album)

        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        settings = Settings()
        self.settings = settings.items

        themes = Themes()
        self.themes = themes.items

        self.status_json = Status()
        self.status = self.status_json.items

        self.first_btn = PyPushButton(
            text="添加相册",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        self.first_btn.setMaximumWidth(90)
        self.first_btn.setMinimumWidth(90)
        self.first_btn.setMinimumHeight(50)
        self.ui.load_pages.left_btn_frame_layout.addWidget(self.first_btn)
        self.first_btn.clicked.connect(lambda: MainFunctions.func_add_album_btn(self))

        num_of_albums = self.status["album_status"]["num_of_albums"]
        self.row_btns = []

        # 配置相册相关按钮
        for row in range(20):
            btn1_frame = QFrame()
            btn1_frame.setObjectName(u"btns_frame_row_%d" % (row + 1))
            btn1_frame.setStyleSheet(u"background: transparent;")
            btn1_frame_layout = QHBoxLayout(btn1_frame)

            (name, details, btn_stamp) = (
                self.status_json.items["album_status"]["albums"][row]["name"],
                self.status_json.items["album_status"]["albums"][row]["details"],
                self.status_json.items["album_status"]["albums"][row]["create_time"],
            ) if row < num_of_albums else ("", "", "unabled")
            btn1 = PyPushButton(
                text=name,
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )

            btn1.setObjectName("btn_album_name_" + btn_stamp)
            btn1.setMaximumWidth(400)
            btn1.setMinimumWidth(180)
            btn1.setMinimumHeight(80)
            #btn1_frame_layout.setSpacing(0)
            btn1_frame_layout.addStretch()
            btn1_frame_layout.setAlignment(Qt.AlignLeft)
            btn1_frame_layout.addWidget(btn1)

            self.ui.load_pages.page_my_album_grid_layout.addWidget(btn1_frame, row + 1, 0)

            btn2_frame = QFrame()
            btn2_frame.setObjectName(u"btns_frame_row_%d" % (row + 1))
            btn2_frame.setStyleSheet(u"background: transparent;")
            btn2_frame_layout = QHBoxLayout(btn2_frame)
            btn2 = PyPushButton(
                text=details,
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn2.setObjectName("btn_album_details_" + btn_stamp)

            btn2.setMaximumWidth(2000)
            btn2.setMinimumWidth(650)
            btn2.setMinimumHeight(80)
            btn2_frame_layout.setSpacing(0)
            btn2_frame_layout.addStretch()
            btn2_frame_layout.addWidget(btn2)

            self.ui.load_pages.page_my_album_grid_layout.addWidget(btn2_frame, row + 1, 1)

            btn1.clicked.connect(partial(MainFunctions.func_about_album_btn, self, btn1))
            btn2.clicked.connect(partial(MainFunctions.func_about_album_btn, self, btn2))

            # 配置回收站按钮
            btn3_frame = QFrame()
            btn3_frame.setObjectName(u"btn3_frame_row_%d" % (row + 1))
            btn3_frame.setStyleSheet(u"background: transparent;")
            btn3_frame_layout = QHBoxLayout(btn3_frame)

            btn3 = PyPushButton(
                text=f"相册“{name}”的回收站",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )

            btn3.setObjectName("btn_bin_" + btn_stamp)
            btn3.setMaximumWidth(400)
            btn3.setMinimumWidth(180)
            btn3.setMinimumHeight(250)
            btn3_frame_layout.setSpacing(0)
            btn3_frame_layout.addStretch()
            btn3_frame_layout.addWidget(btn3)

            btn3.clicked.connect(partial(MainFunctions.func_about_bin_btn, self, btn3))

            self.ui.load_pages.page_dust_bin_grid_layout.addWidget(btn3_frame, row // 4, row % 4)

            if row >= num_of_albums:
                btn1.setStyleSheet(u"background: transparent;color: transparent;")
                btn2.setStyleSheet(u"background: transparent;color: transparent;")
                btn3.setStyleSheet(u"background: transparent;color: transparent;")

            self.row_btns.append((btn1, btn2, btn3))
            # self.ui.load_pages.verticalLayoutScroll.addWidget(btns_frame)

        btn1_page2 = PyPushButton(
            text="选择相册",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        # btn1_page2.setObjectName("btn_album_name_" + btn_stamp)
        btn1_page2.setMaximumWidth(100)
        btn1_page2.setMinimumWidth(100)
        btn1_page2.setMinimumHeight(80)
        btn1_page2.clicked.connect(partial(MainFunctions.func_select_album, self))
        self.ui.load_pages.page2_btn_frame_layout.addWidget(btn1_page2)

        btn_human_page2 = PyPushButton(
            text="根据人脸分类",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        # btn1_page2.setObjectName("btn_album_name_" + btn_stamp)
        btn_human_page2.setMaximumWidth(300)
        btn_human_page2.setMinimumWidth(240)
        btn_human_page2.setMinimumHeight(200)
        btn_human_page2.clicked.connect(partial(MainFunctions.func_classify_human,self))
        self.ui.load_pages.page2_h_layout.addWidget(btn_human_page2)

        btn_aniobj_page2 = PyPushButton(
            text="根据物品分类",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        # btn1_page2.setObjectName("btn_album_name_" + btn_stamp)
        btn_aniobj_page2.setMaximumWidth(300)
        btn_aniobj_page2.setMinimumWidth(240)
        btn_aniobj_page2.setMinimumHeight(200)
        btn_aniobj_page2.clicked.connect(partial(MainFunctions.func_classify_object,self))
        self.ui.load_pages.page2_h_layout.addWidget(btn_aniobj_page2)

        # self.ui.load_pages.left_column_layout.addWidget(self.last_btn)
        # self.ui.load_pages.verticalLayoutScroll.addWidget(self.last_btn_frame)
        # self.ui.load_pages.page_my_album_grid_layout.addWidget(self.last_btn_frame)
        # self.last_btn.clicked.connect(lambda: MainFunctions.add_btns_frame(self))

        # self.func_btn_11.clicked.connect(lambda: MainFunctions.select_image_directory(self))

    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)

    def get_flow_layout(self):
        return self.flow_layout

    def get_frame(self):
        return self.frame


class Worker(QThread):
    finished = Signal(dict)

    def __init__(self, mode, path=''):
        super().__init__()
        self.mode = mode
        if path != '':
            self.path = path
