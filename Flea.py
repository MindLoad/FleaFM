# -*- coding: utf-8 -*-
# Created: 05.01.18
# Changed: 12.02.18

import os
import sys
import array
import shutil
import subprocess
import logging


from ui import RootUI, TableWidget, PopupMenu, RenameUI, LinkUI, ReadUI, CreateUI, SelectByMaskUI
from flea_context import DBConnection, logs
from collections import namedtuple
from contextlib import suppress
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFrame, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QFont, QBrush, QColor, QPaintEvent, QPainter, QFocusEvent, QKeyEvent
from PyQt5.QtCore import Qt, QSize


class Root(QFrame):

    def __init__(self):
        super(Root, self).__init__()
        self._settings()

        self.ui = RootUI(self, MyTableWidget)
        self._clicks()

        """ Create tables """
        self.ui.leftPanel.generate_table()
        self.ui.rightPanel.generate_table()
        self.ui.rightPanel.setFocus()
        """ Check disk partition size """
        self.ui.lbl_disk_num.setText(disk_quote(Path('/')))
        self.ui.rbl_disk_num.setText(disk_quote(Path.home()))

    def _settings(self):
        self.dialog = False
        with DBConnection('settings.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM setting")
            for _ in result.fetchall():
                value, param1, param2, param3, param4, param5 = _
                if value == 'resolution':
                    self.setMinimumSize(param4, param5)
                elif value == 'editor':
                    self.editor = param2

    def _clicks(self):
        self.ui.tool_terminal.clicked.connect(self.run_terminal)
        self.ui.tool_rights.clicked.connect(self.run_rights)

    def sync(self, panel):
        return self.ui.sync_panel[panel]

    def run_terminal(self):
        self.panel = self.focusWidget()
        print(self.panel.path)

    def run_rights(self):
        self.panel = self.focusWidget()
        print(self.panel.path / self.panel.currentItem().text())

    def resizeEvent(self, event):
        if self.dialog:
            self.showread.setFixedSize(self.size())


@logs
def error(message):
    _error = Error(message)
    _error.show()


def disk_quote(path):
    disk = shutil.disk_usage(path)
    result = f"{human_size(disk.total)} / Free {human_size(disk.free)} ~ {disk.free * 100 / disk.total:.1f}%"
    return result


def human_size(size):
    for index in _suffix:
        size /= 1024
        if size < 1024:
            return f"{size:.1f} {index}"


class DirList:

    DirItems = namedtuple('DirItems', 'name_ size_ isDir_')

    def __init__(self, parent):
        self.parent = parent
        self._items = [self.DirItems(item.name, self.calc_size(item), item.is_dir())
                       for item in parent.path.iterdir()]

    def __len__(self):
        return len(self._items)

    def __getitem__(self, pos):
        return self._items[pos]

    @property
    def items_name(self):
        return (i.name_ for i in self._items)

    @property
    def folders(self):
        if self.parent.hide:
            return sorted([i for i in self._items if i.isDir_ and not i.name_.startswith('.')])
        else:
            return sorted([i for i in self._items if i.isDir_])

    @property
    def folders_name(self):
        if self.parent.hide:
            return (i.name_ for i in self._items if i.isDir_ and not i.name_.startswith('.'))
        else:
            return (i.name_ for i in self._items if i.isDir_)

    @property
    def files(self):
        if self.parent.hide:
            return sorted([i for i in self._items if not i.isDir_ and not i.name_.startswith('.')])
        else:
            return sorted([i for i in self._items if not i.isDir_])

    @property
    def files_name(self):
        if self.parent.hide:
            return (i.name_ for i in self._items if not i.isDir_ and not i.name_.startswith('.'))
        else:
            return (i.name_ for i in self._items if not i.isDir_)

    @property
    def len_folders(self):
        return len(self.folders)

    @property
    def len_files(self):
        return len(self.files)

    def calc_size(self, item):
        with suppress(OSError):
            return human_size(item.stat().st_size)

    def total_size(self):
        return f"{sum(i.size_ for i in self._items if isinstance(i.size_, int)) / 1048576:.1f} Mb"


class MyTableWidget(QTableWidget):

    def __init__(self, _path, _tool):
        self.hide = True
        self.path = _path
        self.tool_path, self.tool_folders, self.tool_files, self.tool_selection, self.tool_disk_size = _tool
        self.insert = set()
        self.insert_sum = array.array('i')
        super(MyTableWidget, self).__init__()
        self.font_active = QFont("Arial", 10)
        self.font_inactive = QFont("Arial", 9)
        self.read_panel = DirList(self)
        self.table_ui = TableWidget(self)
        self.customContextMenuRequested.connect(self.popup)
        self.doubleClicked.connect(self.double)

    def generate_table(self):
        self.tool_selection.clear()
        self.insert.clear()
        del self.insert_sum[:]
        """ Generate table """
        self.setRowCount(self.read_panel.len_folders + self.read_panel.len_files + 1)
        dir_back = QTableWidgetItem("..")
        dir_back.setIcon(QIcon(QPixmap(":/back_dir")))
        self.setItem(0, 0, dir_back)
        dir_back_ext = QTableWidgetItem("")
        dir_back_size = QTableWidgetItem("")
        for item in (dir_back_ext, dir_back_size):
            item.setFlags(Qt.ItemIsSelectable)
        self.setItem(0, 1, dir_back_ext)
        self.setItem(0, 2, dir_back_size)
        self.setRowHeight(0, 24)
        if self.read_panel.folders:
            for index, folder_ in enumerate(self.read_panel.folders, start=1):
                dir_ = QTableWidgetItem(folder_.name_)
                dir_.setIcon(QIcon(QPixmap(":/dir")))
                dir_.setFont(self.font_active)
                self.setItem(index, 0, dir_)
                dir_ext = QTableWidgetItem("<dir>")
                dir_ext.setFlags(Qt.ItemIsSelectable)
                dir_ext.setFont(self.font_inactive)
                self.setItem(index, 1, dir_ext)
                dir_2 = QTableWidgetItem("")
                dir_2.setFlags(Qt.ItemIsSelectable)
                dir_2.setFont(self.font_inactive)
                self.setItem(index, 2, dir_2)
                self.setRowHeight(index, 23)
        if self.read_panel.files:
            for index, files_ in enumerate(self.read_panel.files, start=self.read_panel.len_folders + 1):
                extension = Path(files_.name_).suffix[1:]
                logo = ":/file"
                file_ = QTableWidgetItem(files_.name_)
                file_.setIcon(QIcon(QPixmap(logo)))
                file_.setFont(self.font_active)
                self.setItem(index, 0, file_)
                file_ext = QTableWidgetItem()
                file_ext.setData(Qt.DisplayRole, extension)
                file_ext.setFlags(Qt.ItemIsSelectable)
                file_ext.setFont(self.font_inactive)
                self.setItem(index, 1, file_ext)
                file_size = QTableWidgetItem()
                file_size.setData(Qt.DisplayRole, files_.size_)
                file_size.setFlags(Qt.ItemIsSelectable)
                file_size.setFont(self.font_inactive)
                self.setItem(index, 2, file_size)
                self.setRowHeight(index, 23)
        self.tool_path.setText(self.path.as_posix())
        self.tool_folders.setText(str(self.read_panel.len_folders))
        self.tool_files.setText(str(self.read_panel.len_files))

    def popup(self, position):
        if self.currentItem().row() != 0:
            self.pop_menu = PopupMenu(self, position)

    def create_link(self):
        self.showlink = Link(self)
        self.showlink.show()

    def refresh_panel(self):
        self.read_panel = DirList(self)
        self.generate_table()

    def mirror_path(self):
        mirror_panel = main.sync(self)
        mirror_panel.path = self.path
        mirror_panel.read_panel = DirList(self)
        mirror_panel.generate_table()

    def disk_size(self):
        self.tool_disk_size.setText(disk_quote(self.path))

    def path_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(str(self.path))

    def name_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.currentItem().text())

    def rename_item(self):
        self.showrename = Rename(self)
        self.showrename.show()

    def delete_item(self):
        """ Delete """

    def double(self):
        if self.currentItem().text() == "..":
            if os.access(self.path.parent, os.R_OK):
                up_dir_item = self.path.name
                self.path = self.path.parent
                self.refresh_panel()
                find_up_dir_item = self.findItems(up_dir_item, Qt.MatchExactly)[0]
                self.setCurrentItem(find_up_dir_item)
            else:
                return error("< Access to folder denied >")
        elif Path(self.path, self.currentItem().text()).is_dir():
            _ = Path(self.path, self.currentItem().text())
            if os.access(_, os.R_OK):
                self.path = _
                self.refresh_panel()
                self.setCurrentItem(self.item(0, 0))
            else:
                return error("< Access to folder denied >")

    def to_insert(self, item):
        self.insert.add(item.text())
        item.setForeground(QBrush(QColor("#ff9d29")))
        if item.text() in self.read_panel.files_name:
            self.insert_sum.append((self.path / item.text()).stat().st_size)
        self.tool_selection.setText(f"selected: {len(self.insert)} / {human_size(sum(self.insert_sum))}")

    def from_insert(self, item):
        self.insert.remove(item.text())
        item.setForeground(QBrush(QColor("#3a3a3a")))
        if item.text() in self.read_panel.files_name:
            self.insert_sum.remove((self.path / item.text()).stat().st_size)
        self.tool_selection.setText(f"selected: {len(self.insert)} / {human_size(sum(self.insert_sum))}") if self.insert else self.tool_selection.clear()

    def bookmark(self, path):
        self.path = Path(path)
        self.refresh_panel()
        self.setCurrentItem(self.item(0, 0))

    def read_file(self, stat):
        _name = self.currentItem().text()
        if _name in self.read_panel.files_name:
            _file = self.path / _name
            if stat == 'read':
                if os.access(_file, os.W_OK):
                    main.dialog = True
                    main.showread = Read(_file, self)
                    main.showread.setFixedSize(main.size())
                    main.showread.move(0, 0)
                    main.showread.show()
                else:
                    error("< Permission denied >")
            else:
                try:
                    subprocess.Popen([main.editor, _file]) if os.access(_file, os.W_OK) else error('< Permission denied >')
                except FileNotFoundError:
                    return error("< Default editor error! >")
        else:
            """ Show folder size """

    def create_obj(self, stat):
        if os.access(self.path, os.W_OK):
            main.creat_ui = Create(self, stat)
            main.creat_ui.show()
        else:
            return error("< Write access Denied! >")

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.modifiers() == Qt.ShiftModifier and a0.key() == Qt.Key_F4:
            """ Create file """
            self.create_obj("Create file")
        elif a0.key() == Qt.Key_Tab:
            # main.focusWidget().objectName()
            """ Panel switching """
            main.sync(self).setFocus(True)
        elif a0.key() == Qt.Key_Enter or a0.key() == Qt.Key_Return:
            """ Enter Key """
            self.double()
        elif a0.key() == Qt.Key_Backspace:
            """ Backspace Key """
            self.setCurrentItem(self.item(0, 0))
            self.double()
        elif a0.modifiers() == Qt.ControlModifier and a0.key() == Qt.Key_H:
            """ Hide / Unhide """
            self.hide = False if self.hide else True
            self.generate_table()
        elif a0.key() == Qt.Key_Insert:
            """ Insert Key """
            if self.currentItem().row() != 0:
                item = self.currentItem()
                self.to_insert(item) if item.text() not in self.insert else self.from_insert(item)
                if item.row() < len(self.read_panel.folders) + len(self.read_panel.files):
                    self.setCurrentItem(self.item(item.row() + 1, 0))
            else:
                self.setCurrentItem(self.item(1, 0))
        elif a0.key() == Qt.Key_F3:
            """ Read """
            self.read_file('read')
        elif a0.key() == Qt.Key_F4:
            """ Edit """
            self.read_file('write')
        elif a0.key() == Qt.Key_F5:
            """ F5 Key sorted(z, key=lambda x: Path(x).suffix[1:]) """
        elif a0.key() == Qt.Key_F7:
            """ Create folder """
            self.create_obj("Create folder")
        elif a0.key() == Qt.Key_F10:
            """ Close App """
            main.close()
        elif a0.key() == Qt.Key_F11:
            """ Full Screen """
            if not main.isMaximized():
                main.showMaximized()
            else:
                main.showNormal()
        elif a0.key() == Qt.Key_Plus:
            self.selectfind = SelectByMask(self, 1)
            self.selectfind.show()
        elif a0.key() == Qt.Key_Minus:
            self.selectfind = SelectByMask(self, 2)
            self.selectfind.show()
        else:
            return QTableWidget.keyPressEvent(self, a0)


