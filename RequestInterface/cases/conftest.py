'''
    会被pytest执行的自定义代码，不用引用这个包
    1.pytest_runtest_makereport 这个函数中的代码会在每个测试用例执行之前执行一次，并且会在测试用例执行之后执行两次；
      使用yield参数，让这个函数在测试用例执行前不执行；
      统计去重的思路：可以将测试结果放到字典中，利用字典的覆盖写入，记录的是最终的执行状态；
      如果重跑了多次，那么以最后执行的状态被记录
    2.夹具函数也写在这里，fixture函数，在测试用例执行时，可以将函数名作为参数传入，每次就会自动执行这个函数
      使用夹具函数，创建一个client对象
'''
import pytest
from core.util import *
from core.client import *
import requests

# DATA全局变量，在run（）中统计测试用例执行结果用
DATA = {'pass':0, 'failed':0, 'error':0, 'tatle':0}

# GLOBALS全局变量，读取xml中的global配置，先加载；也可以使用夹具函数将用例产生的结果，放入
GLOBALS = get_global_info()

# 设置一个返回GLOBALS的脚手架函数
@pytest.fixture()
def get():
    def __get(name):
        return GLOBALS[name]
    return __get

# 将获取的参数放入到全局变量
@pytest.fixture()
def set():
    def __set(name, value):
        GLOBALS[name] = value
    return __set


@pytest.hookimpl(hookwrapper=True ,tryfirst=True)
def pytest_runtest_makereport(item, call):
    # print('这是钩子执行结果')

    # 这个关键字将函数分批次执行，先拿到执行结果
    result = yield
    # print(result.get_result())
    data = result.get_result()
    if data.when == 'call':
        DATA['tatle'] += 1

        if data.outcome == 'passed':
            DATA['pass'] += 1
        elif data.outcome == 'failed':
            DATA['failed'] += 1
        elif data.outcome == 'error':
            DATA['error'] += 1


# 写一个脚手架函数，创建client对象
@pytest.fixture()
def api():
    def __api(name):
        dic = get_api(name=name)
        client = Client(url=dic['host'] + dic['url'], method=dic['method'], body_type=dic['body_type'])
        client.set_headers(dic['header'])
        return client
    return __api


# 另一种写脚手架函数的方式：创建一个client
@pytest.fixture()
def client(request):
    dic = get_api(request.module.__name__.split('.')[1][5:])
    c = Client(url=dic['host'] + dic['url'], method=dic['method'], body_type=dic['body_type'],
               params=dic['param'])
    c.set_headers(dic['header'])
    # c.set_bodies(dic['data'])
    return c

    # print(host+url,method)
    # print((requests.get(url=host+url)).text)


