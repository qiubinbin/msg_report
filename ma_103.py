from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys, re
from MessageAnalysis import Ui_Analyzer


class Msg_als(QtWidgets.QMainWindow, Ui_Analyzer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_gif = QIcon('5-121204194114.gif')
        self.action_open.triggered.connect(self.openfile)
        self.pushButton_search.setIcon(self.button_gif)
        self.comboBox_date1.currentIndexChanged.connect(self.changetimelist1)
        self.comboBox_date2.currentIndexChanged.connect(self.changetimelist2)
        self.pushButton_search.clicked.connect(self.search)
        self.action_save.triggered.connect(self.savefile)

    def savefile(self):
        f = open('.\\result.txt', mode='w', encoding='utf-8')
        f.write(str(self.display_select.toPlainText()))
        f.close()

    def openfile(self):
        """文件打开显示并生成日期目录"""
        global dates_list
        dates_list = {}
        global file
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, '打开', 'C:\\Users\\qiubi\\Desktop',
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
            file_opened.close()
            # 显示初始日期，时间会自动调用更新函数
            self.comboBox_date1.addItems(dates_list.keys())
            self.comboBox_date2.addItems(dates_list.keys())
        except:
            pass

    def changetimelist1(self):
        """根据日期选择更新时间列表1"""
        self.comboBox_time1.clear()
        self.comboBox_time1.addItems(dates_list[self.comboBox_date1.currentText()])

    def changetimelist2(self):
        """根据日期选择更新时间列表2"""
        self.comboBox_time2.clear()
        self.comboBox_time2.addItems(dates_list[self.comboBox_date2.currentText()])

    def search(self):
        self.show216(self.comboBox_date1.currentText(), self.comboBox_time1.currentText())
        self.show216(self.comboBox_date2.currentText(), self.comboBox_time2.currentText())

    def show216(self, date, time):
        """根据时间选择显示216开关结果"""
        # self.display_select.clear()
        file_temp = open(file, mode='r', encoding='utf-8')
        file_opened = file_temp.read()
        pattern_str = date + ' ' + time + '\n' + r'(?P<content>.+?)(?P<date1>2019-\d+-\d+)'
        pattern_date = re.compile(pattern_str, flags=re.S)
        content_msg = re.search(pattern_date, file_opened)
        html_str = '<h1 color="#5ba19b" style="line-height:0.4px">' + date + ' ' + time + '</font>'
        self.display_select.append(html_str)
        src = content_msg['content'].strip()
        # 在时间段中查找216记录
        pattern_linematch_send1 = re.compile(r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+?)')
        pattern_linematch_send2 = re.compile(r'^\s')
        pattern_linematch_receive1 = re.compile(r'(?P<content_216>RX-.+?F0 A0 (?P<value>0[12]).+?)')
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

        if search_result:
            for line in search_result:
                line = self.word2html(line, 0)
                self.display_select.append(line)
                QtWidgets.QApplication.processEvents()
        else:
            self.display_select.append('<font color="#1c1259">无记录</font>')
        file_temp.close()
        self.display_select.setReadOnly(False)  # 打开编辑，方便做笔记

    def word2html(self, src, line):
        """'文本转标记"""
        if line == 1:
            src = src.replace('\n', '<br/>')
        src = src.replace('           ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
        src = src.replace('TX', '<font color="#db2d43"><strong>TX</strong></font>')
        src = src.replace('RX', '<font color="#00bd56"><strong>RX</strong></font>')
        src = '<p>' + src + '</p>'
        return src


app = QtWidgets.QApplication(sys.argv)
win = Msg_als()
win.show()
sys.exit(app.exec_())
