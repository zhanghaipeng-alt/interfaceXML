import requests
from core.client import *
from core.util import *
import jsonpath
import json
import pytest
import pymysql
import xlrd
'''
    读Excel文件：
        1.openpyxl：可以读写Excel的任意版本，读取性能慢，Excel后台弹出；
        2.xlrd, xlwd：两个项目不是同一团队开发，xlrd读很好用，但是xlwd不能追加写，而且不能使用07以下版本；
        3.
'''

def demo():


    host = 'http://140.143.171.176:9000'
    url = '/account/api/login'

    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Cookie':'sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe'}
    data = {'username': 'test3', 'password': '123456'}
    res = requests.post(url='http://140.143.171.176:9000/account/api/login/', headers=headers, data=data
                        , allow_redirects=False)

    # res = requests.get(url='http://140.143.171.176:9000/login')
    print(res.headers, res.status_code, res.text,)
    # 添加检查点
    # assert res.status_code==200, '响应状态码非200'
    # res.elapsed.seconds
    # res.elapsed.total_seconds()


def demo1():
    host = 'http://140.143.171.176:9000'
    url = '/account/api/login/'
    data = {'username': 'test3', 'password': '123456'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Cookie': 'sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe'}
    client = Client(url=host+url, method=Client.METHOD.POST, timeout=3,
                    body_type=Client.BODY_TYPE.FROM)
    client.set_headers(headers)
    client.set_bodies(data=data)
    client.send()
    client.check_status_code(302)
    client.check_headers_in('sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe')


def demo3():
    url = 'http://140.143.171.176:9000/ticket/api/search/'
    headers = {'Cookie': 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64'}
    client = Client(url=url, method=Client.METHOD.GET)
    client.set_headers(headers)
    client.send()
    client.status_code_is_200()

def demo4():
    url = 'http://140.143.171.176:9000/ticket/api/order/'
    headers = {'Cookie': 'Cookie: sessionid=rg6qrevau94hrnmwwqy41cayk3rk4l9n; suid=4; sukey=ed05155fbf4f7a6373bc7c344be065bd',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {'id': '8'}

    client = Client(url=url, method=Client.METHOD.POST,body_type=Client.BODY_TYPE.FROM)
    client.set_headers(headers)
    client.set_bodies(data)
    client.send()
    client.status_code_is_200()
    client.check_json_value('code',0)



    # res = requests.post(url=url, headers=headers, data=data)
    # print(res.content)
    # assert res.status_code == 200, '返回状态码非200'
import xml.etree.cElementTree as ET
def xmlTest():
    et = ET.ElementTree(file='../config.xml')
    result = []
    for i in et.findall('.//cases/*'):
        if i.attrib['run'] == '1':
            result.append('./cases/test_{filename}::{casename}'.format(filename=i.tag.split('-')[0],
                                                               casename=i.tag.split('-')[1]))
    print(result)

def request_test():
    # param = {'page':1, 'limt':10}
    # c = requests.get(url='http://140.143.171.176:9000/ticket/api/search/', params=param)
    # print(c.request.url, c.headers)
    url = 'http://140.143.171.176:9000/ticket/api/search/'
    headers = {'Cookie' : 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64'}
    client = Client(url=url, method=Client.METHOD.GET)
    client.set_headers(headers)
    client.send()
    # client.res_status_code
    # client.res_headers
    # client.res_times
    # client.status_code_is_200
    print(client.res_to_json, client.res_status_code)
    client.check_json_value('data[0].number', 'Z172')



def mysqlTest():
    # 建立MySQL数据库连接
    connet = pymysql.connect(host='140.143.171.176', port=3306,
                    user='root', password='l#4@ssf7*', db='ticket')
    # 创建一个MySQL游标
    cursor = connet.cursor()

    # 查询SQL语句
    cursor.execute('select * from index_citys')

    # 获取查询结果,返回结果是一个多维元祖
    result = cursor.fetchall() # 获取全部结果
    print(result)

def excel():

    #word_book = xlrd.open_workbook('/Users/zhanghaipeng/PycharmProjects/RequestInterface/suite.xlsx')
    word_book = xlrd.open_workbook('./suite.xlsx')


    # 2.打开sheet页
    sheet = word_book.sheet_by_name('全局变量')
    # 3.获取行数，根据行数循环读取内容
    print(sheet.ncols, sheet.nrows)
    print(sheet.row_values(1))
    try:
        print(str(sheet.cell(1, 2)))
    except:
        print('单元格为空值')

    # 4.根据单元格位置，获取单元格内容，读取的单元格内容是有格式的；


def GetUglyNumber_Solution(index):
    if index < 1:
        return 0
    count = 1
    two_pointer = 0
    three_pointer = 0
    five_pointer = 0
    ugly_num = [1]
    while count != index:
        min_value = min(2 * ugly_num[two_pointer], 3 * ugly_num[three_pointer], 5 * ugly_num[five_pointer])
        ugly_num.append(min_value)
        count += 1
        if min_value == 2 * ugly_num[two_pointer]:
            two_pointer += 1
        if min_value == 3 * ugly_num[three_pointer]:
            three_pointer += 1
        if min_value == 5 * ugly_num[five_pointer]:
            five_pointer += 1
    return ugly_num[count - 1]

def testLoad():
    '''
    根据序列化和反序列的特性

    loads： 是将string转换为dict
    dumps： 是将dict转换为string
    load： 是将里json格式字符串转化为dict，读取文件
    dump： 是将dict类型转换为json格式字符串，存入文件
    :return:
    '''

    dic = {'a':'1111','b':'2222','c':'3333','d':'4444'}
    print(type(dic))

    str1 = json.dumps(dic)
    print(type(str1), str1)

    dic2 = json.loads(str1)
    print(type(dic2), dic2)


if __name__ == '__main__':
    testLoad()