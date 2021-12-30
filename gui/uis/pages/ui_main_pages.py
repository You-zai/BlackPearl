from gui.core.qt_core import *


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        # MainPages.resize(860, 600)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")

        self.page_my_album = QWidget()
        self.page_my_album.setObjectName(u"page_my_album")
        self.page_my_album.setStyleSheet(u"font-size: 14pt")
        self.pages.addWidget(self.page_my_album)

        # 总布局
        self.page_my_album_grid_layout = QGridLayout()
        self.page_my_album_grid_layout.setSpacing(10)
        self.page_my_album_grid_layout.setObjectName(u"page_my_album_grid_layout")
        self.page_my_album.setLayout(self.page_my_album_grid_layout)
        self.page_my_album_grid_layout.setContentsMargins(10, 10, 10, 10)

        self.left_lable = QLabel()
        self.left_lable.setObjectName(u"left_lable")
        self.left_lable.setStyleSheet(u"background: transparent;")
        self.left_lable.setText("我的相册")
        self.left_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.left_lable.setAlignment(Qt.AlignCenter)

        self.left_btn_frame = QFrame()
        self.left_btn_frame.setObjectName(u"func_2_frame_2")
        self.left_btn_frame.setStyleSheet(u"background: transparent;")
        self.left_btn_frame_layout = QHBoxLayout(self.left_btn_frame)
        self.left_btn_frame_layout.addWidget(self.left_lable)
        self.left_btn_frame_layout.setAlignment(Qt.AlignCenter)
        self.left_btn_frame_layout.setSpacing(20)
        self.page_my_album_grid_layout.addWidget(self.left_btn_frame, 0, 0)

        self.right_lable = QLabel()
        self.right_lable.setObjectName(u"right_lable")
        self.right_lable.setStyleSheet(u"background: transparent;")
        self.right_lable.setText("详细信息")
        self.right_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.right_lable.setAlignment(Qt.AlignCenter)
        self.page_my_album_grid_layout.addWidget(self.right_lable, 0, 1)

        self.page_my_album_grid_layout.setHorizontalSpacing(50)
        self.page_my_album_grid_layout.setVerticalSpacing(10)

        # 添加滚动条
        self.scroll_page_my_album = QScrollArea(self.page_my_album)
        self.scroll_page_my_album.setContentsMargins(1, 1, 1, 1)
        self.scroll_page_my_album.setObjectName(u"scroll_page_my_album")
        self.scroll_page_my_album.setStyleSheet(u"background: transparent;")
        self.scroll_page_my_album.setFrameShape(QFrame.NoFrame)
        self.scroll_page_my_album.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_page_my_album.setWidgetResizable(True)
        self.scroll_page_my_album_contents = QWidget(self.scroll_page_my_album)
        self.scroll_page_my_album_contents.setObjectName(u"scroll_page_my_album_contents")
        self.scroll_page_my_album_contents.setStyleSheet(u"background: transparent;")
        self.scroll_page_my_album.setWidget(self.scroll_page_my_album_contents)

        # self.page_my_album_grid_layout.addWidget(self.scroll_page_my_album)

        # self.verticalLayoutScroll = QVBoxLayout()
        # self.page_my_album.setLayout(self.verticalLayoutScroll)
        # self.verticalLayoutScroll.addWidget(self.page_my_album)
        # self.verticalLayoutScroll.addWidget(self.left_column)
        # self.verticalLayoutScroll.addWidget(self.right_column)
        # 第一页 我的相册 配置完毕

        self.page_basic_function = QWidget()
        self.page_basic_function.setObjectName(u"page_basic_function")
        self.page_basic_function.setStyleSheet(u"font-size: 14pt")
        self.pages.addWidget(self.page_basic_function)

        self.page2_v_layout = QVBoxLayout()
        self.page_basic_function.setLayout(self.page2_v_layout)
        self.page2_v_layout.setAlignment(Qt.AlignTop)
        self.page2_v_layout.setContentsMargins(0, 0, 0, 0)
        self.page2_v_layout.setSpacing(50)
        self.page2_v_layout.setObjectName(u"page2_v_layout")

        self.page2_up_lb = QFrame()
        self.page2_up_lb.setObjectName(u"page2_up_lb")
        self.page2_up_lb.setStyleSheet(u"font-s ize: 14pt")
        self.page2_up_lb_layout = QHBoxLayout(self.page2_up_lb)
        self.page2_up_lb_layout.setAlignment(Qt.AlignLeft)
        # self.page2_up_lb.setLayout(self.page2_up_lb_layout)

        self.page2_btn_frame = QFrame()
        self.page2_btn_frame.setObjectName(u"page2_btn_frame")
        self.page2_btn_frame.setStyleSheet(u"background: transparent;")
        self.page2_btn_frame_layout = QHBoxLayout()
        self.page2_btn_frame.setLayout(self.page2_btn_frame_layout)
        self.page2_up_lb_layout.addWidget(self.page2_btn_frame)
        self.page2_up_lb_layout.setSpacing(30)
        self.page2_up_lb_layout.setContentsMargins(30,10,0,30)

        self.page2_label = QLabel()
        self.page2_label.setObjectName(u"page2_label")
        self.page2_label.setStyleSheet(u"background: transparent;")
        self.page2_label.setText("当前选中的相册：无")
        self.page2_label.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.page2_label.setAlignment(Qt.AlignCenter)
        self.page2_up_lb_layout.addWidget(self.page2_label)

        self.page2_v_layout.addWidget(self.page2_up_lb)

        self.page2_btns = QWidget()
        self.page2_btns.setObjectName(u"page2_btns")
        self.page2_btns.setStyleSheet(u"background: transparent;")
        self.page2_h_layout = QHBoxLayout()
        self.page2_btns.setLayout(self.page2_h_layout)
        self.page2_h_layout.setAlignment(Qt.AlignCenter)
        self.page2_h_layout.setSpacing(150)
        self.page2_v_layout.addWidget(self.page2_btns)

        self.page_dust_bin = QWidget()
        self.page_dust_bin.setObjectName(u"page_dust_bin")
        self.page_dust_bin.setStyleSheet(u"font-size: 14pt")
        self.pages.addWidget(self.page_dust_bin)

        # 回收站布局
        self.page_dust_bin_grid_layout = QGridLayout()
        self.page_dust_bin_grid_layout.setSpacing(10)
        self.page_dust_bin_grid_layout.setObjectName(u"page_my_album_grid_layout")
        self.page_dust_bin.setLayout(self.page_dust_bin_grid_layout)
        # self.page_dust_bin_grid_layout.setContentsMargins(10, 10, 10, 10)
        self.page_dust_bin_grid_layout.setAlignment(Qt.AlignTop)

        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.page_settings.setStyleSheet(u"font-size: 14pt")
        self.pages.addWidget(self.page_settings)

        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainPages)

    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
    # retranslateUi