class Link(QFrame):

    def __init__(self, panel):
        self.panel = panel
        super(Link, self).__init__(main)
        self.ui = LinkUI(self, str(panel.path / panel.currentItem().text()))
        self.move(main.width() / 2 - 180, main.height() / 2 - 80)
        self._to_input.returnPressed.connect(self.run)

    def run(self):
        from_ = self._from_input.text()
        to_ = self._to_input.text().lstrip(' ').rstrip(' ')
        to_panel = main.sync(self.panel)
        if not Path(from_).exists():
            return error("< Wrong source destination >")
        if not to_:
            return error("< Wrong target destination >")
        try:
            Path(to_panel.path / to_).symlink_to(from_)
            to_panel.refresh_panel()
            if to_panel.path == self.panel.path:
                self.panel.refresh_panel()
        except PermissionError:
            return error("< Create Link / Access Denied >")
        except FileExistsError:
            return error("< Create Link / File already exist >")
        self.close()
        self.panel.setFocus(True)

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


class Rename(QFrame):

    def __init__(self, panel):
        self.panel = panel
        super(Rename, self).__init__(main)
        self.ui = RenameUI(self, panel.currentItem().text())
        self.move(main.width() / 2 - 230, main.height() / 2 - 35)
        self.line.returnPressed.connect(self.run)

    def run(self):
        new_name = self.line.text()
        if new_name in self.panel.read_panel.items_name:
            error("< Such name already exists >")
            return
        fifo_path = self.panel.path / self.panel.currentItem().text()
        try:
            fifo_path.rename(self.panel.path / new_name)
        except PermissionError:
            return error("< Permission Error! >")
        self.panel.refresh_panel()
        with suppress(ValueError):
            relative = main.sync(self.panel).path.relative_to(fifo_path)
            main.sync(self.panel).path = self.panel.path / self.line.text() / relative
            main.sync(self.panel).refresh_panel()
        if self.panel.path == main.sync(self.panel).path:
            main.sync(self.panel).refresh_panel()
        self.close()
        self.panel.setFocus(True)

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


