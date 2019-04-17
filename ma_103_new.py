from PyQt5 import QtWidgets
from PyQt5 import QtCore
import sys, re, collections, qtawesome


class Msg_als(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.edit = False  # 编辑状态
        self.action_open.triggered.connect(self.open_file)
        self.pushButton_note.clicked.connect(self.open_edit)
        self.pushButton_save.clicked.connect(self.save_file)
        self.comboBox_date1.currentIndexChanged.connect(self.change_timelist_1)
        self.comboBox_time1.currentIndexChanged.connect(self.change_datelist_2)
        self.comboBox_date2.currentIndexChanged.connect(self.change_timelist_2)
        self.pushButton_search.clicked.connect(self.search)
        self.action_save.triggered.connect(self.save_file)

    def init_ui(self):
        """初始化UI"""
        """菜单栏"""
        self.action_open = QtWidgets.QAction(qtawesome.icon('fa.folder-open', color="black"), '打开(O)')
        self.action_open.setShortcut('Ctrl+O')
        self.action_save = QtWidgets.QAction(qtawesome.icon('fa.save', color="black"), '保存(S)')
        self.action_save.setShortcut('Ctrl+S')
        self.menubar = self.menuBar()
        self.menu_F = self.menubar.addMenu('&文件')
        self.menu_F.addAction(self.action_open)
        self.menu_F.addAction(self.action_save)
        """状态栏"""
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        """主窗口"""
        self.setFixedSize(1000, 600)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        """左窗口"""
        self.left_widget = QtWidgets.QWidget()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        """右窗口"""
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        """设置窗口占位"""
        self.main_layout.addWidget(self.left_widget, 0, 0, 10, 2)  # 10行2列
        self.main_layout.addWidget(self.right_widget, 0, 2, 10, 10)  # 10行12列
        self.setCentralWidget(self.main_widget)
        """设置部件"""
        self.pushButton_search = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='#AFB1B3'), "搜索")
        self.pushButton_search.setObjectName('left_button')
        self.pushButton_note = QtWidgets.QPushButton(qtawesome.icon('fa.pencil-square-o', color='#AFB1B3'), "笔记")
        self.pushButton_note.setObjectName('left_button')
        self.pushButton_save = QtWidgets.QPushButton(qtawesome.icon('fa.save', color='white'), "保存")
        self.pushButton_save.setObjectName('left_button')
        self.pushButton_feedback = QtWidgets.QPushButton(qtawesome.icon('fa.telegram', color='white'), "反馈")
        self.pushButton_feedback.setObjectName('left_button')
        self.begin_label = QtWidgets.QPushButton('开始时间')
        self.begin_label.setObjectName('left_label')
        self.end_label = QtWidgets.QPushButton('结束时间')
        self.end_label.setObjectName('left_label')
        self.display_select = QtWidgets.QTextEdit()
        self.display_select.setReadOnly(True)
        self.comboBox_date1 = QtWidgets.QComboBox()
        self.comboBox_date1.setObjectName('left_combobox')
        self.comboBox_time1 = QtWidgets.QComboBox()
        self.comboBox_time1.setObjectName('left_combobox')
        self.comboBox_date2 = QtWidgets.QComboBox()
        self.comboBox_date2.setObjectName('left_combobox')
        self.comboBox_time2 = QtWidgets.QComboBox()
        self.comboBox_time2.setObjectName('left_combobox')
        self.display_widget = QtWidgets.QWidget()
        self.display_widget.setObjectName('display_widget')
        self.display_layout = QtWidgets.QGridLayout()
        self.display_widget.setLayout(self.display_layout)
        self.tempwidget = QtWidgets.QWidget()
        """给左窗口添加部件"""
        self.left_layout.addWidget(self.begin_label, 0, 0, 1, 2)
        self.left_layout.addWidget(self.comboBox_date1, 1, 0, 1, 2)
        self.left_layout.addWidget(self.comboBox_time1, 2, 0, 1, 2)
        self.left_layout.addWidget(self.end_label, 3, 0, 1, 2)
        self.left_layout.addWidget(self.comboBox_date2, 4, 0, 1, 2)
        self.left_layout.addWidget(self.comboBox_time2, 5, 0, 1, 2)
        self.left_layout.addWidget(self.pushButton_search, 6, 0, 1, 2)
        self.left_layout.addWidget(self.pushButton_note, 7, 0, 1, 2)
        self.left_layout.addWidget(self.pushButton_save, 8, 0, 1, 2)
        self.left_layout.addWidget(self.pushButton_feedback, 9, 0, 1, 2)
        """给右窗口添加部件"""
        self.right_layout.addWidget(self.display_widget, 0, 2, 10, 6)
        self.right_layout.addWidget(self.tempwidget, 0, 8, 10, 6)
        self.display_layout.addWidget(self.display_select, 0, 2, 1, 1)
        """样式表"""
        self.setWindowOpacity(0.99)  # 窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.left_widget.setStyleSheet('''
        QWidget#left_widget{
        background-color:#232F3F;
        border-top-left-radius:10px;
        border-top-right-radius:10px;
        border-bottom-left-radius:10px;
        border-bottom-right-radius:10px;
        }
        QPushButton{
        border:none;
        background-color:none;
        color:#F49900;}
        QPushButton#left_label{
        border:none;
        border-bottom:2px solid white;
        font-size:18px;
        font-weight:700;
        font-family:"等线"}
        QPushButton#left_button:hover{
        border-left:4px solid red;
        font-weight:700}
        QPushButton#left_combobox{border:1px solid lightgray}''')
        self.display_select.setStyleSheet('''
        QTextEdit{
        color:#000000;
        background-color:#F5F5F5;
        border:1px solid gray;
        width:300px;
        border-top-left-radius:10px;
        border-top-right-radius:10px;
        border-bottom-left-radius:10px;
        border-bottom-right-radius:10px;
        font-family:"微软雅黑"}
        ''')
        self.menubar.setStyleSheet('''
        background-color:#FFFFFF;
        border-bottom:2px solid white;
        color:black;
        menu_F:hover{
        background-color:#4B6EAF;}''')
        self.statusbar.setStyleSheet('''
        background-color:#FFFFFF;''')
        self.main_widget.setStyleSheet('''
        background-color:#FFFFFF;''')

    def save_file(self):
        try:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '打开', 'C:\\', 'Text Files (*.txt)')
        except:
            pass
        f = open(path, mode='w', encoding='utf-8')
        f.write(str(self.display_select.toPlainText()))
        f.close()
        self.statusbar.showMessage('已保存至' + path, msecs=700)

    def open_file(self):
        """文件打开显示并生成日期目录 """
        global dates_list
        dates_list = collections.OrderedDict()
        global file
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubi\\Desktop',
                                                        'Text Files (*.txt)')
        self.statusbar.showMessage("已打开 " + file, msecs=20)
        pattern_date = re.compile(
            r'(?P<date1>2019-\d+-\d+) (?P<date2>\d{2}:\d{2}:\d{2})')
        try:
            file_opened = open(file, mode='r', encoding='utf-8')
            for line in file_opened:
                dates = re.findall(pattern_date, line)
                if dates:
                    if dates[0][0] not in dates_list.keys():
                        dates_list[dates[0][0]] = [dates[0][1]]
                    else:
                        dates_list[dates[0][0]].append(dates[0][1])
            file_opened.close()
            # 显示初始日期，时间会自动调用更新函数
            self.comboBox_date1.addItems(dates_list.keys())
        except BaseException:
            pass

    def change_timelist_1(self):
        """根据日期选择更新时间列表1"""
        try:
            self.comboBox_time1.clear()
            self.comboBox_time1.addItems(
                dates_list[self.comboBox_date1.currentText()])
        except:
            pass

    def change_datelist_2(self):
        """根据起始时间选择更新结束日期列表"""
        self.comboBox_date2.clear()
        try:
            if dates_list[self.comboBox_date1.currentText(
            )][-1] == self.comboBox_time1.currentText():
                self.comboBox_date2.addItems([i for i in list(dates_list.keys()) if
                                              list(dates_list.keys()).index(i) > list(dates_list.keys()).index(
                                                  self.comboBox_date1.currentText())])

            else:
                self.comboBox_date2.addItems([i for i in list(dates_list.keys()) if
                                              list(dates_list.keys()).index(i) >= list(dates_list.keys()).index(
                                                  self.comboBox_date1.currentText())])
        except:
            pass

    def change_timelist_2(self):
        """根据结束日期变化更新结束时间表"""
        self.comboBox_time2.clear()
        try:
            if self.comboBox_date2.currentText() != self.comboBox_date1.currentText():
                self.comboBox_time2.addItems(
                    dates_list[self.comboBox_date2.currentText()])
            else:
                self.comboBox_time2.addItems([i for i in dates_list[self.comboBox_date1.currentText()] if
                                              dates_list[self.comboBox_date1.currentText()].index(i) > dates_list[
                                                  self.comboBox_date1.currentText()].index(
                                                  self.comboBox_time1.currentText())])
        except:
            pass

    def search(self):
        self.display_select.clear()
        # 按时间段进行搜索显示
        for i in range(list(dates_list.keys()).index(self.comboBox_date1.currentText()),
                       list(dates_list.keys()).index(self.comboBox_date2.currentText()) + 1):
            if self.comboBox_date1.currentText() == self.comboBox_date2.currentText():
                for item in dates_list[list(dates_list.keys())[i]]:
                    if dates_list[
                        list(dates_list.keys())[i]].index(self.comboBox_time2.currentText()) >= dates_list[
                        list(dates_list.keys())[i]].index(item) >= dates_list[
                        list(dates_list.keys())[i]].index(self.comboBox_time1.currentText()):
                        self.show216(list(dates_list.keys())[i], item)
            elif list(dates_list.keys()).index(self.comboBox_date1.currentText()) == i:
                for item in dates_list[list(dates_list.keys())[i]]:
                    if dates_list[list(dates_list.keys())[i]].index(item) >= dates_list[
                        list(dates_list.keys())[i]].index(self.comboBox_time1.currentText()):
                        self.show216(list(dates_list.keys())[i], item)
            elif list(dates_list.keys()).index(self.comboBox_date2.currentText()) == i:
                for item in dates_list[list(dates_list.keys())[i]]:
                    if dates_list[list(dates_list.keys())[i]].index(item) <= dates_list[
                        list(dates_list.keys())[i]].index(self.comboBox_time2.currentText()):
                        self.show216(list(dates_list.keys())[i], item)
            else:
                for item in dates_list[list(dates_list.keys())[i]]:
                    self.show216(list(dates_list.keys())[i], item)

    def show216(self, date, time):
        """ 根据时间选择显示216开关结果"""
        file_temp = open(file, mode='r', encoding='utf-8')
        file_opened = file_temp.read()
        pattern_str = date + ' ' + time + '\n' + \
                      r'(?P<content>.+?)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content_msg = re.search(pattern_date, file_opened)
        src = content_msg['content'].strip()
        # 在时间段中查找216记录
        pattern_linematch_send1 = re.compile(
            r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+?)')
        pattern_linematch_send2 = re.compile(r'^\s')
        pattern_linematch_receive1 = re.compile(
            r'(?P<content_216>RX-.+?F0 A0 (?P<value>0[12]).+?)')
        pattern_linematch_receive2 = re.compile(r'^\s')
        search_result = []
        pre_signal = False
        rev_signal = False
        for line in src.split('\n'):
            if re.match(pattern_linematch_send1, line):
                pre_signal = True
                search_result.append(line)
            elif pre_signal & bool(re.match(pattern_linematch_send2, line)):
                search_result.append(line)
            elif pre_signal & (not bool(re.match(pattern_linematch_send2, line))):
                pre_signal = False
            elif re.match(pattern_linematch_receive1, line):
                rev_signal = True
                search_result.append(line)
            elif rev_signal & bool(re.match(pattern_linematch_receive2, line)):
                search_result.append(line)
            elif rev_signal & (not bool(re.match(pattern_linematch_receive2, line))):
                rev_signal = False
        self.display_select.setHtml(self.createhtml(search_result, date, time))
        QtWidgets.QApplication.processEvents()
        file_temp.close()

    def createhtml(self, result_list, date, time):
        result_str = ''
        if list:
            for item in result_list:
                result_str += (self.word2html(item, 0))
            html = self.display_select.toHtml() + '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time + '</h2><hr>' + result_str
        else:
            html = self.display_select.toHtml() + '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time + '</h2><hr><p style="color:#499C54;text-align:center">无记录</p>'
        return html

    def word2html(self, src, line):
        """'文本转标记"""
        if line == 1:
            src = src.replace('\n', '<br/>')
        src = src.replace(
            '           ',
            '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        src = src.replace(
            'TX', '<font style="font-weight:bold;color:#db2d43">TX</font>')
        src = src.replace(
            'RX', '<font style="font-weight:bold;color:#00bd56">RX</font>')
        src = '<p style="text-align:left;color:#BE9117">' + src + '</p>'
        return src

    def open_edit(self):
        if not self.edit:
            self.display_select.setReadOnly(False)  # 打开编辑，方便做笔记
            self.statusbar.showMessage("已开启编辑")
            self.edit = True
        else:
            self.display_select.setReadOnly(True)
            self.statusbar.showMessage("已关闭编辑", msecs=200)
            self.edit = False


app = QtWidgets.QApplication(sys.argv)
win = Msg_als()
win.show()
sys.exit(app.exec_())
