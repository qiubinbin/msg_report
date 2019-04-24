from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QFont
import re, collections, qtawesome
from feedback_win import FeedBack


class Button(QtWidgets.QPushButton):
    """复写QPushButton"""

    def __init__(self, icon: str):
        super().__init__()
        self.btn_icon = icon
        self.setIcon(qtawesome.icon(self.btn_icon, color='white'))  # 初始图标颜色

    def enterEvent(self, a0: QtCore.QEvent):
        """复写鼠标进入事件"""
        if self.enterEvent:
            self.setIcon(qtawesome.icon(self.btn_icon, color='red'))

    def leaveEvent(self, a0: QtCore.QEvent):
        """复写鼠标离开事件"""
        if self.leaveEvent:
            self.setIcon(qtawesome.icon(self.btn_icon, color='white'))


class TextView(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)  # 将ContextMenuPolicy设置为Qt.CustomContextMenu
        self.customContextMenuRequested.connect(self.showmenu)

    def showmenu(self):
        menu = QtWidgets.QMenu()
        action_paste = QtWidgets.QAction(qtawesome.icon('fa.clipboard', color='black'), '粘贴')
        action_paste.setShortcut('Ctrl+V')
        menu.addAction(action_paste)
        action_paste.triggered.connect(self.paste)
        menu.exec_(QtGui.QCursor.pos())


