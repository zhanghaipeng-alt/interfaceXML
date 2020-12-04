'''
    从CSV导入数据。
    为了让测试用例文件不用引Pytest包，也可以在这里引。
    fixure 夹具函数
'''
import csv
import pytest
import allure
import xml.etree.cElementTree as ET
import xlrd
# pytest.mark.parametrize，参数化装饰器函数，可实现接口字段参数化

data = pytest.mark.parametrize
feature = allure.feature
title = allure.title
order = pytest.mark.run
story = allure.story()

# 在文件中读取参数
def get_csv(filename):
    result = []
    with open('./data/' + filename, 'r', encoding='utf-8') as f:
        for i in csv.reader(f):
            result.append(i)

    return result

# 在文件中获取配置的测试用例
def get_cases():
    cases = []
    et = ET.ElementTree(file='./Config.xml')

    for i in et.findall('.//cases/*'):
        if i.attrib['run'] == '1':
            cases.append('./cases/test_{filename}.py::{casename}'.format(filename=i.tag.split('-')[0],
                                                                      casename=i.tag.split('-')[1]))
    return cases


# 获取配置文件中的接口模板信息
def get_api(name):
    et = ET.ElementTree(file='./Config.xml')
    dic = {}

    for i in et.findall('.//mould/' +name+'/*'):
        if i.tag == 'host':
            dic[i.tag] = i.text
        if i.tag == 'url':
            dic[i.tag] = i.text
        if i.tag == 'method':
            dic[i.tag] = i.text
        if i.tag == 'body_type':
            dic[i.tag] = i.text
        if i.tag == 'header':
            dic['header'] = {}
            for j in et.findall('.//mould/' +name+ '/header' + '/*'):
                dic[i.tag][j.tag] = j.text
        if i.tag == 'data':
            dic['data'] = {}
            for m in et.findall('.//mould/' +name+ '/data' + '/*'):
                dic[i.tag][m.tag] = m.text
        if i.tag == 'param':
            dic['param'] = {}
            for m in et.findall('.//mould/' +name+ '/param' + '/*'):
                dic[i.tag][m.tag] = m.text
    return dic

# 获取xml文件中的全局配置
def get_global_info():
    et = ET.ElementTree(file='./Config.xml')
    global_info = {}

    for i in et.findall('.//global/*'):
        global_info[i.tag] = i.text
    return global_info

# 从Excel中获取全局变量配置
def get_data_excel(filename):
    data = {}
    try:
        work_book = xlrd.open_workbook('/Users/zhanghaipeng/PycharmProjects/RequestInterface/suite.xlsx')
    except FileNotFoundError:
        raise Exception('没有找到文档')

    try:
        sheet = work_book.sheet_by_name(filename)
        for i in range(1, sheet.nrows):
            key = sheet.row_values(i)[0]
            value = sheet.row_values(i)[1]
            data[key] = value
        return data
    except xlrd.biffh.XLRDError:
        raise Exception('sheet页不存在')

# 以字典格式读取Excel中的数据
def get_dic_excel(filename):
    data = []
    try:
        work_book = xlrd.open_workbook('/Users/zhanghaipeng/PycharmProjects/RequestInterface/suite.xlsx')
    except FileNotFoundError:
        raise Exception('文档不存在')

    try:
        sheet = work_book.sheet_by_name(filename)
        headers = sheet.row_values(0)
        for i in range(1, sheet.nrows):
            dic = {}
            for index, value in enumerate(sheet.row_values(i)):
                dic[headers[index]] = value
            data.append(dic)
        return data
    except xlrd.biffh.XLRDError:
        raise Exception('sheet页不存在')



# if __name__ == '__main__':
#     # a = get_data_excel('全局变量')
#     c = get_dic_excel('测试用例')
#     print(c)

