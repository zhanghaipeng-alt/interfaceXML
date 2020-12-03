from core.client import *
from core.util import *

'''
    使用测试用例的参数化：使用pytest中的装饰器函数pytest.mark.paramtrize(),
    使用方法如下：在需要做参数化的测试用例加上装饰器函数，参数列表为需要做参数分的参数；
    allure.feature()：模块名称
    allure.title()：测试用例的名称
    pytest.mark.run(order=1)：定义用例的执行顺序，数字越小，先执行。
    
'''
# data = [('test1', '123456', 302),
#         ('test3', '123456', 302),
#         ('test8', '123456', 200)]
# @pytest.mark.parametrize('username, password, code', get_csv('login.csv') )
# @allure.feature('模块名称：登录模块')
# @allure.title('测试用例名称：登录数据校验')
# @pytest.mark.run(order=1)

@data('username, password, code', get_csv('login.csv'))
@feature('模块：登录模块')
@title('用例名称：登录数据校验')
@order(1)
def test_login01(client, username, password, code):
    '''
    登录测试用例参数校验
    :return:
    ,allow_redirects=False
    '''
    host = 'http://140.143.171.176:9000'
    url = '/account/api/login/'
    data = {'username': username, 'password': password}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded',
    #            'Cookie': 'sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe'}
    # client = Client(url=host + url, method=Client.METHOD.POST, timeout=3,
    #                 body_type=Client.BODY_TYPE.FROM)
    # client.set_headers(headers)
    client.set_bodies(data=data)
    client.send()
    client.check_status_code(code=code)
    client.check_times_less_than(500)
    # client.check_headers_in('sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe')


    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {'username': 'teEst4', 'password': '123456'}
    # res = requests.post(url=host + url, headers=headers, data=data
    #                     , allow_redirects=False)
    # print(res.content)
    # # 添加检查点
    # assert res.status_code==200, '响应状态码非200'
    # # res.elapsed.seconds
    # # res.elapsed.total_seconds()


@feature('模块:登录模块')
@title('用例名称：登录用例demo')
def test_login02(client):
    '''
    密码错误
    :return:
    '''

    # host = 'http://140.143.171.176:9000'
    # url = '/account/api/login/'
    # data = {'username': 'test3', 'password': '12343356'}
    # headers = {'Content-Type': 'application/x-www-form-urlencoded',
    #            'Cookie': 'sessionid=270odmrrzzplem5aczgoxl5c1xvvxjbe'}

    # client = api('login')
    # client = Client(url=host + url, method=Client.METHOD.POST, timeout=3,
    #                 body_type=Client.BODY_TYPE.FROM)
    # client.set_headers(headers)
    # client.set_bodies(data=data)
    client.send()
    client.check_status_code(302)



# if __name__ == '__main__':
#     pytest.main()