class Read(QFrame):

    def __init__(self, file, panel):
        self.file = file
        self.panel = panel
        super(Read, self).__init__(main)
        self.ui = ReadUI(self)
        self.topbar.setText(f"{self.file.name} / UTF-8")
        self.display.setFocus(True)
        self.show_text('UTF-8')
        self.codec = lambda: self.sender().text()

    def show_text(self, _codec):
        try:
            text = self.file.read_text(encoding=_codec)
        except (UnicodeDecodeError, UnicodeError) as err:
            text = f"<b>Unicode Error:</b><br>{err}"
        self.display.setText(text)
        lines = len(text.split('\n'))
        self.linecount.setText(f"Lines: {lines:3}")

    def changecodec(self):
        self.display.clear()
        self.topbar.setText(f"{self.file.name} / {self.codec()}")
        self.show_text(self.codec())

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            main.dialog = False
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


class Create(QFrame):

    def __init__(self, panel, stat):
        self.stat = stat
        self.panel = panel
        super(Create, self).__init__(main)
        self.ui = CreateUI(self)
        self.move(main.width() / 2 - 230, main.height() / 2 - 35)
        self.title.setText(stat)
        self.InputValue.returnPressed.connect(self.create)

    def create(self):
        path = self.panel.path / self.InputValue.text()
        if not path.exists():
            if self.stat == "Create file":
                path.touch()
            else:
                path.mkdir()
            self.panel.refresh_panel()
            new_item = self.panel.findItems(path.name, Qt.MatchExactly)[0]
            self.panel.setCurrentItem(new_item)
            self.close()
            self.panel.setFocus(True)
        else:
            return error("< Duplicate Names forbidden! >")

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


