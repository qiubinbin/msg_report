from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys, re
from MessageAnalysis import Ui_Analyzer


class Msg_als(QtWidgets.QMainWindow, Ui_Analyzer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_gif = QIcon('5-121204194114.gif')
        self.pushButton_search.setIcon(self.button_gif)
        self.action_open.triggered.connect(self.openfile)
        self.comboBox_date.currentIndexChanged.connect(self.select_changed)
        self.comboBox_time.currentIndexChanged.connect(self.text_color)
        self.pushButton_search.clicked.connect(self.filter)

    def openfile(self):
        '''文件打开时处理'''
        self.display_origin.clear()
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubi\\Desktop',
                                                        'Text Files (*.txt)')
        self.statusbar.showMessage(file)
        try:
            self.file_opened = open(file, mode='r', encoding='utf-8')
            self.data = self.file_opened.read()
            self.gen_menu(self.data)
            # print(self.word(self.data))
            self.display_origin.setHtml(self.word(self.data))
        except:
            pass

    def gen_menu(self, file):
        '''创建日期选项'''
        pattern_date = re.compile(r'(?P<date1>2019-\d+-\d+) (?P<date2>\d{2}:\d{2}:\d{2})')
        self.dates = re.findall(pattern_date, file)
        dates_list = {date[0] for date in self.dates}
        self.comboBox_date.addItems(dates_list)

    def select_changed(self):
        '''跟随日期变化，创建时间选项'''
        self.comboBox_time.clear()
        time_list = [date[1] for date in self.dates if date[0] == self.comboBox_date.currentText()]
        self.comboBox_time.addItems(time_list)
        self.text_color()

    def text_color(self):
        '''文本处理'''
        self.display_select.clear()
        pattern_str = self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content_msg = re.search(pattern_date, self.data)
        html_str = '<font color="#e4508f">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        try:
            src = content_msg['content'].strip()
            src = self.word(src)
            self.display_select.append(src.strip())
        except:
            pass

    def filter(self):
        """获取控制记录"""
        self.display_select.clear()
        pattern_str = self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content_msg = re.search(pattern_date, self.data)
        html_str = '<font color="#e4508f">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        src = content_msg['content'].strip()
        pattern_216 = re.compile(r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+\n.+\n)TX')
        record_216 = re.search(pattern_216, src).group('content_216').strip()
        result_216 = self.word(record_216)
        self.display_select.clear()
        self.display_select.setHtml(result_216)

    def word(self, src):
        '''文本转标记'''
        src = src.replace('\n', '<br/>')
        src = src.replace('           ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        src = src.replace('TX', '<font color="#ff3796"><strong>TX</strong></font><font>')
        src = src.replace('RX', '</font><font color="#00faac"><strong>RX</strong></font>')
        return src


app = QtWidgets.QApplication(sys.argv)
win = Msg_als()
win.show()
sys.exit(app.exec_())
