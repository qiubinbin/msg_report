from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import sys, re, time
from MessageAnalysis import Ui_Analyzer


class Msg_als(QtWidgets.QMainWindow, Ui_Analyzer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_gif = QIcon('5-121204194114.gif')
        self.action_open.triggered.connect(self.openfile)
        self.pushButton_search.setIcon(self.button_gif)
        self.comboBox_date.currentIndexChanged.connect(self.changetimelist)
        self.comboBox_date.currentIndexChanged.connect(self.showbydateortime)
        self.comboBox_time.currentIndexChanged.connect(self.showbydateortime)
        self.pushButton_search.clicked.connect(self.show216)
        self.action_save.triggered.connect(self.savefile)

    def savefile(self):
        f = open('.\\result.txt', mode='w', encoding='utf-8')
        f.write(str(self.display_select.toPlainText()))
        f.close()

    def openfile(self):
        """文件打开显示并生成日期目录"""
        self.display_origin.clear()
        global dates_list
        dates_list = {}
        global file
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubin1\\Desktop',
                                                        'Text Files (*.txt)')
        self.statusbar.showMessage(file)
        pattern_date = re.compile(r'(?P<date1>2019-\d+-\d+) (?P<date2>\d{2}:\d{2}:\d{2})')
        try:
            file_opened = open(file, mode='r', encoding='utf-8')
            for line in file_opened:
                dates = re.findall(pattern_date, line)
                if dates:
                    if dates[0][0] not in dates_list.keys():
                        dates_list[dates[0][0]] = [dates[0][1]]
                    else:
                        dates_list[dates[0][0]].append(dates[0][1])
                line_html = self.word2html(line, 0)
                self.display_origin.append(line_html)
                QtWidgets.QApplication.processEvents()  # 刷新页面,阻止卡顿
            file_opened.close()
            # 显示初始日期，时间会自动调用更新函数
            self.comboBox_date.clear()
            self.comboBox_date.addItems(dates_list.keys())
        except:
            pass

    def changetimelist(self):
        """根据日期选择更新时间列表"""
        self.comboBox_time.clear()
        self.comboBox_time.addItems(dates_list[self.comboBox_date.currentText()])

    def showbydateortime(self):
        """根据日期选择显示结果"""
        self.display_select.clear()
        pattern_str = self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content = open(file, mode='r', encoding='utf-8')
        content_msg = re.search(pattern_date, content.read())
        html_str = '<font color="#5ba19b">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        try:
            src = content_msg['content'].strip()
            src = src.replace('\n', '<br/>')
            src = self.word2html(src, 1)
            self.display_select.append(src.strip())
            content.close()
        except:
            pass

    def show216(self):
        """根据时间选择显示216开关结果"""
        self.display_select.clear()
        file_temp = open(file, mode='r', encoding='utf-8')
        file_opened = file_temp.read()
        pattern_str = self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + r'(?P<content>.+)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content_msg = re.search(pattern_date, file_opened)
        html_str = '<font color="#5ba19b">' + self.comboBox_date.currentText() + ' ' + self.comboBox_time.currentText() + '</font>'
        self.display_select.append(html_str)
        src = content_msg['content'].strip()
        # 在时间段中查找216记录
        pattern_216 = re.compile(r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+\n.+\n)TX')
        record_216 = re.search(pattern_216, src).group('content_216').strip()
        result_216 = self.word2html(record_216, 1)
        self.display_select.append(result_216)
        file_temp.close()
        self.display_select.setReadOnly(False)  # 打开编辑，方便做笔记

    def word2html(self, src, line):
        """'文本转标记"""
        if line == 1:
            src = src.replace('\n', '<br/>')
        src = src.replace('           ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        src = src.replace('TX', '<font color="#db2d43"><strong>TX</strong></font>')
        src = src.replace('RX', '<font color="#00bd56"><strong>RX</strong></font>')
        src = '<font>' + src + '</font>'
        return src


app = QtWidgets.QApplication(sys.argv)
win = Msg_als()
win.show()
sys.exit(app.exec_())
