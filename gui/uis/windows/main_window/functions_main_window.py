import sys

import numpy

from gui.core.qt_core import *
from .ui_main import *
from .flow_layout import *
import os
import json
from math import floor, ceil
from gui.core.qt_core import *
from gui.widgets import *
import datetime
from functools import partial
from face_recognition import *
from scipy.spatial.distance import pdist
import cv2
import shutil
from torchvision import *
import torch

cur_album = ""

style = '''
    QPushButton {{
    	border: none;
        padding-left: 10px;
        padding-right: 5px;
        color: {color};
    	border-radius: {radius};	
    	background-color: {bg_color};
    }}
    QPushButton:hover {{
    	background-color: {bg_color_hover};
    }}
    QPushButton:pressed {{	
    	background-color: {bg_color_pressed};
    }}
    '''
dialog_dict = {}


def make_dirs(album_name: str):
    _translate = ["dog", "horse", "elephant", "butterfly", "chicken", "cat", "cow", "sheep", "spider",
                  "squirrel", "human"]
    setting = Settings()
    path = setting.items["app_path"] + "\\" + album_name + "result"
    if not os.path.exists(path):
        os.makedirs(path)
        for label in _translate:
            os.makedirs(os.path.join(path, label))


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


class AniObj(object):
    def __init__(self):
        self.translate = ["dog", "horse", "elephant", "butterfly", "chicken", "cat", "cow", "sheep", "spider",
                          "squirrel", "human"]
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self._net = models.resnet34(pretrained=False)
        fc_inputs = self._net.fc.in_features
        self._net.fc = torch.nn.Sequential(
            torch.nn.Linear(fc_inputs, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.4),
            torch.nn.Linear(256, 11),
            torch.nn.LogSoftmax(dim=1)
        )
        self._net.load_state_dict(torch.load("resources/AniObjClass.pkl", self._device))
        torch.no_grad()
        self._net = self._net.to(self._device)
        self._net.eval()

    def out(self, image):  # 这个最重要
        t_img = load_image_file(image)
        t_img = cv2.resize(t_img, (224, 336))
        t_img = transform(t_img)
        t_img = t_img.unsqueeze(0)
        t_img = t_img.to(self._device)
        outputs = self._net(t_img)

        predicted, index = torch.max(outputs, 1)  # torch.max(tensorA,dim):dim表示指定的维度,返回指定维度的最大数和对应下标
        degree = int(index[0])
        return self.translate[degree]


func_aniobj = AniObj()