class SelectByMask(QFrame):

    def __init__(self, panel, arg):
        self.panel = panel
        self.arg = arg
        self.selectitem = None
        super(SelectByMask, self).__init__(main)
        self.ui = SelectByMaskUI(self)
        self.search_line.returnPressed.connect(self.select)
        if self.panel.objectName() == "__leftPanel":
            self.move(self.panel.width() / 2 - 120, self.panel.height() / 2 - 25)
        else:
            self.move(self.panel.width() * 3 / 2 - 100, self.panel.height() / 2 - 25)

    def select(self):
        text = self.search_line.text().replace(".", "\.").replace("*", ".+")
        exp = fr"^{text}$"
        self.selectitem = self.panel.findItems(exp, Qt.MatchRegExp)
        if self.selectitem:
            self.run()

    def run(self):
        self.panel.setCurrentItem(self.selectitem[0])
        for item in self.selectitem:
            if item.text() in self.panel.read_panel.items_name:
                if self.arg == 1:
                    self.panel.to_insert(item)
                else:
                    self.panel.from_insert(item)
        self.close()
        self.panel.setFocus(True)

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


class Error(QFrame):

    def __init__(self, message):
        self.message = message
        self.panel = main.focusWidget()
        super(Error, self).__init__(main)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFixedSize(380, 65)
        self.move(main.width() / 2 - 190, main.height() / 2 - 30)
        self.setFocus(True)

    def paintEvent(self, a0: QPaintEvent):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setBrush(QColor("#da1f0c"))
        paint.setPen(QColor("#fd2e0f"))
        paint.drawRoundedRect(0, 0, 380, 65, 2, 8)
        """ inProcess """
        # pixmap = QPixmap().load(":/error")
        # paint.drawPixmap(14, 14, pixmap)
        paint.setFont(QFont("Arial", 14, weight=75))
        paint.setPen(QColor("#f8ebff"))
        paint.drawText(70, 10, 310, 20, Qt.AlignLeft, "Error !")
        paint.setFont(QFont("Arial", 11, weight=0))
        paint.drawText(70, 35, 310, 30, Qt.AlignLeft, self.message)

    def focusOutEvent(self, a0: QFocusEvent):
        self.close()

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.key() == Qt.Key_Escape:
            self.close()
            self.panel.setFocus(True)
        else:
            return QWidget.keyPressEvent(self, a0)


if __name__ == '__main__':
    __author__ = 'Mind Load'
    _suffix = ('K', 'M', 'G', 'T')
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon"))
    main = Root()
    main.setWindowTitle("Flea")
    main.show()
    sys.exit(app.exec_())
