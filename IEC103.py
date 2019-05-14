"""IEC103规约分析"""
import collections
import re
import configparser

conf = configparser.ConfigParser()
conf.read('configure.ini', 'utf-8')
control_dict = {
    '馈线柜断路器分FUN': conf.items('馈线柜断路器分')[0][1],
    '馈线柜断路器分INF': conf.items('馈线柜断路器分')[1][1],
    '馈线柜断路器分有效值': conf.items('馈线柜断路器分')[2][1],
    '馈线柜断路器合FUN': conf.items('馈线柜断路器合')[0][1],
    '馈线柜断路器合INF': conf.items('馈线柜断路器合')[1][1],
    '馈线柜断路器合有效值': conf.items('馈线柜断路器合')[2][1],
    '进线柜断路器分FUN': conf.items('进线柜断路器分')[0][1],
    '进线柜断路器分INF': conf.items('进线柜断路器分')[1][1],
    '进线柜断路器分有效值': conf.items('进线柜断路器分')[2][1],
    '进线柜断路器合FUN': conf.items('进线柜断路器合')[0][1],
    '进线柜断路器合INF': conf.items('进线柜断路器合')[1][1],
    '进线柜断路器合有效值': conf.items('进线柜断路器合')[2][1],
}
date_type = {
    1: '带时标的报文',
    2: '具有相对时间的带时标报文',
    3: '被测值I',
    4: '具有相对时间的带时标的被测值',
    5: '标识',
    6: '时间同步',
    7: '总召唤',
    8: '总召唤终止',
    9: '被测值II',
    10: '通用分类数据',
    11: '通用标识',
    20: '一般命令',
    21: '通用命令',
    23: '被记录的扰动表',
    24: '扰动数据传输的命令',
    25: '扰动数据传输的认可',
    26: '准备传送扰动数据',
    27: '准备传送一个通道',
    28: '准备传送带标志的状态变位',
    29: '传送带标志的状态变位',
    30: '传送扰动值',
    31: '传送结束',
}
slave2master_function = {0: '确认',
                         1: '链路忙，未收到报文',
                         8: '以数据包响应请求帧',
                         9: '从站没有所召唤的数据',
                         11: '从站以链路状态响应主站请求'}
master2slave_function = {0: '复位通信单元',
                         3: '传送数据',
                         4: '传送数据',
                         7: '传送数据',
                         9: '召唤链路状态',
                         10: '召唤1级数据',
                         11: '召唤2级数据'}
master2slave_transform = {8: '时间同步',
                          9: '总召启动',
                          12: '未知传送原因',
                          20: '一般命令',
                          31: '扰动数据的传输',
                          40: '通用分类写命令',
                          42: '通用分类读命令'}
slave2master_transform = {1: '突发报文',
                          2: '循环传送',
                          3: '复位帧计算',
                          4: '复位通信单元',
                          5: '启动',
                          6: '电源合上',
                          7: '测试模式',
                          8: '时间同步',
                          9: '总召唤',
                          10: '总召唤终止',
                          11: '当地操作',
                          12: '远方操作',
                          20: '命令的肯定认可',
                          21: '命令的否定认可',
                          31: '扰动数据的传送',
                          40: '通用分类写命令的肯定认可',
                          41: '通用分类写命令的否定认可',
                          42: '通用分类读命令的肯定认可',
                          43: '通用分类读命令的否定认可',
                          44: '通用分类写确认'}
pattern_variable = re.compile(
    r'^(?P<head>68 (?P<length>[0-9A-F]{2}) (?P=length) 68) (?P<code>[0-9A-F]{2}) (?P<addr>[0-9A-F]{2}) (?P<asdu>.+?) (?P<cs>[0-9A-F]{2}) (?P<end>16)$',
    flags=re.S)
pattern_fixed = re.compile(
    r'^(?P<head>10) (?P<code>[0-9A-F]{2}) (?P<addr>[0-9A-F]{2}) (?P<cs>[0-9A-F]{2}) (?P<end>16)$', flags=re.S)


