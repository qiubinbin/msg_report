import re

# d = re.compile('2019-3-12 00:00:06'+r'(?P<content>.+)(?P<date1>2019-\d+-\d+)', flags=re.S)
# result = re.match(d, ''' 2019-3-12 00:00:06
# RX-34:390: 68 0C 0C 68 08 09 03 02 02 09 C2 91 70 FF F8 2A
#            05 16
# TX-34:400: 10 7B 09 84 16
#
# 2019-3-11 22:07:35''')
# print(re.sub(d,'<font color="#ff3796">TX</font>',''' 2019-3-12 00:00:06
# RX-34:390: 68 0C 0C 68 08 09 03 02 02 09 C2 91 70 FF F8 2A
#            05 16
# TX-34:400: 10 7B 09 84 16
#
# 2019-3-11 22:07:35'''))
pattern_216 = re.compile(r'(?P<content_216>TX-.+?F0 A0 (?P<value>0[12]).+\n.+\n)TX')
record_216=re.search(pattern_216,'''TX-28:437: 68 0A 0A 68 53 09 14 81 0C 09 F0 A0 01 00 97 16 //PSCADA下发216遥控分闸指令
RX-28:489: 10 00 09 09 16 //216返回确认帧
TX-28:499''')
print(record_216.group('content_216'))