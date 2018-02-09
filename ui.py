# -*- coding: utf-8 -*-
# Created: 05.01.18
# Changed: 09.02.18

import source

from pathlib import Path
from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QMenu, QAction, QSizePolicy, QHBoxLayout, QVBoxLayout, QMenu,\
    QMenuBar, QHeaderView, QAbstractItemView, QLineEdit, QGraphicsDropShadowEffect, QTextEdit
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize


class RootUI:

    def __init__(self, root, table):
        self.root = root
        """ Widgets """
        self.left_widget = QWidget()
        self.right_widget = QWidget()
        self.tool_terminal = QToolButton()
        self.tool_rights = QToolButton()
        self.lmenu = QMenu(self.root)
        self.rmenu = QMenu(self.root)
        self.ltl_dir = QLabel()
        self.ltl_path = QLabel()
        self.ltl_bookmark = QToolButton()
        self.rtl_dir = QLabel()
        self.rtl_path = QLabel()
        self.rtl_bookmark = QToolButton()
        self.lbl_dir = QLabel()
        self.lbl_2 = QLabel()
        self.lbl_file = QLabel()
        self.lbl_4 = QLabel()
        self.lbl_selection = QLabel()
        self.lbl_disk = QLabel()
        self.lbl_disk_num = QLabel()
        self.rbl_dir = QLabel()
        self.rbl_2 = QLabel()
        self.rbl_file = QLabel()
        self.rbl_4 = QLabel()
        self.rbl_selection = QLabel()
        self.rbl_disk = QLabel()
        self.rbl_disk_num = QLabel()
        """ Left & Right Panels """
        self.leftPanel = table(Path('/'), (self.ltl_path, self.lbl_2, self.lbl_4, self.lbl_selection, self.lbl_disk_num))
        self.rightPanel = table(Path.home(), (self.rtl_path, self.rbl_2, self.rbl_4, self.rbl_selection, self.rbl_disk_num))
        """ Layouts """
        self.top_left_layout = QHBoxLayout()
        self.top_right_layout = QHBoxLayout()
        self.bottom_left_layout = QHBoxLayout()
        self.bottom_right_layout = QHBoxLayout()
        self.panelleftlayout = QVBoxLayout()
        self.panelrightlayout = QVBoxLayout()
        self.tool_barlayout = QHBoxLayout()
        self.tablelayout = QHBoxLayout()
        """ Panel Sync """
        self.sync_panel = {self.leftPanel: self.rightPanel, self.rightPanel: self.leftPanel}
        """ Configure Widget elements """
        self.root.setStyleSheet('''
            QWidget#__widget {border: 1px solid #c8c8c8; border-radius: 2px;}
            QToolButton#__tool {border: none; font: 11px Arial; color: #4e4e4e; margin: 5px 0 0 5px;}
            QToolButton#__tool:hover, QToolButton#__tool:focus {color: #000000;}
            QToolButton#__tool:hover {border: 1px solid #c5c5c5;}
            QToolButton#__tool::menu-indicator {image: none;}
            QToolButton#__bookmark {border: none;}
            QToolButton#__bookmark::menu-indicator {image: none;}
            QMenu {border: 1px solid #b8b8b8; font: 12px Arial; margin: 0; background: #eaeaea;}
            QMenu::item {padding: 9px 30px; color: #5a5a5a;}
            QMenu::item:selected {color: #ffffff; background: #297fb8;}
            QMenu::separator {height: 1px; margin: 0; background: #b8b8b8;}
            QLabel#__pixmap, QLabel#__folder {padding-left: 4px;}
            QLabel#__path {font: 12px Verdana; color: #808080; padding-left: 2px;}
            QLabel#__digits {font: 12px Arial; color: #6d6d6d; padding-left: 2px;}
            QLabel#__selection {font: 10px Arial; color: #838383;}
            QLabel#__disknum {font: 11px Arial; color: #808080; padding-left: 4px;}
        ''')

        for _widg in (self.left_widget, self.right_widget):
            _widg.setObjectName("__widget")
        self.tool_terminal.setIcon(QIcon(":/terminal"))
        self.tool_rights.setIcon(QIcon(":/rights"))
        for tool in (self.tool_terminal, self.tool_rights):
            tool.setObjectName('__tool')
            tool.setMinimumSize(35, 35)
            tool.setCursor(Qt.PointingHandCursor)
        """ Bookmark menu """
        self.lmenu.setCursor(Qt.PointingHandCursor)
        laction_1 = QAction("Filesystem", self.root, triggered=lambda: self.leftPanel.bookmark("/"))
        laction_2 = QAction("Home", self.root, triggered=lambda: self.leftPanel.bookmark("/home/udmin/"))
        laction_3 = QAction("Downloads", self.root, triggered=lambda: self.leftPanel.bookmark("/home/udmin/Загрузки/"))
        laction_4 = QAction("Mount", self.root, triggered=lambda: self.leftPanel.bookmark("/media/"))
        laction_5 = QAction("Project", self.root,
                            triggered=lambda: self.leftPanel.bookmark("/home/udmin/Soft/linux/python/app/"))
        self.lmenu.addAction(laction_1)
        self.lmenu.addAction(laction_2)
        self.lmenu.addAction(laction_3)
        self.lmenu.addSeparator()
        self.lmenu.addAction(laction_4)
        self.lmenu.addSeparator()
        self.lmenu.addAction(laction_5)
        self.rmenu.setCursor(Qt.PointingHandCursor)
        raction_1 = QAction("Filesystem", self.root, triggered=lambda: self.rightPanel.bookmark("/"))
        raction_2 = QAction("Home", self.root, triggered=lambda: self.rightPanel.bookmark("/home/udmin/"))
        raction_3 = QAction("Downloads", self.root, triggered=lambda: self.rightPanel.bookmark("/home/udmin/Загрузки/"))
        raction_4 = QAction("Mount", self.root, triggered=lambda: self.rightPanel.bookmark("/media/"))
        raction_5 = QAction("Project", self.root,
                            triggered=lambda: self.rightPanel.bookmark("/home/udmin/Soft/linux/python/app/"))
        self.rmenu.addAction(raction_1)
        self.rmenu.addAction(raction_2)
        self.rmenu.addAction(raction_3)
        self.rmenu.addSeparator()
        self.rmenu.addAction(raction_4)
        self.rmenu.addSeparator()
        self.rmenu.addAction(raction_5)
        """ Верхняя левая адресная панель: Каталог, Путь, Закладки """
        self.ltl_dir.setObjectName("__pixmap")
        self.ltl_dir.setPixmap(QPixmap(":/dir").scaled(QSize(20, 20)))
        self.ltl_dir.setFixedSize(24, 24)
        self.ltl_path.setObjectName("__path")
        self.ltl_path.setAlignment(Qt.AlignTop)
        self.ltl_bookmark.setObjectName("__bookmark")
        self.ltl_bookmark.setFixedSize(14, 14)
        self.ltl_bookmark.setCursor(Qt.PointingHandCursor)
        self.ltl_bookmark.setIcon(QIcon(QPixmap(":/bookmark")))
        self.ltl_bookmark.setPopupMode(QToolButton.InstantPopup)
        self.ltl_bookmark.setMenu(self.lmenu)
        """ Верхняя правая адресная панель: Каталог, Путь, Закладки """
        self.rtl_dir.setObjectName("__pixmap")
        self.rtl_dir.setPixmap(QPixmap(":/dir").scaled(QSize(20, 20)))
        self.rtl_dir.setFixedSize(24, 24)
        self.rtl_path.setObjectName("__path")
        self.rtl_path.setAlignment(Qt.AlignTop)
        self.rtl_bookmark.setObjectName("__bookmark")
        self.rtl_bookmark.setFixedSize(14, 14)
        self.rtl_bookmark.setCursor(Qt.PointingHandCursor)
        self.rtl_bookmark.setIcon(QIcon(QPixmap(":/bookmark")))
        self.rtl_bookmark.setPopupMode(QToolButton.InstantPopup)
        self.rtl_bookmark.setMenu(self.rmenu)
        """ Tables """
        self.leftPanel.setObjectName("__leftPanel")
        self.rightPanel.setObjectName("__rightPanel")
        """ Нижняя левая панель: Каталог, Файл, Диск """
        self.lbl_dir.setObjectName("__folder")
        self.lbl_dir.setPixmap(QPixmap(":/folder"))
        self.lbl_dir.setMinimumSize(20, 20)
        self.lbl_2.setObjectName("__digits")
        self.lbl_2.setMinimumWidth(35)
        self.lbl_file.setPixmap(QPixmap(":/file"))
        self.lbl_4.setObjectName("__digits")
        self.lbl_selection.setObjectName("__selection")
        self.lbl_selection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.lbl_selection.setAlignment(Qt.AlignCenter)
        self.lbl_disk.setPixmap(QPixmap(":/disk"))
        self.lbl_disk_num.setObjectName("__disknum")
        """ Нижняя правая панель: Каталог, Файл, Диск """
        self.rbl_dir.setObjectName("__folder")
        self.rbl_dir.setPixmap(QPixmap(":/folder"))
        self.rbl_dir.setMinimumSize(20, 20)
        self.rbl_2.setObjectName("__digits")
        self.rbl_2.setMinimumWidth(35)
        self.rbl_file.setPixmap(QPixmap(":/file"))
        self.rbl_4.setObjectName("__digits")
        self.rbl_selection.setObjectName("__selection")
        self.rbl_selection.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.rbl_selection.setAlignment(Qt.AlignCenter)
        self.rbl_disk.setPixmap(QPixmap(":/disk"))
        self.rbl_disk_num.setObjectName("__disknum")
        """ Box Layouts """
        self.top_left_layout.addWidget(self.ltl_dir)
        self.top_left_layout.addWidget(self.ltl_path)
        self.top_left_layout.addWidget(self.ltl_bookmark)
        self.top_left_layout.setContentsMargins(1, 1, 1, 2)
        self.top_right_layout.addWidget(self.rtl_dir)
        self.top_right_layout.addWidget(self.rtl_path)
        self.top_right_layout.addWidget(self.rtl_bookmark)
        self.top_right_layout.setContentsMargins(1, 1, 1, 2)
        self.bottom_left_layout.addWidget(self.lbl_dir)
        self.bottom_left_layout.addWidget(self.lbl_2)
        self.bottom_left_layout.addWidget(self.lbl_file)
        self.bottom_left_layout.addWidget(self.lbl_4)
        self.bottom_left_layout.addWidget(self.lbl_selection)
        self.bottom_left_layout.addWidget(self.lbl_disk)
        self.bottom_left_layout.addWidget(self.lbl_disk_num)
        self.bottom_left_layout.setContentsMargins(0, 2, 0, 0)
        self.bottom_right_layout.addWidget(self.rbl_dir)
        self.bottom_right_layout.addWidget(self.rbl_2)
        self.bottom_right_layout.addWidget(self.rbl_file)
        self.bottom_right_layout.addWidget(self.rbl_4)
        self.bottom_right_layout.addWidget(self.rbl_selection)
        self.bottom_right_layout.addWidget(self.rbl_disk)
        self.bottom_right_layout.addWidget(self.rbl_disk_num)
        self.bottom_right_layout.setContentsMargins(0, 2, 0, 0)

        self.panelleftlayout.addLayout(self.top_left_layout)
        self.panelleftlayout.addWidget(self.leftPanel)
        self.panelleftlayout.addLayout(self.bottom_left_layout)
        self.panelleftlayout.setContentsMargins(5, 5, 5, 5)
        self.panelleftlayout.setSpacing(1)
        self.panelrightlayout.addLayout(self.top_right_layout)
        self.panelrightlayout.addWidget(self.rightPanel)
        self.panelrightlayout.addLayout(self.bottom_right_layout)
        self.panelrightlayout.setContentsMargins(5, 5, 5, 5)
        self.panelrightlayout.setSpacing(1)

        self.left_widget.setLayout(self.panelleftlayout)
        self.right_widget.setLayout(self.panelrightlayout)

        self.tool_barlayout.addWidget(self.tool_terminal)
        self.tool_barlayout.addWidget(self.tool_rights)
        self.tool_barlayout.addStretch(1)
        self.tool_barlayout.setContentsMargins(0, 0, 0, 0)
        self.tool_barlayout.setSpacing(0)

        self.tablelayout.addWidget(self.left_widget)
        self.tablelayout.addWidget(self.right_widget)
        self.tablelayout.setContentsMargins(3, 3, 3, 3)
        self.tablelayout.setSpacing(3)

        mainlayout = QVBoxLayout(self.root)
        mainlayout.addLayout(self.tool_barlayout)
        mainlayout.addLayout(self.tablelayout)
        mainlayout.setContentsMargins(2, 2, 2, 2)
        mainlayout.setSpacing(0)

        self.root.setLayout(mainlayout)