class Msg_als(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.feedwin = FeedBack()
        self.common_init()
        self.incoming_init()
        self.init_action_connect()

    def init_action_connect(self):
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.incoming_cabinet_201_202.triggered.connect(self.incoming_init)
        self.feeder_cabinet_211_212_213_214_215_216.triggered.connect(self.feeder_init)
        self.pushButton_note.clicked.connect(self.open_edit)
        self.pushButton_save.clicked.connect(self.save_file)
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_feedback.clicked.connect(self.feedwin.show)
        self.comboBox_date1.currentIndexChanged.connect(self.change_timelist_1)
        self.comboBox_time1.currentIndexChanged.connect(self.change_datelist_2)
        self.comboBox_date2.currentIndexChanged.connect(self.change_timelist_2)
        self.pushButton_clear.clicked.connect(self.clear)

    def common_init(self):
        """初始化UI"""
        """菜单栏"""
        self.action_open = QtWidgets.QAction(qtawesome.icon('fa.folder-open', color="black"), '打开(O)')
        self.action_open.setShortcut('Ctrl+O')
        self.action_save = QtWidgets.QAction(qtawesome.icon('fa.save', color="black"), '保存(S)')
        self.action_save.setShortcut('Ctrl+S')
        self.incoming_cabinet_201_202 = QtWidgets.QAction(qtawesome.icon('fa.share'), '进线柜')
        self.feeder_cabinet_211_212_213_214_215_216 = QtWidgets.QAction(qtawesome.icon('fa.share'), '馈线柜')
        self.menubar = self.menuBar()
        self.menu_F = self.menubar.addMenu('文件')
        self.menu_F.addAction(self.action_open)
        self.menu_F.addAction(self.action_save)
        self.menu_P = self.menubar.addMenu('协议')
        self.protocol_103 = self.menu_P.addMenu(qtawesome.icon('fa.file-word-o', color='black'), '103协议')
        self.protocol_103.addAction(self.incoming_cabinet_201_202)
        self.protocol_103.addAction(self.feeder_cabinet_211_212_213_214_215_216)
        """状态栏"""
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        """主窗口"""
        self.setWindowTitle('报文分析')
        # self.setWindowIcon(QIcon('images/icon.png'))
        self.setFixedSize(1000, 600)
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)
        """左窗口"""
        self.left_widget = QtWidgets.QFrame()
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)
        """右窗口"""
        self.right_widget = QtWidgets.QWidget()
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)
        """设置窗口占位"""
        self.main_layout.addWidget(self.left_widget, 0, 0, 10, 2)  # 10行2列
        self.main_layout.addWidget(self.right_widget, 0, 2, 10, 10)  # 10行10列
        self.setCentralWidget(self.main_widget)
        """设置部件"""
        self.pushButton_search = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='white'), "搜索")
        self.pushButton_search.setObjectName('left_button')
        self.pushButton_note = QtWidgets.QPushButton(qtawesome.icon('fa.pencil-square-o', color='white'), "笔记")
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
        self.display_select.setFont(QFont("Consolas", 8))
        self.display_select.setReadOnly(True)
        self.comboBox_date1 = QtWidgets.QComboBox()
        self.comboBox_date1.setObjectName('left_combobox')
        self.comboBox_time1 = QtWidgets.QComboBox()
        self.comboBox_time1.setObjectName('left_combobox')
        self.comboBox_date2 = QtWidgets.QComboBox()
        self.comboBox_date2.setObjectName('left_combobox')
        self.comboBox_time2 = QtWidgets.QComboBox()
        self.comboBox_time2.setObjectName('left_combobox')
        self.display_widget = QtWidgets.QFrame()
        self.display_widget.setObjectName('display_widget')
        self.display_layout = QtWidgets.QGridLayout()
        self.display_widget.setLayout(self.display_layout)
        self.transform_widget = QtWidgets.QWidget()
        self.transform_widget.setObjectName('transform_widget')
        self.transform_layout = QtWidgets.QGridLayout()
        self.transform_widget.setLayout(self.transform_layout)
        self.label_source = QtWidgets.QPushButton('源数据')
        self.label_source.setObjectName('label')
        self.label_protocol = QtWidgets.QPushButton('103规约')
        self.label_protocol.setObjectName('label')
        self.pushButton_execute = Button('fa.download')
        self.pushButton_execute.setObjectName('button_execute')
        self.pushButton_execute.setToolTip('分析')
        self.pushButton_clear = Button('fa.undo')
        self.pushButton_clear.setObjectName('button_clear')
        self.pushButton_clear.setToolTip('清空')
        self.display_source = TextView()
        self.display_source.setToolTip('请在此处输入数据源')
        self.display_result = QtWidgets.QTextEdit()
        self.display_result.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)  # 关闭自带菜单
        self.display_result.setReadOnly(True)
        self.display_result.setToolTip('此处显示分析结果')
        self.display_result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.display_result.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        """给左窗口添加部件"""
        self.left_layout.addWidget(self.begin_label, 0)
        self.left_layout.addWidget(self.comboBox_date1, 1)
        self.left_layout.addWidget(self.comboBox_time1, 2)
        self.left_layout.addWidget(self.end_label, 3)
        self.left_layout.addWidget(self.comboBox_date2, 4)
        self.left_layout.addWidget(self.comboBox_time2, 5)
        self.left_layout.addWidget(self.pushButton_search, 6)
        self.left_layout.addWidget(self.pushButton_note, 7)
        self.left_layout.addWidget(self.pushButton_save, 8)
        self.left_layout.addWidget(self.pushButton_feedback, 9)
        """给右窗口添加部件"""
        self.right_layout.addWidget(self.display_widget, 0, 2, 10, 6)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        self.display_layout.addWidget(self.display_select, 0, 2)  # 结果显示窗口
        self.right_layout.addWidget(self.transform_widget, 0, 8, 10, 5)
        self.widget_title = QtWidgets.QFrame()
        self.widget_title.setObjectName('title')
        self.widget_title_layout = QtWidgets.QHBoxLayout()
        self.widget_title.setLayout(self.widget_title_layout)
        self.widget_uptitle = QtWidgets.QFrame()
        self.widget_uptitle_layout = QtWidgets.QVBoxLayout()
        self.widget_uptitle.setLayout(self.widget_uptitle_layout)
        self.widget_uptitle_layout.setContentsMargins(0, 0, 0, 0)
        self.widget_uptitle_layout.setSpacing(0)  # 取消默认间隔
        self.widget_uptitle_layout.addWidget(self.widget_title, 0)
        self.widget_uptitle_layout.addWidget(self.display_source, 1)
        self.transform_layout.setContentsMargins(0, 0, 0, 0)
        self.transform_layout.addWidget(self.widget_uptitle, 0, 8, 5, 5)
        self.transform_layout.addWidget(self.display_result, 5, 8, 5, 5)
        self.widget_title_layout.addWidget(self.label_source, 0)
        self.widget_title_layout.addStretch(6)  # 预留空白，调整布局
        self.widget_title_layout.addWidget(self.label_protocol, 1)
        self.widget_title_layout.addStretch(6)
        self.widget_title_layout.addWidget(self.pushButton_execute, 2)
        self.widget_title_layout.addWidget(self.pushButton_clear, 3)
        self.display_source.setContentsMargins(0, 0, 0, 0)
        icon = qtawesome.icon('fa.download', color='red')
        self.transform_widget.setStyleSheet('''
        QFrame#title{background-color: #242F3F;border-bottom:1px solid #305f72}
        QPushButton{border:none;background-color:none;color:#F49900;font:75 10pt "微软雅黑";}''')

    def incoming_init(self):
        self.statusbar.showMessage('请打开进线柜日志文件')
        self.style_incoming()

    def feeder_init(self):
        self.statusbar.showMessage('请打开馈线柜日志文件')
        """样式表"""
        self.setWindowOpacity(0.99)  # 窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.left_widget.setStyleSheet('''
            QFrame#left_widget{
            background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(132, 77, 181, 255), stop:1 rgba(102, 130, 237, 255));
            border-top-left-radius:10px;
            border-top-right-radius:10px;
            border-bottom-left-radius:10px;
            border-bottom-right-radius:10px;
            }
            QPushButton{
            border:none;
            background-color:none;
            color:white;}
            QPushButton#left_label{
            border:none;
            border-bottom:2px solid white;
            font-size:18px;
            font-weight:700;
            font-family:"等线"}
            QPushButton#left_button:hover{
            border-left:4px solid white;
            font-weight:700}''')
        self.display_select.setStyleSheet('''
            QTextEdit{
            color:#000000;
            background-color:#F5F5F5;
            border:1px solid gray;
            width:300px;}''')
        self.menubar.setStyleSheet('''
            menu_F:hover{
            background-color:#4B6EAF;}''')
        self.statusbar.setStyleSheet('''
            background-color:#FFFFFF;''')
        self.main_widget.setStyleSheet('''
            background-color:#FFFFFF;''')

    def style_incoming(self):
        """样式表"""
        self.setWindowOpacity(0.99)  # 窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.left_widget.setStyleSheet('''
            QFrame#left_widget{
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
            QComboBox#left_combobox{border: 1px;
            border-color: darkgray;
            border-style: solid;}
            QComboBox#left_combobox:down-arrow{image:url(icon/svgs/regular/arrow2.svg);}
            QComboBox#left_combobox:drop-down{
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;}''')
        self.display_select.setStyleSheet('''
            QTextEdit{
            color:#000000;
            background-color:#F5F5F5;
            border:1px solid gray;
            width:300px;}''')
        self.menubar.setStyleSheet('''
            menu_F:hover{
            background-color:#4B6EAF;}''')
        self.statusbar.setStyleSheet('''
            background-color:#FFFFFF;''')
        self.main_widget.setStyleSheet('''
            background-color:#FFFFFF;''')

    def clear(self):
        self.display_source.clear()
        self.display_result.clear()

    def save_file(self):
        try:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '打开', 'C:\\', 'Text Files (*.txt)')
            f = open(path, mode='w', encoding='utf-8')
            f.write(str(self.display_select.toPlainText()))
            f.close()
            self.statusbar.showMessage('已保存至' + path, msecs=700)
        except:
            pass

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
        except:
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
        try:
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
        except:
            pass

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
            html = '<body background-color: #0033FF>' + self.display_select.toHtml() + \
                   '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time + \
                   '</h2><hr>' + result_str + '</body>'
        else:
            html = '<body background-color: #0033FF>' + self.display_select.toHtml() + \
                   '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time \
                   + '</h2><hr style="height:1px;border:none;border-top:1px dashed #0066CC;">' \
                     '<p style="color:#1c1259;text-align:center;font-family:"等线"">无记录</p>' + '</body>'
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
        src = '<p style="text-align:left">' + src + '</p>'
        return src

    def open_edit(self):
        if self.display_select.isReadOnly():
            self.display_select.setReadOnly(False)  # 打开编辑，方便做笔记
            self.statusbar.showMessage("已开启编辑")
        else:
            self.display_select.setReadOnly(True)  # 关闭编辑
            self.statusbar.showMessage("已关闭编辑", msecs=200)