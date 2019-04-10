from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys, re
from MessageAnalysis import Ui_Analyzer


class MsgAls(QtWidgets.QMainWindow, Ui_Analyzer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_gif = QIcon('5-121204194114.gif')
        self.pushButton_search.setIcon(self.button_gif)
        self.action_open.triggered.connect(self.openfile)
        self.comboBox_date.currentIndexChanged.connect(self.time_select_changed)
        self.comboBox_time.currentIndexChanged.connect(self.display_content)
        self.pushButton_search.clicked.connect(self.filter)

    def openfile(self):
        """文件打开时处理"""
        self.display_origin.clear()  # 清楚历史记录
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubin1\\Desktop',
                                                             'Text Files (*.txt)')
        self.statusbar.showMessage(file_path)
        try:
            file_generator = self.textfileload(file_path)
            # self.data = self.file_opened.read()#此语句影响运行速率
            for line in file_generator:
                self.display_origin.append(self.str2html(line))  # 显示源文件
                self.creat_date_list(line)
        except:
            pass

    def creat_date_list(self, file):
        """创建日期选项"""
        pattern_date = re.compile(r'(?P<date1>2019-\d+-\d+) (?P<date2>\d{2}:\d{2}:\d{2})')
        try:
            global dates  # 多处使用，设置为全局
            dates = re.findall(pattern_date, file)
            for date in dates:
                self.date_list.add(date[0])
            date_list_current = [self.comboBox_date.itemText(i) for i in range(self.comboBox_date.count())]
            for date in self.date_list:
                if date not in date_list_current:
                    self.comboBox_date.addItem(date)
        except:
            pass

    def time_select_changed(self, line):
        """根据日期显示时间选项"""
        self.comboBox_time.clear()
        time_list = [date[1] for date in dates if date[0] == self.comboBox_date.currentText()]
        self.comboBox_time.addItems(time_list)


    def display_content(self, line):
        """显示筛选结果"""
        self.display_select.clear()
        pattern_str = self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)'
        pattern_compile = re.compile(pattern_str, flags=re.S)
        html_str = '<font color="#e4508f">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        try:
            content_msg = re.search(pattern_compile, line)
            src = content_msg['content'].strip()
            src = self.str2html(src)
            self.display_select.append(src)
        except '':
            pass

    def filter(self):
        """显示搜索结果"""
        self.display_select.clear()
        pattern_date = re.compile(
            self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)',
            flags=re.S)
        content_msg = re.search(pattern_date, self.data)
        html_str = '<font color="#e4508f">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        src = content_msg['content'].strip()
        pattern_216 = re.compile(r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+\n.+\n)TX')
        record_216 = re.search(pattern_216, src).group('content_216').strip()
        result_216 = self.str2html(record_216)
        self.display_select.clear()
        self.display_select.setHtml(result_216)

    @staticmethod
    def str2html(src):
        """文本转标记"""
        src = src.replace('           ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')  # 处理空格
        src = src.replace('TX', '<font color="#ff3796"><strong>TX</strong></font>')
        src = src.replace('RX', '<font color="#00faac"><strong>RX</strong></font>')
        src = '<font>' + src + '</font>'
        return src

    @staticmethod
    def textfileload(path):
        """文件动态加载"""
        for line in open(path, mode='r', encoding='utf-8'):
            yield line


app = QtWidgets.QApplication(sys.argv)
win = MsgAls()
win.show()
sys.exit(app.exec_())
