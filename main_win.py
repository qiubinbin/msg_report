"""主窗口"""
import collections
import configparser
import re

import paramiko
import qtawesome
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal

from IEC103 import analysis
from download_win import File_dowload, OpenTip
from feedback_win import FeedBack
from override import TextView, Button4Icon, WebView
from remote_login_win import Login
from setting_win import Setting


class File_copy(QtCore.QThread):
	mySignal = pyqtSignal(dict)

	def __init__(self, connect=None, statusbar=None):
		super().__init__()
		self.connect = connect
		self.statusbar = statusbar
		conf = configparser.ConfigParser()
		conf.read('configure.ini', 'utf-8')
		self.remote_path = conf.items('远程服务器地址', 'utf-8')[0][1]  # 远程服务器日志文件夹地址
		self.content = dict()

	def run(self):
		try:
			transport = paramiko.Transport((self.connect['host'], self.connect['port']))
			QtWidgets.QApplication.processEvents()
			transport.connect(username=self.connect['username'], password=self.connect['password'])
			sftp = paramiko.SFTPClient.from_transport(transport)
			remote_files = sftp.listdir(self.remote_path)  # 获取远程文件夹中的文件列表
			self.content['remote_path'] = self.remote_path
			self.content['filelist'] = remote_files
			self.content['transport'] = transport
			self.content['statusbar'] = self.statusbar
			self.mySignal.emit(self.content)

		except Exception as e:
			self.statusbar.showMessage(str(e))