class TableWidget:

    def __init__(self, table):
        """ QTableWidget """
        table.setStyleSheet('''
            QTableWidget::item:!enabled {border-left: 1px solid #e3e3e3;}
            QTableWidget::item:!enabled:selected {border-left: 1px solid #e3e3e3;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ececec, stop: 1.0 #dedede); color:#808080;}
            QTableWidget::item:!enabled:selected:active {background: #f17a4c; color: #fff; border-left:#f17a4c;}
            QTableWidget:focus {border: 1px solid #ff9166;}
            QTableWidget::item:enabled {background-color: #f1f1f1;}
            QTableWidget::item:enabled:selected {border-top: 1px solid #dbdbdb; border-bottom: 1px solid #dbdbdb;
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ececec, stop: 1.0 #dedede); color:#808080;}
            QTableWidget::item:enabled:focus {background: #f17a4c; border-top: 1px solid #f17a4c; border-bottom: 1px solid #f17a4c; color: #fff;}
            QHeaderView {font: 10px Arial; color: #808080;}
            QScrollBar:vertical {border: none; background: #efefef; width: 3px;}
            QScrollBar::handle:vertical {max-height: 0; background: #f17a4c;}
            ''')
        table.setColumnCount(3)
        table.setColumnWidth(1, 60)
        table.setColumnWidth(2, 70)
        table.setHorizontalHeaderLabels(("Имя", "Расш.", "Размер"))
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.setIconSize(QSize(19, 19))
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)


