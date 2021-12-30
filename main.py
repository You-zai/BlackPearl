# ///////////////////////////////////////////////////////////////
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
import json

from gui.uis.windows.main_window.functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.core.qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"


# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items
        self.settings["app_path"] = os.getcwd()
        settings.serialize()
        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True  # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)
        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        print(btn.objectName())
        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        # 我的相册
        if btn.objectName() == 'btn_my_album':
            self.ui.left_menu.select_only_one(btn.objectName())
            if MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
            MainFunctions.load_main_credit_bar(self)
            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_my_album)

        # 基本功能
        if btn.objectName() == 'btn_basic_function':
            self.ui.left_menu.select_only_one(btn.objectName())
            if MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
            MainFunctions.load_main_credit_bar(self)
            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_basic_function)

        if btn.objectName() == 'btn_dust_bin':
            self.ui.left_menu.select_only_one(btn.objectName())
            if MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
            MainFunctions.load_main_credit_bar(self)
            # Load Page
            MainFunctions.set_page(self, self.ui.load_pages.page_dust_bin)

        if btn.objectName() == 'btn_extended_functions':
            self.ui.left_menu.select_only_one(btn.objectName())
            if MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
            MainFunctions.set_page(self, self.ui.load_pages.page_settings)
            # MainFunctions.load_duplicate_result(self)

        # OPEN Settings
        if btn.objectName() == 'btn_settings' or btn.objectName() == 'btn_close_left_column':
            if not MainFunctions.left_column_is_visible(self):
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                self.ui.left_menu.deselect_all_tab()
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(btn.objectName)

        '''
        '''
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////

        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                # MainFunctions.toggle_left_column(self)
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn            
            top_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            top_settings.set_active_tab(False)

        else:
            pass
        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

    def closeEvent(self, event):
        print("Detected")
        self.close()
        print("Closed")


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == '__main__':
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication()
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    app.exec()
