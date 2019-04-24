"""IEC103规约分析"""
import re

text = """68 0C 0C 68 28 09 03 02 02 09 C2 91 80 FF 50 2D
           90 16"""
slave2master_function = {0: '确认', 1: '链路忙，未收到报文', 8: '以数据包响应请求帧', 9: '从站没有所召唤的数据', 11: '从站以链路状态响应主站请求'}
master2slave_funtion = {0: '复位通信单元', 3: '传送数据', 4: '传送数据', 7: '传送数据', 9: '召唤链路状态', 10: '召唤1级数据', 11: '召唤2级数据'}
pattern_variable = re.compile(
    r'^(?P<head>68 (?P<length>[0-9A-F]{2}) (?P=length) 68) (?P<code>[0-9A-F]{2}) (?P<addr>[0-9A-F]{2}) (?P<asdu>.+?) (?P<cs>[0-9A-F]{2}) 16$',
    flags=re.S)
pattern_fixed = re.compile(
    r'^(?P<head>10) (?P<code>[0-9A-F]{2}) (?P<addr>[0-9A-F]{2}) (?P<cs>[0-9A-F]{2}) (?P<end>16)$')
temp = re.match(pattern_variable, text)
print(temp['length'])


def control_analysis(control_message: str):
    """解析控制域"""
    content = ''
    temp = bin(int(control_message, 16))[2:]
    if temp[1]:
        content += '启动报文位（PRM）:1 ' + '主站 → 从站\n'
        if temp[2]:
            content += '帧计数位（FCB）:1\n'
        else:
            content += '帧计数位（FCB）:0\n'
        if temp[3]:
            content += '帧计数有效位（FCV）:1\n'
        else:
            content += '帧计数有效位（FCV）:0\n'
        function_code = int(temp[4:], 2)
        content += '功能码：' + str(function_code) + ' ' + master2slave_funtion[function_code]
    else:
        content += '启动报文位（PRM）:0 ' + '从站 → 主站'
        if temp[2]:
            content += '要求访问位（ACD）:1，从站有一级数据请求传送\n'
        else:
            content += '要求访问位（ACD）:0\n'
        if temp[3]:
            content += '数据流控制位（DFC）:1，从站缓冲区已满\n'
        else:
            content += '数据流控制位（DFC）:0，从站可以接受数据\n'
        function_code = int(temp[4:], 2)
        content += '功能码：' + str(function_code) + ' ' + slave2master_function[function_code]
    return content


def asdu_analysis(asdu_message: str):
    content = ''
    asdu = re.sub(re.compile(r'\s'), '', asdu_message)
    asdu_type = asdu[0:2]
    content += asdu_type + '    ASDU类型标识：' + str(int(asdu_type, 16))


def analysis(message: str):
    dict_message = {}
    message_type = ''
    if re.match(re.compile(r'^10'), message):
        message_type = '固定帧长报文'
        result = re.match(pattern_fixed, message)
        dict_message[result['head']] = '启动字符'
        dict_message[result['code']] = '控制域\n' + control_analysis(result['code'])
        dict_message[result['addr']] = '地址域'
        dict_message[result['cs']] = '代码和'
        dict_message[result['end']] = '结束字符'

    elif re.match(re.compile(r'^68'), message):
        message_type = '可变帧长报文'
        result = re.match(pattern_variable, message)
        dict_message[result['head']] = '启动帧 长度：' + str(int(result['length'], 16))
        dict_message[result['code']] = '控制域：' + control_analysis(result['code'])
        dict_message[result['addr']] = '地址域'
        '''asdu'''

        dict_message[result['cs']] = '代码和'
        dict_message[result['end']] = '结束字符'
    else:
        print(message)
    return message_type, dict_message


print(analysis(text))
