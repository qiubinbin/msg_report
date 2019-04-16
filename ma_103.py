from PyQt5 import QtWidgets
import sys
import re
import collections
from MessageAnalysis import Ui_Analyzer


class Msg_als(QtWidgets.QMainWindow, Ui_Analyzer):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.edit = False  # 编辑状态
        self.action_open.triggered.connect(self.open_file)
        self.pushButton_note.clicked.connect(self.open_edit)
        self.pushButton_save.clicked.connect(self.save_file)
        self.comboBox_date1.currentIndexChanged.connect(self.change_timelist_1)
        self.comboBox_time1.currentIndexChanged.connect(self.change_datelist_2)
        self.comboBox_date2.currentIndexChanged.connect(self.change_timelist_2)
        self.pushButton_search.clicked.connect(self.search)
        self.action_save.triggered.connect(self.save_file)

    def save_file(self):
        f = open('.\\result.txt', mode='w', encoding='utf-8')
        f.write(str(self.display_select.toPlainText()))
        f.close()

    def open_file(self):
        """文件打开显示并生成日期目录"""
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
        """根据时间选择显示216开关结果"""
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

    def createhtml(self, list, date, time):
        result_str = ''
        if list:
            for item in list:
                result_str += (self.word2html(item, 0))
            html = '<body background="leaves.png">' + self.display_select.toHtml() + \
                   '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time + \
                   '</h2><hr>' + result_str + '</body>'
        else:
            html = '<body background="leaves.png">' + self.display_select.toHtml() + \
                   '<h2 style="color:#5ba19b;text-align:center">' + date + ' ' + time \
                   + '</h2><hr><p style="color:#1c1259;text-align:center">无记录</p>' + '</body>'
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