class PopupMenu:

    def __init__(self, table, position):
        """ Popup Menu """
        position.setY(position.y() + 21)
        popup_menu = QMenu(table)
        popup_menu.setStyleSheet('''
            QMenu {border: 1px solid #b8b8b8; font: 12px Arial; margin: 0; background: #eaeaea;}
            QMenu::item {padding: 9px 30px; color: #5a5a5a;}
            QMenu::item:selected {color: #ffffff; background: #297fb8;}
            QMenu::separator {height: 1px; margin: 0; background: #b8b8b8;}
        ''')
        popup_menu.setCursor(Qt.PointingHandCursor)
        popup_menu.addAction("Symlink", table.create_link)
        popup_menu.addSeparator()
        popup_menu.addAction("Refresh", table.refresh_panel)
        popup_menu.addAction("Panel mirror", table.mirror_path)
        popup_menu.addSeparator()
        popup_menu.addAction("Disk size", table.disk_size)
        popup_menu.addSeparator()
        popup_menu.addAction("Copy path", table.path_to_clipboard)
        popup_menu.addAction("Copy name", table.name_to_clipboard)
        popup_menu.addAction("Rename", table.rename_item)
        popup_menu.addAction("Delete", table.delete_item)
        popup_menu.exec_(table.mapToGlobal(position))
        popup_menu.deleteLater()