def control_analysis(control_message: str):
    """解析控制域"""
    content = ''
    temp = '{:08b}'.format(int(control_message, 16))
    if int(temp[1]):
        content += '&nbsp;&nbsp;&nbsp;启动报文位(PRM）:1 ' + '主站 → 从站<br>'
        if temp[2]:
            content += '&nbsp;&nbsp;&nbsp;帧计数位(FCB):1<br>'
        else:
            content += '&nbsp;&nbsp;&nbsp;帧计数位(FCB):0<br>'
        if int(temp[3]):
            content += '&nbsp;&nbsp;&nbsp;帧计数有效位(FCV):1<br>'
        else:
            content += '&nbsp;&nbsp;&nbsp;帧计数有效位(FCV):0<br>'
        function_code = int(temp[4:], 2)
        content += '&nbsp;&nbsp;&nbsp;功能码:' + str(function_code) + ' ' + master2slave_function[function_code]
    else:
        content += '&nbsp;&nbsp;&nbsp;启动报文位(PRM):0 ' + '从站 → 主站<br>'
        if int(temp[2]):
            content += '&nbsp;&nbsp;&nbsp;要求访问位(ACD):1，从站有一级数据请求传送<br>'
        else:
            content += '&nbsp;&nbsp;&nbsp;要求访问位(ACD):0<br>'
        if int(temp[3]):
            content += '&nbsp;&nbsp;&nbsp;数据流控制位(DFC):1，从站缓冲区已满<br>'
        else:
            content += '&nbsp;&nbsp;&nbsp;数据流控制位(DFC):0，从站可以接受数据<br>'
        function_code = int(temp[4:], 2)
        content += '&nbsp;&nbsp;&nbsp;功能码:' + str(function_code) + ' ' + slave2master_function[function_code]
    return content


def asdu_analysis(asdu_message: str, control_message: str):
    transform_direction = int('{:08b}'.format(int(control_message, 16))[1])
    content_asdu = ''
    asdu = re.sub(re.compile(r'\s'), '', asdu_message)
    asdu_type = asdu[0:2]
    if int(asdu_type, 16) in date_type.keys():
        content_asdu += '<br>' + asdu_type + '&nbsp;&nbsp;ASDU类型标识:' + date_type[int(asdu_type, 16)] + '<br>'
    else:
        content_asdu += '<br>' + asdu_type + '&nbsp;&nbsp;ASDU类型标识:未知标识(' + str(int(asdu_type, 16)) + ')<br>'
    asdu_vsq = str('{:08b}'.format(int(asdu[2:4], 16)))
    if int(asdu_vsq[0]):
        content_asdu += asdu[
                        2:4] + '&nbsp;&nbsp;可变结构限定词:<br>&nbsp;&nbsp;&nbsp;SQ=1 顺序(如:首地址,数据1,数据2···)<br>&nbsp;&nbsp;&nbsp;信息数目:' + str(
            int(asdu_vsq[1:], 2)) + '<br>'
    else:
        content_asdu += asdu[
                        2:4] + '&nbsp;&nbsp;可变结构限定词:<br>&nbsp;&nbsp;&nbsp;SQ=0 非顺序(如:地址1,数据1,地址2···)<br>&nbsp;&nbsp;&nbsp;信息数目:' + str(
            int(asdu_vsq[1:], 2)) + '<br>'
    if transform_direction:
        content_asdu += asdu[4:6] + '&nbsp;&nbsp;传送原因:' + master2slave_transform[int(asdu[4:6], 16)] + '<br>'
    else:
        content_asdu += asdu[4:6] + '&nbsp;&nbsp;传送原因:' + slave2master_transform[int(asdu[4:6], 16)] + '<br>'
    content_asdu += asdu[6:8] + '&nbsp;&nbsp;应用服务数据单元公共地址:' + str(int(asdu[6:8], 16)) + '<br>'
    content_asdu += asdu[8:10] + '&nbsp;&nbsp;功能类型:' + str(int(asdu[8:10], 16)) + '<br>'
    content_asdu += asdu[10:12] + '&nbsp;&nbsp;信息序号:' + str(int(asdu[10:12], 16)) + '<br>'
    if (asdu[8:10] == control_dict['馈线柜断路器分FUN']) & (asdu[10:12] == control_dict['馈线柜断路器分INF']) & (
            asdu[12:14] == control_dict['馈线柜断路器分有效值']):
        content_asdu += asdu[12:14] + '&nbsp;馈线柜断路器分闸控制'
    elif (asdu[8:10] == control_dict['馈线柜断路器合FUN']) & (asdu[10:12] == control_dict['馈线柜断路器合INF']) & (
            asdu[12:14] == ['馈线柜断路器合有效值']):
        content_asdu += asdu[12:14] + '&nbsp;馈线柜断路器合闸控制'
    elif (asdu[8:10] == control_dict['进线柜断路器分FUN']) & (asdu[10:12] == control_dict['进线柜断路器分INF']) & (
            asdu[12:14] == ['进线柜断路器分有效值']):
        content_asdu += asdu[12:14] + '&nbsp;进线柜断路器分闸控制'
    elif (asdu[8:10] == control_dict['进线柜断路器合FUN']) & (asdu[10:12] == control_dict['进线柜断路器合INF']) & (
            asdu[12:14] == ['进线柜断路器合有效值']):
        content_asdu += asdu[12:14] + '&nbsp;进线柜断路器合闸控制'
    if int(asdu_type, 16) == 1:
        """处理带时标的报文"""
        content_asdu += asdu[14:16] + '&nbsp;&nbsp;毫秒(低):' + str(int(asdu[14:16], 16) / 1000)
        content_asdu += asdu[16:18] + '&nbsp;&nbsp;毫秒(高):' + str(int(asdu[16:18], 16) / 1000)
        content_asdu += asdu[18:20] + '&nbsp;&nbsp;分钟:' + str(int(asdu[18:20], 16))
        content_asdu += asdu[20:22] + '&nbsp;&nbsp;小时:' + str(int(asdu[20:22], 16))
        content_asdu += asdu[22:24] + '&nbsp;&nbsp;附加信息SIN:' + str(int(asdu[22:24], 16))
    # TODO
    # 其他类型未在PSCADA看到，暂不分析

    return content_asdu