class MainFunctions():
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    def func_about_album_btn(self, btn_object: object):
        object_name = btn_object.objectName()
        if dialog_dict.get(object_name) is not None:
            return

        dialog_dict[object_name] = 1

        print("in func_about_album_btn:" + object_name)
        if object_name[-7:] == "unabled":
            return
            # QMessageBox.information(self, "", "别瞎点！！！")

        def get_name_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["name"]

        def get_details_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["details"]

        def get_pos_by_time(self, create_time: str):
            cnt = 0
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return cnt
                cnt += 1

        time_stamp = object_name[-14:]

        if object_name[:15] == "btn_album_name_":
            dialog = QDialog()
            # dialog.resize(400, 200)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.setWindowTitle(get_name_by_time(self, time_stamp))
            dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

            dialog_layout = QVBoxLayout(dialog)
            btn_change_album_name_frame = QFrame()
            btn_change_album_name_frame.setStyleSheet(u"background: transparent;")
            btn_change_album_name_frame_layout = QHBoxLayout(btn_change_album_name_frame)
            btn_change_album_name_frame_layout.setAlignment(Qt.AlignCenter)

            btn_change_album_name = PyPushButton(
                text="更改相册名称",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_change_album_name.setMinimumWidth(100)
            btn_change_album_name.setMinimumHeight(50)
            btn_change_album_name_frame_layout.addWidget(btn_change_album_name)

            btn_delete_album_frame = QFrame()
            btn_delete_album_frame.setStyleSheet(u"background: transparent;")
            btn_delete_album_frame_layout = QHBoxLayout(btn_delete_album_frame)
            btn_delete_album_frame_layout.setAlignment(Qt.AlignCenter)

            btn_delete_album = PyPushButton(
                text="删除此相册",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_delete_album.setMinimumWidth(100)
            btn_delete_album.setMinimumHeight(50)
            btn_delete_album_frame_layout.addWidget(btn_delete_album)

            btn_back_frame = QFrame()
            btn_back_frame.setStyleSheet(u"background: transparent;")
            btn_back_frame_layout = QHBoxLayout(btn_back_frame)
            btn_back_frame_layout.setAlignment(Qt.AlignCenter)

            btn_back = PyPushButton(
                text="返回",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_back.setMinimumWidth(100)
            btn_back.setMinimumHeight(50)
            btn_back_frame_layout.addWidget(btn_back)

            dialog_layout.addWidget(btn_change_album_name_frame)
            dialog_layout.addWidget(btn_delete_album_frame)
            dialog_layout.addWidget(btn_back_frame)

            def func_btn_change_name(self, dialog1):
                dialog = QDialog()
                dialog.setWindowTitle("更改相册名")
                dialog.setWindowModality(Qt.ApplicationModal)
                # dialog.resize(800, 500)
                dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))
                dialog_layout = QVBoxLayout(dialog)

                label1 = QLabel()
                label1.setObjectName(u"label1")
                label1.setStyleSheet(u"background: transparent;")
                label1.setText("请输入相册新名称：")
                label1.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
                label1.setAlignment(Qt.AlignCenter)
                dialog_layout.addWidget(label1)

                album_name_box = QPlainTextEdit()
                album_name_box.setObjectName("album_name_box")
                album_name_box.setStyleSheet(f'''
                            font: 20pt "Microsoft YaHei";
                            color: {self.themes["app_color"]["white"]};
                        ''')
                album_name_box.setMinimumWidth(750)
                album_name_box.setMinimumHeight(70)
                album_name_box.setMaximumHeight(70)
                dialog_layout.addWidget(album_name_box)

                btn_check_frame = QFrame()
                btn_check_frame.setObjectName("btn_add_images_frame")
                btn_check_frame.setStyleSheet(u"background: transparent;")
                btn_check_frame_layout = QHBoxLayout(btn_check_frame)
                btn_check_frame_layout.setAlignment(Qt.AlignCenter)

                btn_check = PyPushButton(
                    text="确认",
                    radius=8,
                    color=self.themes['app_color']['white'],
                    bg_color=self.themes['app_color']['dark_one'],
                    bg_color_hover=self.themes['app_color']['pink'],
                    bg_color_pressed=self.themes['app_color']['pink']
                )
                btn_check.setMinimumWidth(100)
                btn_check.setMaximumWidth(60)
                btn_check.setMinimumHeight(70)

                btn_check_frame_layout.addWidget(btn_check)

                btn_cancel_frame = QFrame()
                btn_cancel_frame.setStyleSheet(u"background: transparent;")
                btn_cancel_frame_layout = QHBoxLayout(btn_cancel_frame)
                btn_cancel_frame_layout.setAlignment(Qt.AlignCenter)
                btn_cancel = PyPushButton(
                    text="取消",
                    radius=8,
                    color=self.themes['app_color']['white'],
                    bg_color=self.themes['app_color']['dark_one'],
                    bg_color_hover=self.themes['app_color']['pink'],
                    bg_color_pressed=self.themes['app_color']['pink']
                )
                btn_cancel.setMinimumWidth(100)
                btn_cancel.setMaximumWidth(60)
                btn_cancel.setMinimumHeight(70)
                btn_cancel_frame_layout.addWidget(btn_cancel)

                btns_frame = QWidget()
                btns_frame.setStyleSheet(u"background: transparent;")
                btns_frame_layout = QHBoxLayout(btns_frame)
                btns_frame_layout.addWidget(btn_check_frame)
                btns_frame_layout.addWidget(btn_cancel_frame)
                btns_frame_layout.setAlignment(Qt.AlignCenter)
                btns_frame_layout.addStretch()
                btns_frame_layout.setSpacing(50)

                dialog_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)
                dialog.close()

                def func_check(dialog):
                    name = album_name_box.toPlainText()
                    cnt = 0
                    for album in self.status_json.items["album_status"]["albums"]:
                        if album["create_time"] == time_stamp:
                            album["name"] = name
                            break
                        cnt += 1

                    self.status_json.items["album_status"]["albums"][cnt]["name"] = name
                    self.status_json.serialize()
                    self.row_btns[cnt][0].setText(name)

                    dialog.close()

                def func_cancel(dialog):
                    dialog.close()

                btn_check.clicked.connect(partial(func_check, dialog))
                btn_cancel.clicked.connect(partial(func_cancel, dialog))
                dialog.exec_()
                # dialog1.close()

            def func_btn_delete_album(self, dialog, time_stamp: str):
                cnt = 0
                for album in self.status_json.items["album_status"]["albums"]:
                    if album["create_time"] == time_stamp:
                        self.status_json.items["album_status"]["albums"].remove(album)
                        self.status_json.items["album_status"]["num_of_albums"] -= 1
                        self.status_json.serialize()
                        break
                    cnt += 1

                num_albums = len(self.row_btns)
                for row in range(cnt, num_albums - 1):
                    self.row_btns[row][0].setText(self.row_btns[row + 1][0].text())
                    self.row_btns[row][0].setStyleSheet(self.row_btns[row + 1][0].styleSheet())
                    self.row_btns[row][0].setObjectName(self.row_btns[row + 1][0].objectName())

                    self.row_btns[row][1].setText(self.row_btns[row + 1][1].text())
                    self.row_btns[row][1].setStyleSheet(self.row_btns[row + 1][1].styleSheet())
                    self.row_btns[row][1].setObjectName(self.row_btns[row + 1][1].objectName())

                    self.row_btns[row][2].setText(self.row_btns[row + 1][2].text())
                    self.row_btns[row][2].setStyleSheet(self.row_btns[row + 1][2].styleSheet())
                    self.row_btns[row][2].setObjectName(self.row_btns[row + 1][2].objectName())

                self.row_btns.pop()

                dialog.close()

            def func_btn_back(dialog):
                dialog.close()

            btn_change_album_name.clicked.connect(partial(func_btn_change_name, self, dialog))
            btn_delete_album.clicked.connect(partial(func_btn_delete_album, self, dialog, time_stamp))
            btn_back.clicked.connect(partial(func_btn_back, dialog))

            dialog.exec_()
            dialog_dict.clear()

        elif object_name[:18] == "btn_album_details_":
            dialog = QDialog()
            # dialog.resize(800, 300)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.setWindowTitle(f"相册 ”{get_name_by_time(self, time_stamp)}“")
            dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

            # 最大的是纵向布局 纵向布局最下方是添加照片和返回两个按钮 纵向布局上方是网格布局用于展示照片 且含有滚动条
            dialog_v_layout = QVBoxLayout(dialog)

            btn_add_images_frame = QFrame()
            btn_add_images_frame.setObjectName("btn_add_images_frame")
            btn_add_images_frame.setStyleSheet(u"background: transparent;")
            btn_add_images_frame_layout = QHBoxLayout(btn_add_images_frame)
            btn_add_images_frame_layout.setAlignment(Qt.AlignCenter)

            btn_add_images = PyPushButton(
                text="添加照片",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_add_images.setMinimumWidth(200)
            btn_add_images.setMaximumWidth(300)
            btn_add_images.setMinimumHeight(70)
            btn_add_images_frame_layout.addWidget(btn_add_images)

            btn_back_frame = QFrame()
            btn_back_frame.setStyleSheet(u"background: transparent;")
            btn_back_frame_layout = QHBoxLayout(btn_back_frame)
            btn_back_frame_layout.setAlignment(Qt.AlignCenter)
            btn_back = PyPushButton(
                text="返回",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_back.setMinimumWidth(100)
            btn_back.setMaximumWidth(200)
            btn_back.setMinimumHeight(70)
            btn_back_frame_layout.addWidget(btn_back)

            btn_search_same_frame = QFrame()
            btn_search_same_frame.setStyleSheet(u"background: transparent;")
            btn_search_same_frame_layout = QHBoxLayout(btn_search_same_frame)
            btn_search_same_frame_layout.setAlignment(Qt.AlignCenter)
            btn_search_same = PyPushButton(
                text="查看相似图片",
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )
            btn_search_same.setMinimumWidth(250)
            btn_search_same.setMaximumWidth(320)
            btn_search_same.setMinimumHeight(70)
            btn_search_same_frame_layout.addWidget(btn_search_same)

            btns_frame = QWidget()
            btns_frame.setStyleSheet(u"background: transparent;")
            btns_frame_layout = QHBoxLayout(btns_frame)
            btns_frame_layout.addWidget(btn_add_images_frame)
            btns_frame_layout.addWidget(btn_search_same_frame)
            btns_frame_layout.addWidget(btn_back_frame)
            btns_frame_layout.setAlignment(Qt.AlignCenter)
            btns_frame_layout.addStretch()
            btns_frame_layout.setSpacing(50)

            scrollArea = QScrollArea(dialog)
            scrollArea.setWidgetResizable(True)
            scrollAreaWidgetContents = QWidget(scrollArea)
            # scrollAreaWidgetContents.setGeometry()
            scrollArea.setWidget(scrollAreaWidgetContents)
            scrollArea.setMinimumWidth(1200)
            scrollArea.setMinimumHeight(800)

            dialog_v_layout.addWidget(scrollArea, Qt.AlignCenter, Qt.AlignCenter)
            dialog_v_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

            image_grid_scroll_layout = QGridLayout(scrollAreaWidgetContents)
            image_grid_scroll_layout.setSpacing(10)

            col_num = 4  # 列数
            list_images = self.status_json.items["album_status"]["albums"][get_pos_by_time(self, time_stamp)][
                "image_paths"]  # 图片路径的列表
            image_num = len(list_images)
            row_num = ceil(image_num / col_num)

            for i in range(row_num):
                for j in range(col_num):
                    if i * col_num + j + 1 > image_num:
                        break

                    image_frame = QFrame()
                    image_frame.setObjectName(u"image_frame")
                    image_frame.setStyleSheet(u"background: transparent;")
                    image_frame_layout = QVBoxLayout(image_frame)
                    image_frame_layout.setAlignment(Qt.AlignCenter)

                    image_label = QLabel()
                    image_label.setPixmap(QPixmap(list_images[i * col_num + j]))
                    image_label.setMinimumWidth(200)
                    image_label.setMaximumWidth(360)
                    image_label.setMinimumHeight(200)
                    image_label.setMaximumHeight(360)
                    image_label.setAlignment(Qt.AlignCenter)

                    name_label = QLabel()
                    name_label.setObjectName(u"name_label")
                    name_label.setStyleSheet(u"background: transparent;")
                    name = os.path.split(list_images[i * col_num + j])[1]
                    name_label.setText(name if len(name) < 20 else name[-20:])
                    name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                    name_label.setAlignment(Qt.AlignCenter)

                    image_frame_layout.addWidget(image_label)
                    image_frame_layout.addWidget(name_label)

                    image_grid_scroll_layout.addWidget(image_frame, i, j)

            def func_btn_add_images(self, dialog):
                image_paths = QFileDialog.getOpenFileNames(dialog, "选择图片", "C:/",
                                                           "Image Files (*.jpg *.png *.jpeg *.bmp *.tiff)")[0]

                if len(image_paths) == 0:
                    return

                cnt = 0
                for image_path in image_paths:
                    image_path = os.path.normpath(image_path)
                    if image_path not in list_images:
                        cnt += 1
                        list_images.append(image_path)

                self.status_json.serialize()

                for i in range(image_grid_scroll_layout.count()):
                    image_grid_scroll_layout.itemAt(i).widget().deleteLater()

                image_num = len(list_images)
                row_num = ceil(image_num / col_num)

                for i in range(row_num):
                    for j in range(col_num):
                        if i * col_num + j + 1 > image_num:
                            break

                        image_frame = QFrame()
                        image_frame.setObjectName(u"image_frame")
                        image_frame.setStyleSheet(u"background: transparent;")
                        image_frame_layout = QVBoxLayout(image_frame)
                        image_frame_layout.setAlignment(Qt.AlignCenter)

                        image_label = QLabel()
                        image_label.setPixmap(QPixmap(list_images[i * col_num + j]))
                        image_label.setMinimumWidth(200)
                        image_label.setMaximumWidth(360)
                        image_label.setMinimumHeight(200)
                        image_label.setMaximumHeight(360)
                        image_label.setAlignment(Qt.AlignCenter)

                        name_label = QLabel()
                        name_label.setObjectName(u"name_label")
                        name_label.setStyleSheet(u"background: transparent;")
                        name = os.path.split(list_images[i * col_num + j])[1]
                        name_label.setText(name if len(name) < 20 else name[-20:])
                        name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                        name_label.setAlignment(Qt.AlignCenter)

                        image_frame_layout.addWidget(image_label)
                        image_frame_layout.addWidget(name_label)

                        image_grid_scroll_layout.addWidget(image_frame, i, j)

            def func_btn_search_same(self):
                dialog_search = QDialog()
                dialog_search.setWindowTitle("查看相似图片")
                dialog_search.setWindowModality(Qt.ApplicationModal)
                # dialog_search.resize(800, 400)
                dialog_search.setStyleSheet(
                    u"background: {0};font-size: 14pt".format(self.themes["app_color"]["bg_one"]))
                dialog_search_v_layout = QVBoxLayout(dialog_search)
                # 最大的是纵向布局 纵向布局最下方是添加照片和返回两个按钮 纵向布局上方是网格布局用于展示照片 且含有滚动条

                btn_delete_same_frame = QFrame()
                btn_delete_same_frame.setObjectName("btn_add_images_frame")
                btn_delete_same_frame.setStyleSheet(u"background: transparent;")
                btn_delete_same_frame_layout = QHBoxLayout(btn_delete_same_frame)
                btn_delete_same_frame_layout.setAlignment(Qt.AlignCenter)

                btn_delete_same = PyPushButton(
                    text="删除相似照片",
                    radius=8,
                    color=self.themes['app_color']['white'],
                    bg_color=self.themes['app_color']['dark_one'],
                    bg_color_hover=self.themes['app_color']['pink'],
                    bg_color_pressed=self.themes['app_color']['pink']
                )
                btn_delete_same.setMinimumWidth(200)
                btn_delete_same.setMaximumWidth(300)
                btn_delete_same.setMinimumHeight(70)
                btn_delete_same_frame_layout.addWidget(btn_delete_same)

                btn_back1_frame = QFrame()
                btn_back1_frame.setStyleSheet(u"background: transparent;")
                btn_back1_frame_layout = QHBoxLayout(btn_back1_frame)
                btn_back1_frame_layout.setAlignment(Qt.AlignCenter)
                btn_back1 = PyPushButton(
                    text="返回",
                    radius=8,
                    color=self.themes['app_color']['white'],
                    bg_color=self.themes['app_color']['dark_one'],
                    bg_color_hover=self.themes['app_color']['pink'],
                    bg_color_pressed=self.themes['app_color']['pink']
                )
                btn_back1.setMinimumWidth(100)
                btn_back1.setMaximumWidth(200)
                btn_back1.setMinimumHeight(70)
                btn_back1_frame_layout.addWidget(btn_back1)

                btns1_frame = QWidget()
                btns1_frame.setStyleSheet(u"background: transparent;")
                btns1_frame_layout = QHBoxLayout(btns1_frame)
                btns1_frame_layout.addWidget(btn_delete_same_frame)
                btns1_frame_layout.addWidget(btn_back1_frame)
                btns1_frame_layout.setAlignment(Qt.AlignCenter)
                btns1_frame_layout.addStretch()
                btns1_frame_layout.setSpacing(50)

                scrollArea1 = QScrollArea(dialog_search)
                scrollArea1.setWidgetResizable(True)
                scrollArea1WidgetContents = QWidget(scrollArea1)
                # scrollAreaWidgetContents.setGeometry()
                scrollArea1.setWidget(scrollArea1WidgetContents)
                scrollArea1.setMinimumWidth(1100)
                scrollArea1.setMinimumHeight(900)

                dialog_search_v_layout.addWidget(scrollArea1, Qt.AlignCenter, Qt.AlignCenter)
                dialog_search_v_layout.addWidget(btns1_frame, Qt.AlignCenter, Qt.AlignCenter)

                same_image_grid_scroll_layout = QGridLayout(scrollArea1WidgetContents)
                same_image_grid_scroll_layout.setSpacing(10)
                same_image_grid_scroll_layout.setAlignment(Qt.AlignCenter)

                # 编写搜索中 和 搜索后的结果展示
                label_searching = QLabel()
                label_searching.setStyleSheet(u"background: transparent;")
                label_searching.setText("搜索中......")
                label_searching.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 30pt;color:white")
                label_searching.setAlignment(Qt.AlignCenter)

                same_image_grid_scroll_layout.addWidget(label_searching)
                dialog_search.show()

                # 开始搜索相似图片
                list_img_array = []
                for image in list_images:
                    list_img_array.append(cv2.resize(load_image_file(image), (50, 50)).flatten())

                same_pictures = []
                all_same_pictures = []  # a flag

                image_num = len(list_images)

                for i in range(image_num):
                    the_same_pictures_to_i = [i]

                    if i in all_same_pictures:
                        same_pictures.append(the_same_pictures_to_i)
                    else:
                        for j in range(i + 1, image_num):
                            if pdist([list_img_array[i], list_img_array[j]], "euclid") < 0.1:
                                the_same_pictures_to_i.append(j)
                                all_same_pictures.append(j)

                        same_pictures.append(the_same_pictures_to_i)

                if len(all_same_pictures) == 0:
                    label_searching.setText("无相似图片")
                else:
                    for i in range(same_image_grid_scroll_layout.count()):
                        same_image_grid_scroll_layout.itemAt(i).widget().deleteLater()
                cnt = 0
                for same_pictures_to_i in same_pictures:
                    if (len(same_pictures_to_i)) > 1:
                        first_img_num = same_pictures_to_i.pop(0)

                        image_frame = QFrame()
                        image_frame.setObjectName(u"image_frame")
                        image_frame.setStyleSheet(u"background: transparent;")
                        image_frame_layout = QVBoxLayout(image_frame)

                        image_label = QLabel()
                        image_label.setPixmap(QPixmap(list_images[first_img_num]))
                        image_label.setMinimumWidth(200)
                        image_label.setMaximumWidth(360)
                        image_label.setMinimumHeight(200)
                        image_label.setMaximumHeight(360)
                        image_label.setAlignment(Qt.AlignCenter)

                        name_label = QLabel()
                        name_label.setObjectName(u"name_label")
                        name_label.setStyleSheet(u"background: transparent;")
                        name = os.path.split(list_images[first_img_num])[1]
                        name_label.setText(name if len(name) < 20 else name[-20:])
                        name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                        name_label.setAlignment(Qt.AlignCenter)

                        image_frame_layout.addWidget(image_label)
                        image_frame_layout.addWidget(name_label)

                        same_image_grid_scroll_layout.addWidget(image_frame, cnt, 0)

                        col1_label = QLabel()
                        col1_label.setStyleSheet(u"background: transparent;")
                        col1_label.setText("与\n" + os.path.split(list_images[first_img_num])[1] + "\n 相似的图片有：")
                        col1_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                        col1_label.setMinimumWidth(150)
                        col1_label.setMinimumHeight(200)
                        col1_label.setAlignment(Qt.AlignCenter)
                        col1_label_frame = QFrame()
                        col1_label_frame.setStyleSheet(u"background: transparent;")
                        col1_label_frame_layout = QHBoxLayout(col1_label_frame)
                        col1_label_frame_layout.addWidget(col1_label)

                        same_image_grid_scroll_layout.addWidget(col1_label_frame, cnt, 1)

                        # for col in range(2,2+len(same_pictures_to_i))
                        for index, value in enumerate(same_pictures_to_i):
                            col = index + 2
                            image_frame = QFrame()
                            image_frame.setObjectName(u"image_frame")
                            image_frame.setStyleSheet(u"background: transparent;")
                            image_frame_layout = QVBoxLayout(image_frame)

                            image_label = QLabel()
                            image_label.setPixmap(QPixmap(list_images[value]))
                            image_label.setMinimumWidth(200)
                            image_label.setMaximumWidth(360)
                            image_label.setMinimumHeight(200)
                            image_label.setMaximumHeight(360)
                            image_label.setAlignment(Qt.AlignCenter)

                            name_label = QLabel()
                            name_label.setObjectName(u"name_label")
                            name_label.setStyleSheet(u"background: transparent;")
                            name = os.path.split(list_images[value])[1]
                            name_label.setText(name if len(name) < 20 else name[-20:])
                            name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                            name_label.setAlignment(Qt.AlignCenter)

                            image_frame_layout.addWidget(image_label)
                            image_frame_layout.addWidget(name_label)

                            same_image_grid_scroll_layout.addWidget(image_frame, cnt, col)

                        cnt += 1

                def func_btn_delete_same(dialog_search):
                    dialog_check = QDialog()
                    dialog_check.setWindowTitle("删除照片确认")
                    dialog_check.setWindowModality(Qt.ApplicationModal)
                    # dialog_search.resize(800, 400)
                    dialog_check.setStyleSheet(
                        u"background: {0};font-size: 14pt".format(self.themes["app_color"]["bg_one"]))
                    dialog_check_v_layout = QVBoxLayout(dialog_check)
                    dialog_check_v_layout.setSpacing(30)
                    dialog_check_v_layout.setContentsMargins(30, 20, 30, 10)

                    label1 = QLabel()
                    label1.setStyleSheet(u"background: transparent;")
                    label1.setText(f"确认从相册”{get_name_by_time(self, time_stamp)}“中删除以下照片吗？")
                    label1.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                    label1.setAlignment(Qt.AlignCenter)
                    dialog_check_v_layout.addWidget(label1)

                    for delete_image in all_same_pictures:
                        label2 = QLabel()
                        label2.setStyleSheet(u"background: transparent;")
                        label2.setText(os.path.split(list_images[delete_image])[1])
                        label2.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                        label2.setAlignment(Qt.AlignCenter)
                        dialog_check_v_layout.addWidget(label2)

                    btn_check_frame = QFrame()
                    btn_check_frame.setObjectName("btn_add_images_frame")
                    btn_check_frame.setStyleSheet(u"background: transparent;")
                    btn_check_frame_layout = QHBoxLayout(btn_check_frame)
                    btn_check_frame_layout.setAlignment(Qt.AlignCenter)

                    btn_check = PyPushButton(
                        text="确认",
                        radius=8,
                        color=self.themes['app_color']['white'],
                        bg_color=self.themes['app_color']['dark_one'],
                        bg_color_hover=self.themes['app_color']['pink'],
                        bg_color_pressed=self.themes['app_color']['pink']
                    )
                    btn_check.setMinimumWidth(100)
                    btn_check.setMaximumWidth(60)
                    btn_check.setMinimumHeight(70)

                    btn_check_frame_layout.addWidget(btn_check)

                    btn_cancel_frame = QFrame()
                    btn_cancel_frame.setStyleSheet(u"background: transparent;")
                    btn_cancel_frame_layout = QHBoxLayout(btn_cancel_frame)
                    btn_cancel_frame_layout.setAlignment(Qt.AlignCenter)
                    btn_cancel = PyPushButton(
                        text="取消",
                        radius=8,
                        color=self.themes['app_color']['white'],
                        bg_color=self.themes['app_color']['dark_one'],
                        bg_color_hover=self.themes['app_color']['pink'],
                        bg_color_pressed=self.themes['app_color']['pink']
                    )
                    btn_cancel.setMinimumWidth(100)
                    btn_cancel.setMaximumWidth(60)
                    btn_cancel.setMinimumHeight(70)
                    btn_cancel_frame_layout.addWidget(btn_cancel)

                    btns_frame = QWidget()
                    btns_frame.setStyleSheet(u"background: transparent;")
                    btns_frame_layout = QHBoxLayout(btns_frame)
                    btns_frame_layout.addWidget(btn_check_frame)
                    btns_frame_layout.addWidget(btn_cancel_frame)
                    btns_frame_layout.setAlignment(Qt.AlignCenter)
                    btns_frame_layout.addStretch()
                    btns_frame_layout.setSpacing(50)

                    dialog_check_v_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

                    def func_btn_check(dialog_check):
                        all_same_pictures.sort(reverse=True)
                        album_num = get_pos_by_time(self, time_stamp)
                        for ___ in all_same_pictures:
                            self.status_json.items["album_status"]["albums"][album_num]["bin"].append(list_images[___])
                            list_images.pop(___)

                        self.status_json.serialize()
                        dialog_check.close()
                        for i in range(image_grid_scroll_layout.count()):
                            image_grid_scroll_layout.itemAt(i).widget().deleteLater()

                        image_num = len(list_images)
                        row_num = ceil(image_num / col_num)

                        for i in range(row_num):
                            for j in range(col_num):
                                if i * col_num + j + 1 > image_num:
                                    break

                                image_frame = QFrame()
                                image_frame.setObjectName(u"image_frame")
                                image_frame.setStyleSheet(u"background: transparent;")
                                image_frame_layout = QVBoxLayout(image_frame)

                                image_label = QLabel()
                                image_label.setPixmap(QPixmap(list_images[i * col_num + j]))
                                image_label.setMinimumWidth(200)
                                image_label.setMaximumWidth(360)
                                image_label.setMinimumHeight(200)
                                image_label.setMaximumHeight(360)
                                image_label.setAlignment(Qt.AlignCenter)

                                name_label = QLabel()
                                name_label.setObjectName(u"name_label")
                                name_label.setStyleSheet(u"background: transparent;")
                                name = os.path.split(list_images[i * col_num + j])[1]
                                name_label.setText(name if len(name) < 20 else name[-20:])
                                name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                                name_label.setAlignment(Qt.AlignCenter)

                                image_frame_layout.addWidget(image_label)
                                image_frame_layout.addWidget(name_label)

                                image_grid_scroll_layout.addWidget(image_frame, i, j)

                    def func_btn_cancel(dialog_check):
                        dialog_check.close()

                    btn_check.clicked.connect(partial(func_btn_check, dialog_check))
                    btn_cancel.clicked.connect(partial(func_btn_cancel, dialog_check))

                    dialog_check.exec()
                    dialog_search.close()

                def func_btn_back1(dialog_search):
                    dialog_search.close()

                btn_delete_same.clicked.connect(partial(func_btn_delete_same, dialog_search))
                btn_back1.clicked.connect(partial(func_btn_back1, dialog_search))

                dialog_search.exec()

            def func_btn_back(dialog):
                dialog.close()

            btn_add_images.clicked.connect(partial(func_btn_add_images, self, dialog))
            btn_search_same.clicked.connect(partial(func_btn_search_same, self))
            btn_back.clicked.connect(partial(func_btn_back, dialog))

            dialog.exec_()
            dialog_dict.clear()

    def func_add_album_btn(self):
        dialog = QDialog()
        dialog.setWindowTitle("新建相册")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(800, 500)
        dialog.setStyleSheet(u"background: {0};font-size: 14pt".format(self.themes["app_color"]["bg_one"]))
        dialog_layout = QVBoxLayout(dialog)

        label1 = QLabel()
        label1.setObjectName(u"label1")
        label1.setStyleSheet(u"background: transparent;")
        label1.setText("请输入相册名称：")
        label1.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        label1.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(label1)

        album_name_box = QPlainTextEdit()
        album_name_box.setObjectName("album_name_box")
        album_name_box.setStyleSheet(f'''
            font: 20pt "Microsoft YaHei";
            color: {self.themes["app_color"]["white"]};
        ''')
        album_name_box.setMinimumWidth(750)
        album_name_box.setMinimumHeight(70)
        album_name_box.setMaximumHeight(70)
        dialog_layout.addWidget(album_name_box)

        label2 = QLabel()
        label2.setObjectName(u"label2")
        label2.setStyleSheet(u"background: transparent;")
        label2.setText("请输入相册的详细信息：")
        label2.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        label2.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(label2)

        album_details_box = QPlainTextEdit()
        album_details_box.setObjectName("album_details_box")
        album_details_box.setStyleSheet(f'''
            font: 20pt "Microsoft YaHei";
            color: {self.themes["app_color"]["white"]};
        ''')
        dialog_layout.addWidget(album_details_box)

        btn_check_frame = QFrame()
        btn_check_frame.setObjectName("btn_check_frame")
        btn_check_frame.setStyleSheet(u"background: transparent;")
        btn_check_frame_layout = QHBoxLayout(btn_check_frame)
        btn_check_frame_layout.setAlignment(Qt.AlignCenter)

        btn_check = PyPushButton(
            text="确认",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_check.setMinimumWidth(100)
        btn_check.setMaximumWidth(60)
        btn_check.setMinimumHeight(70)

        btn_check_frame_layout.addWidget(btn_check)

        btn_cancel_frame = QFrame()
        btn_cancel_frame.setStyleSheet(u"background: transparent;")
        btn_cancel_frame_layout = QHBoxLayout(btn_cancel_frame)
        btn_cancel_frame_layout.setAlignment(Qt.AlignCenter)
        btn_cancel = PyPushButton(
            text="取消",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_cancel.setMinimumWidth(100)
        btn_cancel.setMaximumWidth(60)
        btn_cancel.setMinimumHeight(70)
        btn_cancel_frame_layout.addWidget(btn_cancel)

        btns_frame = QWidget()
        btns_frame.setStyleSheet(u"background: transparent;")
        btns_frame_layout = QHBoxLayout(btns_frame)
        btns_frame_layout.addWidget(btn_check_frame)
        btns_frame_layout.addWidget(btn_cancel_frame)
        btns_frame_layout.setAlignment(Qt.AlignCenter)
        btns_frame_layout.addStretch()
        btns_frame_layout.setSpacing(50)

        dialog_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

        def func_add_album(self, dialog, album_name_box, album_details_box):
            time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            name = album_name_box.toPlainText()
            details = album_details_box.toPlainText()
            cur_row = self.status_json.items["album_status"]["num_of_albums"]

            self.row_btns[cur_row][0].setObjectName("btn_album_name_" + time_stamp)
            print(self.row_btns[cur_row][0].objectName())
            self.row_btns[cur_row][0].setText(name)
            self.row_btns[cur_row][0].setStyleSheet(style.format(
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            ))

            self.row_btns[cur_row][1].setObjectName("btn_album_details_" + time_stamp)
            self.row_btns[cur_row][1].setText(details)
            self.row_btns[cur_row][1].setStyleSheet(style.format(
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            ))

            self.row_btns[cur_row][2].setObjectName("btn_bin_" + time_stamp)
            self.row_btns[cur_row][2].setText(f"相册“{name}”的回收站")
            self.row_btns[cur_row][2].setStyleSheet(style.format(
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            ))

            self.status_json.items["album_status"]["num_of_albums"] += 1

            album_dict = {
                "create_time": time_stamp,
                "name": name,
                "details": details,
                "bin": [],
                "image_paths": []
            }
            self.status_json.items["album_status"]["albums"].append(album_dict)
            self.status_json.serialize()

            dialog.close()

        def func_cancel(dialog):
            dialog.close()

        btn_check.clicked.connect(lambda: func_add_album(self, dialog, album_name_box, album_details_box))
        btn_cancel.clicked.connect(lambda: func_cancel(dialog))

        dialog.exec_()

    def func_about_bin_btn(self, btn_object: object):
        object_name = btn_object.objectName()

        print("in func_bin_btn:" + object_name)
        if object_name[-7:] == "unabled":
            return
        if object_name[:8] != "btn_bin_":
            return
        time_stamp = object_name[-14:]
        print("in func_bin_btn: pass")

        def get_name_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["name"]

        def get_pos_by_time(self, create_time: str):
            cnt = 0
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return cnt
                cnt += 1

        dialog = QDialog()
        # dialog.resize(800, 300)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setWindowTitle(f"相册 ”{get_name_by_time(self, time_stamp)}“ 的回收站")
        dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

        # 最大的是纵向布局 纵向布局最下方是添加照片和返回两个按钮 纵向布局上方是网格布局用于展示照片 且含有滚动条
        dialog_v_layout = QVBoxLayout(dialog)

        btn_restore_images_frame = QFrame()
        btn_restore_images_frame.setObjectName("btn_restore_images_frame")
        btn_restore_images_frame.setStyleSheet(u"background: transparent;")
        btn_restore_images_frame_layout = QHBoxLayout(btn_restore_images_frame)
        btn_restore_images_frame_layout.setAlignment(Qt.AlignCenter)

        btn_restore_images = PyPushButton(
            text="还原照片",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_restore_images.setMinimumWidth(200)
        btn_restore_images.setMaximumWidth(300)
        btn_restore_images.setMinimumHeight(70)
        btn_restore_images_frame_layout.addWidget(btn_restore_images)

        btn_back_frame = QFrame()
        btn_back_frame.setStyleSheet(u"background: transparent;")
        btn_back_frame_layout = QHBoxLayout(btn_back_frame)
        btn_back_frame_layout.setAlignment(Qt.AlignCenter)
        btn_back = PyPushButton(
            text="返回",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_back.setMinimumWidth(100)
        btn_back.setMaximumWidth(200)
        btn_back.setMinimumHeight(70)
        btn_back_frame_layout.addWidget(btn_back)

        btns_frame = QWidget()
        btns_frame.setStyleSheet(u"background: transparent;")
        btns_frame_layout = QHBoxLayout(btns_frame)
        btns_frame_layout.addWidget(btn_restore_images_frame)
        btns_frame_layout.addWidget(btn_back_frame)
        btns_frame_layout.setAlignment(Qt.AlignCenter)
        btns_frame_layout.addStretch()
        btns_frame_layout.setSpacing(50)

        scrollArea = QScrollArea(dialog)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        # scrollAreaWidgetContents.setGeometry()
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setMinimumWidth(900)
        scrollArea.setMinimumHeight(600)

        dialog_v_layout.addWidget(scrollArea, Qt.AlignCenter, Qt.AlignCenter)
        dialog_v_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

        image_grid_scroll_layout = QGridLayout(scrollAreaWidgetContents)
        image_grid_scroll_layout.setSpacing(10)

        col_num = 3  # 列数
        list_images = self.status_json.items["album_status"]["albums"][get_pos_by_time(self, time_stamp)][
            "image_paths"]  # 图片路径的列表
        list_bin_images = self.status_json.items["album_status"]["albums"][get_pos_by_time(self, time_stamp)][
            "bin"]  # 图片路径的列表
        bin_image_num = len(list_bin_images)
        row_num = ceil(bin_image_num / col_num)

        for i in range(row_num):
            for j in range(col_num):
                if i * col_num + j + 1 > bin_image_num:
                    break

                image_frame = QFrame()
                image_frame.setObjectName(u"image_frame")
                image_frame.setStyleSheet(u"background: transparent;")
                image_frame_layout = QVBoxLayout(image_frame)
                image_frame_layout.setAlignment(Qt.AlignCenter)

                image_label = QLabel()
                image_label.setPixmap(QPixmap(list_bin_images[i * col_num + j]))
                image_label.setMinimumWidth(200)
                image_label.setMaximumWidth(360)
                image_label.setMinimumHeight(200)
                image_label.setMaximumHeight(360)
                image_label.setAlignment(Qt.AlignCenter)

                name_label = QLabel()
                name_label.setObjectName(u"name_label")
                name_label.setStyleSheet(u"background: transparent;")
                name = os.path.split(list_bin_images[i * col_num + j])[1]
                name_label.setText(name if len(name) < 20 else name[-20:])
                name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                name_label.setAlignment(Qt.AlignCenter)

                image_frame_layout.addWidget(image_label)
                image_frame_layout.addWidget(name_label)

                image_grid_scroll_layout.addWidget(image_frame, i, j)

        def func_btn_restore_images(self, dialog):
            for image in list_bin_images:
                list_images.append(image)
            list_bin_images.clear()
            self.status_json.serialize()
            dialog.close()

        def func_btn_back(dialog):
            dialog.close()

        btn_restore_images.clicked.connect(partial(func_btn_restore_images, self, dialog))
        btn_back.clicked.connect(partial(func_btn_back, dialog))

        dialog.exec()

    def func_select_album(self):
        def get_name_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["name"]

        def get_details_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["details"]

        def get_pos_by_time(self, create_time: str):
            cnt = 0
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return cnt
                cnt += 1

        dialog = QDialog()
        # dialog.resize(800, 300)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setWindowTitle(u"选择相册")
        dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

        dialog_v_layout = QVBoxLayout(dialog)
        dialog_v_layout.setSpacing(20)
        dialog_v_layout.setAlignment(Qt.AlignCenter)
        dialog_v_layout.addStretch()
        dialog_v_layout.setContentsMargins(10, 20, 10, 0)

        label1 = QLabel()
        label1.setObjectName(u"name_label")
        label1.setStyleSheet(u"background: transparent;")
        label1.setText("请选择相册")
        label1.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
        label1.setAlignment(Qt.AlignCenter)

        dialog_v_layout.addWidget(label1)

        def func_select_album_check_btn(self, dialog, btn: object):
            time_stamp = btn.objectName()[-14:]
            pos = get_pos_by_time(self, time_stamp)
            global cur_album
            cur_album = time_stamp
            self.ui.load_pages.page2_label.setText("当前选中的相册：" + get_name_by_time(self, time_stamp))

            dialog.close()

        for row in range(self.status_json.items["album_status"]["num_of_albums"]):
            btn1_frame = QFrame()
            btn1_frame.setObjectName(u"btns_frame_row_%d" % (row + 1))
            btn1_frame.setStyleSheet(u"background: transparent;")
            btn1_frame_layout = QHBoxLayout(btn1_frame)

            btn1 = PyPushButton(
                text=self.status_json.items["album_status"]["albums"][row]["name"],
                radius=8,
                color=self.themes['app_color']['white'],
                bg_color=self.themes['app_color']['dark_one'],
                bg_color_hover=self.themes['app_color']['pink'],
                bg_color_pressed=self.themes['app_color']['pink']
            )

            btn1.setObjectName(self.status_json.items["album_status"]["albums"][row]["create_time"])
            btn1.setMaximumWidth(400)
            btn1.setMinimumWidth(180)
            btn1.setMinimumHeight(80)
            btn1_frame_layout.setSpacing(0)
            btn1_frame_layout.addStretch()
            btn1_frame_layout.addWidget(btn1)

            btn1.clicked.connect(partial(func_select_album_check_btn, self, dialog, btn1))

            dialog_v_layout.addWidget(btn1_frame)

        dialog.exec()

    def func_classify_human(self):
        global cur_album
        time_stamp = cur_album

        def get_name_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["name"]

        def get_details_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["details"]

        def get_pos_by_time(self, create_time: str):
            cnt = 0
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return cnt
                cnt += 1

        if get_pos_by_time(self, time_stamp) is None:
            return

        dialog = QDialog()
        # dialog.resize(800, 300)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setWindowTitle(f"相册 ”{get_name_by_time(self, time_stamp)}“ 的分类结果")
        dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

        # 最大的是纵向布局 纵向布局最下方是添加照片和返回两个按钮 纵向布局上方是网格布局用于展示照片 且含有滚动条
        dialog_v_layout = QVBoxLayout(dialog)

        btn_save_result_frame = QFrame()
        btn_save_result_frame.setObjectName("btn_save_result_frame")
        btn_save_result_frame.setStyleSheet(u"background: transparent;")
        btn_save_result_frame_layout = QHBoxLayout(btn_save_result_frame)
        btn_save_result_frame_layout.setAlignment(Qt.AlignCenter)

        btn_save_result = PyPushButton(
            text="保存分类结果",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_save_result.setMinimumWidth(200)
        btn_save_result.setMaximumWidth(300)
        btn_save_result.setMinimumHeight(70)
        btn_save_result_frame_layout.addWidget(btn_save_result)

        btn_back_frame = QFrame()
        btn_back_frame.setStyleSheet(u"background: transparent;")
        btn_back_frame_layout = QHBoxLayout(btn_back_frame)
        btn_back_frame_layout.setAlignment(Qt.AlignCenter)
        btn_back = PyPushButton(
            text="返回",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_back.setMinimumWidth(100)
        btn_back.setMaximumWidth(200)
        btn_back.setMinimumHeight(70)
        btn_back_frame_layout.addWidget(btn_back)

        btns_frame = QWidget()
        btns_frame.setStyleSheet(u"background: transparent;")
        btns_frame_layout = QHBoxLayout(btns_frame)
        btns_frame_layout.addWidget(btn_save_result_frame)
        btns_frame_layout.addWidget(btn_back_frame)
        btns_frame_layout.setAlignment(Qt.AlignCenter)
        btns_frame_layout.addStretch()
        btns_frame_layout.setSpacing(50)

        scrollArea = QScrollArea(dialog)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        # scrollAreaWidgetContents.setGeometry()
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setMinimumWidth(1200)
        scrollArea.setMinimumHeight(800)

        dialog_v_layout.addWidget(scrollArea, Qt.AlignCenter, Qt.AlignCenter)
        dialog_v_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

        image_grid_scroll_layout = QGridLayout(scrollAreaWidgetContents)
        image_grid_scroll_layout.setSpacing(10)

        searching_label = QLabel()
        searching_label.setObjectName(u"searching_label")
        searching_label.setStyleSheet(u"background: transparent;")
        searching_label.setText("识别中……")
        searching_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 24pt;color:white")
        searching_label.setAlignment(Qt.AlignCenter)

        image_grid_scroll_layout.addWidget(searching_label)

        dialog.show()

        list_images = self.status_json.items["album_status"]["albums"][get_pos_by_time(self, time_stamp)][
            "image_paths"]  # 图片路径的列表

        images_code = []
        for index, image_path in enumerate(list_images):
            if self.status_json.items["face_code"].get(image_path) is None:
                face_code = face_encodings(load_image_file(image_path))
                if len(face_code) > 0:
                    face_code = face_code[0]
                    self.status_json.items["face_code"][image_path] = face_code.tolist()
                    images_code.append(face_code)
                else:
                    images_code.append([0 for i in range(128)])
            else:
                images_code.append(self.status_json.items["face_code"].get(image_path))
        self.status_json.serialize()

        same_people = []  # 每个元素都是一个列表 里面是一个人的图片的编号
        all_same_people = []  # A flag
        for i, code in enumerate(images_code):
            if i in all_same_people:
                continue
            if len(images_code) - i <= 2:
                continue
            new_images_code = images_code[i + 1:]
            result_01 = compare_faces(numpy.array(new_images_code), numpy.array(code), tolerance=0.58)
            same_people_to_i = [i]
            for j, result_0_or_1 in enumerate(result_01):
                if result_0_or_1:
                    same_people_to_i.append(i + j + 1)
                    all_same_people.append(i + j + 1)
            same_people.append(same_people_to_i)

        row_num = len(same_people)
        if row_num == 0:
            searching_label.setText("无照片 请添加照片后重试")
        else:
            for i in range(image_grid_scroll_layout.count()):
                image_grid_scroll_layout.itemAt(i).widget().deleteLater()
        for row in range(row_num):
            col_num = len(same_people[row])

            label_first = QLabel()
            label_first.setObjectName(u"name_label")
            label_first.setStyleSheet(u"background: transparent;")
            label_first.setText("人物 {}".format(row + 1))
            label_first.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
            label_first.setAlignment(Qt.AlignCenter)
            image_grid_scroll_layout.addWidget(label_first, row, 0)
            for col in range(col_num):
                image_frame = QFrame()
                image_frame.setObjectName(u"image_frame")
                image_frame.setStyleSheet(u"background: transparent;")
                image_frame_layout = QVBoxLayout(image_frame)
                image_frame_layout.setAlignment(Qt.AlignCenter)

                image_label = QLabel()
                image_label.setPixmap(QPixmap(list_images[same_people[row][col]]))
                image_label.setMinimumWidth(200)
                image_label.setMaximumWidth(360)
                image_label.setMinimumHeight(200)
                image_label.setMaximumHeight(360)
                image_label.setAlignment(Qt.AlignCenter)

                name_label = QLabel()
                name_label.setObjectName(u"name_label")
                name_label.setStyleSheet(u"background: transparent;")
                name = os.path.split(list_images[same_people[row][col]])[1]
                name_label.setText(name if len(name) < 20 else name[-20:])
                name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                name_label.setAlignment(Qt.AlignCenter)

                image_frame_layout.addWidget(image_label)
                image_frame_layout.addWidget(name_label)

                image_grid_scroll_layout.addWidget(image_frame, row, col + 1)

        def func_btn_save_result(self, dialog):
            album_name = get_name_by_time(self, time_stamp)
            setting = Settings()
            path = setting.items["app_path"] + "\\" + album_name + "\\result\\human\\"
            for row in range(row_num):
                col_num = len(same_people[row])
                dir_name = "人物 {}".format(row + 1)
                if not os.path.exists(path + dir_name):
                    os.makedirs(path + dir_name)
                for col in range(col_num):
                    shutil.copy2(list_images[same_people[row][col]], path + dir_name)
            dialog.close()

        def func_btn_back(dialog):
            dialog.close()

        btn_save_result.clicked.connect(partial(func_btn_save_result, self, dialog))
        btn_back.clicked.connect(partial(func_btn_back, dialog))

        dialog.exec()

    def func_classify_object(self):
        global cur_album
        time_stamp = cur_album

        def get_name_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["name"]

        def get_details_by_time(self, create_time: str):
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return album["details"]

        def get_pos_by_time(self, create_time: str):
            cnt = 0
            for album in self.status_json.items["album_status"]["albums"]:
                if album["create_time"] == create_time:
                    return cnt
                cnt += 1

        if get_pos_by_time(self, time_stamp) is None:
            return

        dialog = QDialog()
        # dialog.resize(800, 300)
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setWindowTitle(f"相册 ”{get_name_by_time(self, time_stamp)}“ 的分类结果")
        dialog.setStyleSheet(u"background: {0};font-size: 18pt".format(self.themes["app_color"]["bg_one"]))

        # 最大的是纵向布局 纵向布局最下方是添加照片和返回两个按钮 纵向布局上方是网格布局用于展示照片 且含有滚动条
        dialog_v_layout = QVBoxLayout(dialog)

        btn_save_result_frame = QFrame()
        btn_save_result_frame.setObjectName("btn_save_result_frame")
        btn_save_result_frame.setStyleSheet(u"background: transparent;")
        btn_save_result_frame_layout = QHBoxLayout(btn_save_result_frame)
        btn_save_result_frame_layout.setAlignment(Qt.AlignCenter)

        btn_save_result = PyPushButton(
            text="保存分类结果",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_save_result.setMinimumWidth(200)
        btn_save_result.setMaximumWidth(300)
        btn_save_result.setMinimumHeight(70)
        btn_save_result_frame_layout.addWidget(btn_save_result)

        btn_back_frame = QFrame()
        btn_back_frame.setStyleSheet(u"background: transparent;")
        btn_back_frame_layout = QHBoxLayout(btn_back_frame)
        btn_back_frame_layout.setAlignment(Qt.AlignCenter)
        btn_back = PyPushButton(
            text="返回",
            radius=8,
            color=self.themes['app_color']['white'],
            bg_color=self.themes['app_color']['dark_one'],
            bg_color_hover=self.themes['app_color']['pink'],
            bg_color_pressed=self.themes['app_color']['pink']
        )
        btn_back.setMinimumWidth(100)
        btn_back.setMaximumWidth(200)
        btn_back.setMinimumHeight(70)
        btn_back_frame_layout.addWidget(btn_back)

        btns_frame = QWidget()
        btns_frame.setStyleSheet(u"background: transparent;")
        btns_frame_layout = QHBoxLayout(btns_frame)
        btns_frame_layout.addWidget(btn_save_result_frame)
        btns_frame_layout.addWidget(btn_back_frame)
        btns_frame_layout.setAlignment(Qt.AlignCenter)
        btns_frame_layout.addStretch()
        btns_frame_layout.setSpacing(50)

        scrollArea = QScrollArea(dialog)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget(scrollArea)
        # scrollAreaWidgetContents.setGeometry()
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setMinimumWidth(1200)
        scrollArea.setMinimumHeight(800)

        dialog_v_layout.addWidget(scrollArea, Qt.AlignCenter, Qt.AlignCenter)
        dialog_v_layout.addWidget(btns_frame, Qt.AlignCenter, Qt.AlignCenter)

        image_grid_scroll_layout = QGridLayout(scrollAreaWidgetContents)
        image_grid_scroll_layout.setSpacing(10)

        searching_label = QLabel()
        searching_label.setObjectName(u"searching_label")
        searching_label.setStyleSheet(u"background: transparent;")
        searching_label.setText("识别中……")
        searching_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 24pt;color:white")
        searching_label.setAlignment(Qt.AlignCenter)

        image_grid_scroll_layout.addWidget(searching_label)

        dialog.open()

        list_images = self.status_json.items["album_status"]["albums"][get_pos_by_time(self, time_stamp)][
            "image_paths"]  # 图片路径的列表

        if len(list_images) > 0:
            for i in range(image_grid_scroll_layout.count()):
                image_grid_scroll_layout.itemAt(i).widget().deleteLater()
        else:
            searching_label.setText("无照片 请添加照片后重试")

        result_dict = {"dog": [], "horse": [], "elephant": [], "butterfly": [], "chicken": [], "cat": [], "cow": [],
                       "sheep": [], "spider": [], "squirrel": [], "human": []}
        for i, image_path in enumerate(list_images):
            if self.status_json.items["aniobj_result"].get(image_path) is None:
                result = func_aniobj.out(image_path)
                result_dict[result].append(i)
                self.status_json.items["aniobj_result"][image_path] = result
            else:
                result_dict[self.status_json.items["aniobj_result"][image_path]].append(i)
        self.status_json.serialize()

        row = 0
        for name in func_aniobj.translate:
            col_num = len(result_dict[name])
            if col_num == 0:
                continue

            label_first = QLabel()
            label_first.setObjectName(u"name_label")
            label_first.setStyleSheet(u"background: transparent;")
            label_first.setText(name)
            label_first.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
            label_first.setAlignment(Qt.AlignCenter)
            image_grid_scroll_layout.addWidget(label_first, row, 0)
            for col in range(col_num):
                image_frame = QFrame()
                image_frame.setObjectName(u"image_frame")
                image_frame.setStyleSheet(u"background: transparent;")
                image_frame_layout = QVBoxLayout(image_frame)
                image_frame_layout.setAlignment(Qt.AlignCenter)

                image_label = QLabel()
                image_label.setPixmap(QPixmap(list_images[result_dict[name][col]]))
                image_label.setMinimumWidth(200)
                image_label.setMaximumWidth(360)
                image_label.setMinimumHeight(200)
                image_label.setMaximumHeight(360)
                image_label.setAlignment(Qt.AlignCenter)

                name_label = QLabel()
                name_label.setObjectName(u"name_label")
                name_label.setStyleSheet(u"background: transparent;")
                name1 = os.path.split(list_images[result_dict[name][col]])[1]
                name_label.setText(name1 if len(name1) < 20 else name1[-20:])
                name_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt;color:white")
                name_label.setAlignment(Qt.AlignCenter)

                image_frame_layout.addWidget(image_label)
                image_frame_layout.addWidget(name_label)

                image_grid_scroll_layout.addWidget(image_frame, row, col + 1)

            row += 1

        def func_btn_save_result(self, dialog):
            album_name = get_name_by_time(self, time_stamp)
            setting = Settings()
            path = setting.items["app_path"] + "\\" + album_name + "\\result\\"
            for name in func_aniobj.translate:

                col_num = len(result_dict[name])
                if col_num > 0 and not os.path.exists(path + name):
                    os.makedirs(path + name)

                for col in range(col_num):
                    shutil.copy2(list_images[result_dict[name][col]], path + name)
            dialog.close()

        def func_btn_back(dialog):
            dialog.close()

        btn_save_result.clicked.connect(partial(func_btn_save_result, self, dialog))
        btn_back.clicked.connect(partial(func_btn_back, dialog))
        dialog.exec()

    # SET MAIN WINDOW PAGES
    # ///////////////////////////////////////////////////////////////
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)

    # SET LEFT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_left_column_menu(
            self,
            menu,
            title,
            icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.title_label.setAlignment(Qt.AlignCenter)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)

    # LEDT AND RIGHT COLUMNS / SHOW / HIDE
    # ///////////////////////////////////////////////////////////////
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values        
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values        
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right

            # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def load_main_credit_bar(self):
        self.ui.credits.copyright_label.setText(self.settings["copyright"])
        self.ui.credits.person.setText("")
        self.ui.credits.person_name.setText("")
        self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
        self.ui.credits.person_name.setReadOnly(True)
        self.ui.credits.image.setText("")
        self.ui.credits.image_title.setText("")
        self.ui.credits.update()

    def get_checked_button(self, image_page):
        btn = image_page.button_box.checkedButton()
        print("{} Checked".format(btn.objectName()))
        self.ui.credits.image_title.setText(btn.objectName())

    def select_image_directory(self):
        directory = QFileDialog.getExistingDirectory(None, "C:/")
        if directory == '':
            print("No folder selected")
            return None
        self.ui.credits.copyright_label.setText("选择文件夹：{}".format(directory))
        return directory


class Obj(object):
    def __init__(self):
        self._translate = ["dog", "horse", "elephant", "butterfly", "chicken", "cat", "cow", "sheep", "spider",
                           "squirrel", "human"]
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self._net = models.resnet34(pretrained=False)
        fc_inputs = self._net.fc.in_features
        self._net.fc = torch.nn.Sequential(
            torch.nn.Linear(fc_inputs, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.4),
            torch.nn.Linear(256, 11),
            torch.nn.LogSoftmax(dim=1)
        )
        self._net.load_state_dict(torch.load("resources/AniObjClass.pkl"))
        torch.no_grad()
        self._net = self._net.to(self._device)
        self._net.eval()

    def outcome(self, image):  # 这个最重要
        t_img = load_image_file(image)
        t_img = cv2.resize(t_img, (224, 336))
        t_img = transform(t_img)
        t_img = t_img.unsqueeze(0)
        t_img = t_img.to(self._device)
        outputs = self._net(t_img)

        predicted, index = torch.max(outputs, 1)  # torch.max(tensorA,dim):dim表示指定的维度,返回指定维度的最大数和对应下标
        degree = int(index[0])
        return self._translate[degree]