class RenameUI:

    def __init__(self, _widg, old_name):
        """ Rename widget """
        _widg.setWindowFlags(Qt.FramelessWindowHint)
        _widg.setAttribute(Qt.WA_DeleteOnClose)
        _widg.setFixedSize(460, 58)
        _widg.setObjectName("Rename")
        _widg.setStyleSheet('''
            QFrame {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f2f2f2, stop: 1.0 #e1e1e1);
            border: 1px solid #bdbdbd;}
            QLabel {font: bold 13px Verdana; color: #42688f; border: none;}
            QLineEdit {padding-left: 5px;}
        ''')
        title = QLabel()
        title.setAlignment(Qt.AlignCenter)
        title.setText("Rename:")
        _widg.line = QLineEdit()
        _widg.line.setText(old_name)
        _widg.line.setMinimumHeight(34)
        box = QHBoxLayout()
        box.addWidget(title)
        box.insertSpacing(1, 15)
        box.addWidget(_widg.line)
        box.setContentsMargins(13, 10, 13, 10)
        _widg.setLayout(box)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(7)
        effect.setOffset(0)
        _widg.setGraphicsEffect(effect)
        _widg.line.setFocus(True)


class LinkUI:

    def __init__(self, _widg, source):
        """ Link widget """
        _widg.setWindowFlags(Qt.FramelessWindowHint)
        _widg.setAttribute(Qt.WA_DeleteOnClose)
        _widg.setFixedSize(365, 160)
        _widg.setObjectName("Link")
        _widg.setStyleSheet('''
            QFrame#Link {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f2f2f2, stop: 1.0 #e1e1e1);
            border: 1px solid #bdbdbd;}
            QLabel {font: bold 13px Verdana; color: #42688f; border: none;}
            QLineEdit {padding-left: 5px;}
        ''')
        _widg._from = QLabel()
        _widg._from.setMinimumSize(320, 18)
        _widg._from.setText("Source:")
        _widg._from_input = QLineEdit()
        _widg._from_input.setText(source)
        _widg._from_input.setMinimumSize(320, 34)
        _widg._to = QLabel()
        _widg._to.setMinimumSize(320, 18)
        _widg._to.setText("Symlink:")
        _widg._to_input = QLineEdit()
        _widg._to_input.setMinimumSize(320, 34)
        _widg.box = QVBoxLayout()
        _widg.box.addWidget(_widg._from)
        _widg.box.addWidget(_widg._from_input)
        _widg.box.addSpacing(10)
        _widg.box.addWidget(_widg._to)
        _widg.box.addWidget(_widg._to_input)
        _widg.box.setContentsMargins(20, 15, 20, 20)
        _widg.setLayout(_widg.box)
        _widg._to_input.setFocus(True)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(7)
        effect.setOffset(0)
        _widg.setGraphicsEffect(effect)