def analysis(message: str):
    """报文分析"""
    dict_message = collections.OrderedDict()
    message_type = ''
    if re.match(re.compile(r'^10'), message):
        message_type += '&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;' \
                        '固定帧长报文' \
                        '&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;<hr>'
        result = re.match(pattern_fixed, message)
        dict_message[result['head']] = '&nbsp;&nbsp;&nbsp;启动字符'
        dict_message[result['code']] = '&nbsp;&nbsp;控制域<br>' + control_analysis(
            result['code'])
        dict_message[result['addr']] = '&nbsp;&nbsp;地址域'
        dict_message[result['cs']] = '&nbsp;&nbsp;代码和'
        dict_message[result['end']] = '&nbsp;&nbsp;结束字符'

    elif re.match(re.compile(r'^68'), message):
        message_type += '&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;' \
                        '可变帧长报文' \
                        '&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;&#9107;<hr>'
        result = re.match(pattern_variable, message)
        dict_message[result[
            'head']] = '&nbsp;&nbsp;&nbsp;启动帧<br>&nbsp;&nbsp;&nbsp;' + '启动字符:68<br>&nbsp;&nbsp;&nbsp;' + '长度:' + str(
            int(result['length'], 16))
        dict_message[result['code']] = '&nbsp;&nbsp;控制域<br>' + control_analysis(result['code'])
        dict_message[result['addr']] = '&nbsp;&nbsp;地址域'
        dict_message[re.sub(re.compile(r'\s'), ' ', result['asdu']).strip()] = '  链路用户数据' + asdu_analysis(
            result['asdu'], result['code'])
        dict_message[result['cs']] = '&nbsp;&nbsp;代码和'
        dict_message[result['end']] = '&nbsp;&nbsp;结束字符'
    return message_type, dict_message


if __name__ == '__main__':
    text = """10 7B 09 84 16"""
    temp = analysis(text)
    print(temp[0])
    for m in temp[1].keys():
        print(m, temp[1][m])