class Msg_als(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.is_feeder = True
		self.feedwin = FeedBack()
		self.setting = Setting()
		self.login = Login()
		self.common_init()
		self.style_feeder()
		self.init_action_connect()
		self.setWindowIcon(QtGui.QIcon('icon/main_win.svg'))
		self.setWindowTitle('Message')

	def init_action_connect(self):
		self.action_open.triggered.connect(self.open_file)
		self.action_save.triggered.connect(self.save_file)
		self.action_open_remote.triggered.connect(self.remote)
		self.action_setting.triggered.connect(self.setting.show)
		self.action_feedback.triggered.connect(self.feedwin.show)
		self.feeder_cabin.triggered.connect(self.style_feeder)
		self.incoming_cabinet_201_202.triggered.connect(self.style_incoming)
		# self.pushButton_note.clicked.connect(self.open_edit)
		self.pushButton_save.clicked.connect(self.save_file)
		self.pushButton_search.clicked.connect(self.search)
		self.comboBox_date1.currentIndexChanged.connect(self.change_timelist_1)
		self.comboBox_time1.currentIndexChanged.connect(self.change_datelist_2)
		self.comboBox_date2.currentIndexChanged.connect(self.change_timelist_2)
		self.pushButton_clear.clicked.connect(self.clear)
		self.pushButton_execute.clicked.connect(self.execute)

	def common_init(self):
		"""初始化UI """
		"""菜单栏"""
		self.action_open = QtWidgets.QAction(qtawesome.icon('fa.folder-open-o', color="black"), '打开(O)')
		self.action_open.setShortcut('Ctrl+O')
		self.action_save = QtWidgets.QAction(qtawesome.icon('fa.save', color="black"), '保存(S)')
		self.action_save.setShortcut('Ctrl+S')
		self.action_open_remote = QtWidgets.QAction(qtawesome.icon('fa.ravelry', color="black"), '远程')
		self.action_open_remote.setShortcut('Ctrl+R')
		self.action_about = QtWidgets.QAction('关于')
		self.action_feedback = QtWidgets.QAction('反馈')
		self.incoming_cabinet_201_202 = QtWidgets.QAction(qtawesome.icon('fa.share'), '进线柜')
		self.feeder_cabin = QtWidgets.QAction(qtawesome.icon('fa.share'), '馈线柜')
		self.menubar = self.menuBar()
		self.menu_F = self.menubar.addMenu('文件')
		self.menu_F.addAction(self.action_open)
		self.menu_F.addAction(self.action_save)
		self.menu_F.addAction(self.action_open_remote)
		self.menu_P = self.menubar.addMenu('协议')
		self.menu_H = self.menubar.addMenu('帮助')
		self.action_setting = QtWidgets.QAction(qtawesome.icon('fa.cog', color='black'), '设置')
		self.menu_H.addAction(self.action_about)
		self.menu_H.addAction(self.action_feedback)
		self.menu_H.addAction(self.action_setting)
		self.protocol_103 = self.menu_P.addMenu(qtawesome.icon('fa.file-word-o', color='black'), '103协议')
		self.protocol_103.addAction(self.incoming_cabinet_201_202)
		self.protocol_103.addAction(self.feeder_cabin)
		# 设置菜单栏样式
		self.setStyleSheet('''
			QMenu{background:#F6F6F6;
			color:black;
			font-family:"微软雅黑"}
			QMenu:item:selected{
			background-color: #C9DEF5;}
			QMenuBar:item:selected{background-color: #F6F6F6;}''')
		"""状态栏"""
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setEnabled(True)
		self.statusbar.setObjectName("statusbar")
		self.statusbar_label = QtWidgets.QLabel()
		self.statusbar_label.setText('当前模式: 馈线柜')
		self.statusbar.addPermanentWidget(self.statusbar_label)
		self.setStatusBar(self.statusbar)
		# 设置状态栏样式
		self.statusbar_label.setStyleSheet('''
			font-family:"微软雅黑";
			font-size:11pd;
			font-weight:487;
			border:none;''')
		self.statusbar.setStyleSheet('''
			font-family:"微软雅黑";
			font-size:11pd;
			font-weight:487;
			background-color:#FFFFFF;
			border:none; ''')
		"""主窗口"""
		self.setWindowTitle('报文分析')
		# self.setWindowIcon(QIcon('images/icon.png'))
		self.setFixedSize(1000, 600)
		self.main_widget = QtWidgets.QWidget()
		self.main_layout = QtWidgets.QGridLayout()
		self.main_widget.setLayout(self.main_layout)
		"""左窗口"""
		self.left_widget = QtWidgets.QWidget()
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
		self.pushButton_search = QtWidgets.QPushButton(qtawesome.icon('fa.search', color='white', ), "搜索")
		self.pushButton_search.setObjectName('left_button_search')
		self.pushButton_note = QtWidgets.QPushButton(qtawesome.icon('fa.pencil', color='white'), "笔记")
		self.pushButton_note.setObjectName('left_button_note')
		self.pushButton_save = QtWidgets.QPushButton(qtawesome.icon('fa5s.save', color='white'), "保存")
		self.pushButton_save.setObjectName('left_button_save')
		self.comboBox_date1 = QtWidgets.QComboBox()
		self.comboBox_date1.setObjectName('left_combobox')
		self.comboBox_time1 = QtWidgets.QComboBox()
		self.comboBox_time1.setObjectName('left_combobox')
		self.begin_label = QtWidgets.QGroupBox('开始时间')
		self.begin_label_layout = QtWidgets.QVBoxLayout()
		self.begin_label.setLayout(self.begin_label_layout)
		self.begin_label_layout.addWidget(self.comboBox_date1, 0)
		self.begin_label_layout.addWidget(self.comboBox_time1, 1)
		self.comboBox_date2 = QtWidgets.QComboBox()
		self.comboBox_date2.setObjectName('left_combobox')
		self.comboBox_time2 = QtWidgets.QComboBox()
		self.comboBox_time2.setObjectName('left_combobox')
		self.end_label = QtWidgets.QGroupBox('结束时间')
		self.end_label_layout = QtWidgets.QVBoxLayout()
		self.end_label.setLayout(self.end_label_layout)
		self.end_label_layout.addWidget(self.comboBox_date2, 0)
		self.end_label_layout.addWidget(self.comboBox_time2, 1)
		self.transform_widget = QtWidgets.QWidget()
		self.transform_widget.setObjectName('transform_widget')
		self.transform_layout = QtWidgets.QGridLayout()
		self.transform_widget.setLayout(self.transform_layout)
		self.label_source = QtWidgets.QPushButton('源数据')
		self.label_source.setObjectName('label')
		self.label_protocol = QtWidgets.QPushButton('103规约')
		self.label_protocol.setObjectName('label')
		self.pushButton_execute = Button4Icon('fa.download')
		self.pushButton_execute.setObjectName('button_execute')
		self.pushButton_execute.setToolTip('分析')
		self.pushButton_clear = Button4Icon('fa.undo')
		self.pushButton_clear.setObjectName('button_clear')
		self.pushButton_clear.setToolTip('清空')
		self.display_source = TextView()
		self.display_source.setToolTip('请在此处输入数据源')
		self.display_result = TextView()
		self.display_result.setReadOnly(True)
		self.display_result.setToolTip('此处显示分析结果')
		"""给左窗口添加部件"""
		self.left_layout.addWidget(self.begin_label, 0)
		self.left_layout.addWidget(self.end_label, 3)
		self.left_layout.addStretch(6)
		self.left_layout.addWidget(self.pushButton_search, 6)
		self.left_layout.addWidget(self.pushButton_note, 7)
		self.left_layout.addWidget(self.pushButton_save, 8)
		"""给右窗口添加部件"""
		# self.display_select = TextView()
		# self.display_select.setReadOnly(True)
		self.display_select = WebView()
		self.right_layout.addWidget(self.display_select, 0, 2, 10, 6)
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
		self.widget_title.setStyleSheet('''
			background-color: #698FBF;border-bottom:none;
			border-top-left-radius:8px;border-top-right-radius:8px;''')
		self.label_source.setStyleSheet('''
			color:#FFFFFF;
			border:none;
			background-color:none;
			font:75 10pt "微软雅黑";''')
		self.label_protocol.setStyleSheet('''
			color:#FFFFFF;
			border:none;
			background-color:none;
			font:75 10pt "微软雅黑";''')
		self.display_result.setStyleSheet('''
			border:2px solid #698FBF;
			border-radius: 8px;''')
		self.display_source.setStyleSheet('''
			border:2px solid #698FBF;
			border-bottom-right-radius: 8px;
			border-bottom-left-radius: 8px;''')

	def style_incoming(self):
		self.is_feeder = False
		"""进线柜界面"""
		self.statusbar_label.setText('当前模式: 进线柜')
		self.statusbar.showMessage('请打开进线柜日志文件')
		"""样式表"""
		self.setWindowOpacity(0.99)  # 窗口透明度
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
		self.left_widget.setStyleSheet('''
			QWidget#left_widget{
			background-color:#FFFFFF;
			margin-top:10;
			margin-bottom:10;}
			QGroupBox{
			background-color:#F3F2F8;
			border-radius: 8px;
			height:100px;
			font-family:"微软雅黑";}
			QPushButton{
			border:none;
			background-color:none;
			color:#000000;}
			QPushButton#left_label{
			border:none;
			border-bottom:2px solid white;
			font-size:18px;
			font-weight:700;
			font-family:"黑体";}
			QPushButton#left_button_search{
			background-color:#52A088;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_search:hover{
			background-color:#437868;}
			QPushButton#left_button_note{
			background-color:#8C72BC;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_note:hover{
			background-color:#756397;}
			QPushButton#left_button_save{
			background-color:#E5676B;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_save:hover{
			background-color:#C05D60;}
			QComboBox#left_combobox{
			font-family:"STHeiti-Light";
			border: 1px solid gray;
			border-radius: 1px;
			padding: 1px 18px 1px 3px;
			border-color: darkgray;}
			QComboBox#left_combobox{
			font-family:"Consolas";}
			QComboBox#left_combobox::down-arrow{image:url(icon/arrow2_feeder.svg);}
			QComboBox#left_combobox::drop-down{
			subcontrol-origin: padding;
			subcontrol-position: top right;
			width: 15px;
			border-left-width: 1px;
			border-left-color: darkgray;
			border-top-right-radius: 1px;
			border-bottom-right-radius: 1px;}
			''')
		self.transform_widget.setStyleSheet('''
			QFrame#title{background-color: #232F3F;
			border-top-left-radius:1px;border-top-right-radius:1px;}
			QPushButton{border:none;background-color:none;color:#F49900;font:75 10pt "微软雅黑";}''')
		self.display_select.setStyleSheet('''
			QTextEdit{
			color:#000000;
			border-radius:8px;
			border:2px solid #698FBF;
			font:75 8pt "Consolas";
			width:300px;}''')
		self.menubar.setStyleSheet('''
			menu_F:hover{
			background-color:#4B6EAF;}''')
		self.statusbar.setStyleSheet('''
			background-color:#FFFFFF;''')
		self.main_widget.setStyleSheet('''
			background-color:#FFFFFF;''')

	def style_feeder(self):
		"""馈线柜样式表"""
		self.is_feeder = True
		self.statusbar_label.setText('当前模式: 馈线柜')
		self.statusbar.showMessage('请打开馈线柜日志文件')
		self.setWindowOpacity(0.99)  # 窗口透明度
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
		self.left_widget.setStyleSheet('''
			QWidget#left_widget{
			background-color:#FFFFFF;
			margin-top:10;
			margin-bottom:10;}
			QGroupBox{
			background-color:#F3F2F8;
			border-radius: 8px;
			height:100px;
			font-family:"微软雅黑";}
			QPushButton{
			border:none;
			background-color:none;
			color:#000000;}
			QPushButton#left_label{
			border:none;
			border-bottom:2px solid white;
			font-size:18px;
			font-weight:700;
			font-family:"黑体";}
			QPushButton#left_button_search{
			background-color:#52A088;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_search:hover{
			background-color:#437868;}
			QPushButton#left_button_note{
			background-color:#8C72BC;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_note:hover{
			background-color:#756397;}
			QPushButton#left_button_save{
			background-color:#E5676B;
			color:#FFFFFF;
			font-family:"STHeiti-Light";
			font-weight:700;
			border-radius: 8px;
			height:30px;}
			QPushButton#left_button_save:hover{
			background-color:#C05D60;}
			QComboBox#left_combobox{
			font-family:"STHeiti-Light";
			border: 1px solid gray;
			border-radius: 1px;
			padding: 1px 18px 1px 3px;
			border-color: darkgray;}
			QComboBox#left_combobox{
			font-family:"Consolas";}
			QComboBox#left_combobox::down-arrow{image:url(icon/arrow2_feeder.svg);}
			QComboBox#left_combobox::drop-down{
			subcontrol-origin: padding;
			subcontrol-position: top right;
			width: 15px;
			border-left-width: 1px;
			border-left-color: darkgray;
			border-top-right-radius: 1px;
			border-bottom-right-radius: 1px;}
			''')
		self.transform_widget.setStyleSheet('''
				QFrame#title{background-color: #232F3F;
				border-top-left-radius:1px;border-top-right-radius:1px;}
				QPushButton{border:none;background-color:none;color:#F49900;font:75 10pt "微软雅黑";}''')
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
			path, _ = QtWidgets.QFileDialog.getSaveFileName(self, '打开', 'C:\\', 'Html Files (*.html)')
			f = open(path, mode='w', encoding='utf-8')
			f.write(self.display_select.temp_html)
			f.close()
			self.statusbar.showMessage('已保存至' + path, msecs=700)
		except:
			pass

	def open_file(self, connect=None):
		"""文件打开显示并生成日期目录 """
		"""重新打开文件重置窗口"""
		self.display_select.clear()
		self.display_source.clear()
		self.display_result.clear()
		self.comboBox_date1.clear()
		self.comboBox_time1.clear()
		self.comboBox_date2.clear()
		self.comboBox_time2.clear()
		global dates_list
		dates_list = collections.OrderedDict()
		# print(connect)
		global file
		if connect:
			file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', connect, 'Text Files (*.txt)')
		else:
			file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubi\\Desktop',
			                                                'Text Files (*.txt)')
		self.statusbar.showMessage("已打开 " + file)
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
		self.display_select.clear()  # 搜索前重置缓存
		"""按时间段进行搜索"""
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
		search_result = []
		"""标志组"""
		pre_signal1 = False
		pre_signal2 = False
		pre_signal3 = False
		rev_signal1 = False
		rev_signal2 = False
		rev_signal3 = False
		temp_message = []  # 临时保存一级召唤数据
		if self.is_feeder:
			"""馈线柜"""
			for line in src.split('\n'):
				"""-------------------------遥控过程-------------------------"""
				"""匹配TX(F0 A0)-RX对"""
				if re.match(re.compile(r'TX-.+?F0 A0 .+?'), line):
					pre_signal1 = True
					search_result.append(line)
				elif pre_signal1 & bool(re.match(re.compile(r'^\s'), line)):
					search_result.append(line)
				elif pre_signal1 & bool(re.match(re.compile(r'^RX'), line)):
					search_result.append(line)
					pre_signal1 = False
					rev_signal1 = True
				elif rev_signal1 & bool(re.match(re.compile(r'^\s'), line)):
					search_result.append(line)
					rev_signal1 = False
				else:
					rev_signal1 = False
				"""匹配二级数据-RX召唤"""
				if re.match(re.compile(r'^TX-.+?10 \dA.+?16'), line):
					temp_message.append(line)
					pre_signal2 = True
				elif pre_signal2:
					if re.match(re.compile(r'^RX-.+?F0 A0 .+?'), line):
						temp_message.append(line)
						rev_signal2 = True
					else:
						temp_message.clear()  # 匹配失败，清空
					pre_signal2 = False
				elif rev_signal2:
					if re.match(re.compile(r'^\s'), line):
						temp_message.append(line)
					search_result += temp_message
					temp_message.clear()
					rev_signal2 = False
			"""-------------------------遥信过程-------------------------"""
			for line in src.split('\n'):
				"""断路器分或合位"""
				if re.match(re.compile(r'^TX-.+?10 \dA.+?16'), line):
					temp_message.append(line)
					pre_signal3 = True
				elif pre_signal3:
					if re.match(re.compile(r'^RX-.+?C2 1[BC] 02.+?'), line):
						temp_message.append(line)
						rev_signal3 = True
					else:
						temp_message.clear()  # 匹配失败，清空
					pre_signal3 = False
				elif rev_signal3:
					if re.match(re.compile(r'^\s'), line):
						temp_message.append(line)
					search_result += temp_message
					temp_message = []
					rev_signal3 = False
		else:
			"""进线柜"""
			"""-------------------------遥控过程-------------------------"""
			for line in src.split('\n'):
				"""匹配TX(F0 A0)-RX控制对"""
				if re.match(re.compile(r'TX-.+?B2 4[67] 02.+?'), line):
					pre_signal1 = True
					search_result.append(line)
				elif pre_signal1 & bool(re.match(re.compile(r'^\s'), line)):
					search_result.append(line)
				elif pre_signal1 & bool(re.match(re.compile(r'^RX'), line)):
					search_result.append(line)
					pre_signal1 = False
					rev_signal1 = True
				elif rev_signal1 & bool(re.match(re.compile(r'^\s'), line)):
					search_result.append(line)
					rev_signal1 = False
				else:
					rev_signal1 = False
				"""匹配二级数据-RX召唤"""
				if re.match(re.compile(r'^TX-.+?10 \dA.+?16'), line):
					temp_message.append(line)
					pre_signal2 = True
				elif pre_signal2:
					if re.match(re.compile(r'^RX-.+?B2 4[67] 02.+?'), line):
						temp_message.append(line)
						rev_signal2 = True
					else:
						temp_message.clear()  # 匹配失败，清空
					pre_signal2 = False
				elif rev_signal2:
					if re.match(re.compile(r'^\s'), line):
						temp_message.append(line)
					search_result += temp_message
					rev_signal2 = False
				"""-------------------------遥信过程-------------------------"""
				for line in src.split('\n'):
					"""断路器分或合位"""
					if re.match(re.compile(r'^TX-.+?10 \dA.+?16'), line):
						temp_message.append(line)
						pre_signal3 = True
					elif pre_signal3:
						if re.match(re.compile(r'^RX-.+?B2 6[45] 02.+?'), line):
							temp_message.append(line)
							rev_signal3 = True
						else:
							temp_message.clear()  # 匹配失败，清空
						pre_signal3 = False
					elif rev_signal3:
						if re.match(re.compile(r'^\s'), line):
							temp_message.append(line)
						search_result += temp_message
						temp_message.clear()
						rev_signal3 = False
		self.display_select.sethtml(self.createhtml(search_result, date, time))
		QtWidgets.QApplication.processEvents()
		file_temp.close()

	def createhtml(self, result_list, date, time):
		result_str = ''
		if result_list:
			for index, item in enumerate(result_list):
				if index == 0:
					result_str += self.word2html(item, 0)
				else:
					result_str += ('<br/>' + self.word2html(item, 0))
			html = '<div style="font-size:12;background-color:#5E98AC;border-radius:8px;padding:0px 2px 2px 4px">' + '<h2 style="color:#FFFFFF">' + date + ' ' + time + '</h2><p style="line-height:17px;text-align:left;color:#FFFFFF;font-family:"Courier New"">' + result_str + '</p></div>'
		else:
			html = '<div style="font-size:12;background-color:#DB6E8E;border-radius:8px;padding:0px 2px 2px 4px">' + '<h2 style="color:#FFFFFF">' + date + ' ' + time + '</h2><p style="text-align:left;color:#FFFFFF;text-align:center;font-family:"微软雅黑"">无记录</p>' + '</div>'
		return html

	def word2html(self, src, line):
		"""'文本转标记"""
		if line == 1:
			src = src.replace('\n', '<br/>')
		src = src.replace(
			'           ',
			'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
		src = src.replace(
			'TX', '<font style="font-weight:bold;">TX</font>')
		src = src.replace(
			'RX', '<font style="font-weight:bold;">RX</font>')
		return src

	def open_edit(self):
		if self.display_select.isReadOnly():
			self.display_select.setReadOnly(False)  # 打开编辑，方便做笔记
			self.statusbar.showMessage("已开启编辑")
		else:
			self.display_select.setReadOnly(True)  # 关闭编辑
			self.statusbar.showMessage("已关闭编辑", msecs=200)

	def execute(self):
		"""不用区分进线柜或者馈线柜"""
		message = self.display_source.toPlainText().strip()
		temp_result = None
		try:
			temp_result = analysis(message)
		except Exception as e:
			self.statusbar.showMessage('报文格式不完整！')
		self.display_result.setHtml(temp_result[0])
		for m in temp_result[1].keys():
			self.display_result.append(
				m + temp_result[1][m] + '<hr style=" height:2px;border:none;border-top:2px dotted #008080;" />')

	def remote(self):
		self.login.show()
		self.login.mySignal.connect(self.showlogin)

	def showlogin(self, connect):
		self.thread_file = File_copy(connect, self.statusbar)
		self.thread_file.start()
		self.thread_file.mySignal.connect(self.showdownload)

	def showdownload(self, connect):
		"""下载窗口处理"""
		self.widget = File_dowload(connect['remote_path'], connect['filelist'], connect['transport'],
		                           connect['statusbar'])
		self.widget.show()
		self.widget.mySignal.connect(self.tip)

	def tip(self, connect):
		"""提示窗处理"""
		self.tip_win = OpenTip()
		self.tip_win.show()
		self.path_download = connect
		self.tip_win.mySignal.connect(self.open_file1)

	def open_file1(self, connect):
		"""提示窗信号处理"""
		if connect:
			self.open_file(self.path_download)
		else:
			pass