class ReadUI:

    def __init__(self, _widg):
        """ Read widget """
        _widg.setWindowFlags(Qt.FramelessWindowHint)
        _widg.setAttribute(Qt.WA_DeleteOnClose)
        _widg.setStyleSheet('''
            QWidget {background: #f2f2f2;}
            QTextEdit {color: #494949; border: none; background: #f2f2f2; font-size: 13px;}
            QScrollBar:vertical {border: none; background-color: #e0e0e0; width: 4px;}
            QScrollBar::handle:vertical {max-height: 0; background-color: #f17a4c;}
            QLabel#topbar {font: 11px Arial; color: #898989;}
            QLabel#linecount {font: 10px Arial; color: #898989; padding-right: 10px;}
            QMenuBar {font:11px Arial; color: #373737;}
            QMenuBar::item {background: #efefef;}
            QMenuBar::item:pressed {background-color: #e7e7e7;}
            QMenu {background-color: #e7e7e7; font: 10px Arial; color: #656565; min-width: 80px;}
            QMenu::item:selected {color: #fff;}
        ''')
        _widg.topbar = QLabel()
        _widg.topbar.setObjectName("topbar")
        _widg.topbar.setAlignment(Qt.AlignHCenter | Qt.AlignCenter)
        _widg.topbar.setMinimumHeight(22)
        _widg.menubar = QMenuBar(_widg.topbar)
        _widg.menubar.setMinimumHeight(20)
        _widg.menubar.setMaximumWidth(80)
        _widg.menubar.setCursor(Qt.PointingHandCursor)
        _widg.menu = QMenu("Encoding", _widg.menubar)
        _widg.menu.setCursor(Qt.PointingHandCursor)
        codec_default = QAction("UTF-8", _widg, triggered=_widg.changecodec)
        codec_default16 = QAction("UTF-16", _widg, triggered=_widg.changecodec)
        codec_1 = QAction("cp1250", _widg, triggered=_widg.changecodec)
        codec_2 = QAction("cp1251", _widg, triggered=_widg.changecodec)
        codec_3 = QAction("cp1252", _widg, triggered=_widg.changecodec)
        codec_4 = QAction("866", _widg, triggered=_widg.changecodec)
        codec_5 = QAction("Koi8-r", _widg, triggered=_widg.changecodec)
        codec_6 = QAction("Koi8-u", _widg, triggered=_widg.changecodec)
        codec_7 = QAction("iso8859-5", _widg, triggered=_widg.changecodec)
        _widg.menu.addAction(codec_default)
        _widg.menu.addAction(codec_default16)
        _widg.menu.addAction(codec_1)
        _widg.menu.addAction(codec_2)
        _widg.menu.addAction(codec_3)
        _widg.menu.addAction(codec_4)
        _widg.menu.addAction(codec_5)
        _widg.menu.addAction(codec_6)
        _widg.menu.addAction(codec_7)
        _widg.menubar.addMenu(_widg.menu)
        _widg.display = QTextEdit()
        _widg.display.setReadOnly(True)
        _widg.linecount = QLabel()
        _widg.linecount.setObjectName("linecount")
        _widg.linecount.setMinimumHeight(20)
        _widg.linecount.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        vbox = QVBoxLayout(_widg)
        vbox.addWidget(_widg.topbar)
        vbox.addSpacing(10)
        vbox.addWidget(_widg.display)
        vbox.addWidget(_widg.linecount)
        _widg.setLayout(vbox)


class CreateUI:

    def __init__(self, _widg):
        """ Create widget """
        _widg.setWindowFlags(Qt.FramelessWindowHint)
        _widg.setAttribute(Qt.WA_DeleteOnClose)
        _widg.setFixedSize(460, 58)
        _widg.setObjectName("Create")
        _widg.setStyleSheet('''
            QFrame#Create {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f2f2f2, stop: 1.0 #e1e1e1);
            border: 1px solid #bdbdbd;}
            QLabel {font: bold 13px Verdana; color: #42688f;}
            QLineEdit {padding-left: 3px;}
        ''')
        _widg.title = QLabel()
        _widg.title.setMinimumHeight(30)
        _widg.InputValue = QLineEdit()
        _widg.InputValue.setMinimumHeight(30)
        box = QHBoxLayout()
        box.addWidget(_widg.title)
        box.insertSpacing(1, 10)
        box.addWidget(_widg.InputValue)
        box.setContentsMargins(13, 10, 13, 10)
        _widg.setLayout(box)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(7)
        effect.setOffset(0)
        _widg.setGraphicsEffect(effect)
        _widg.InputValue.setFocus(True)
