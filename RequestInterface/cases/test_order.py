from core.client import *
from core.util import *

# @allure.feature('模块：订单模块')
# @allure.title('下单校验')
# @pytest.mark.run(order=3)
@feature('模块：订单模块')
@title('用例名称：下单校验')
@order(3)
def test_order01():
    '''
    下单成功
    :return:
    '''
    # url = 'http://140.143.171.176:9000/ticket/api/order'
    # headers = {'Cookie' : 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64',
    # 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    # data = {'id': '3'}
    # res = requests.post(url=url, headers=headers, data=data)
    # print(res.content)
    # assert res.status_code==200, '返回状态码非200'
    url = 'http://140.143.171.176:9000/ticket/api/order/'
    headers = {
        'Cookie': 'Cookie: sessionid=rg6qrevau94hrnmwwqy41cayk3rk4l9n; suid=4; sukey=ed05155fbf4f7a6373bc7c344be065bd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {'id': '8'}

    client = Client(url=url, method=Client.METHOD.POST, body_type=Client.BODY_TYPE.FROM)
    client.set_headers(headers)
    client.set_bodies(data)
    client.send()
    client.status_code_is_200()
    client.check_times_less_than(500)



# 使用脚手架函数的写法
@feature('模块：订单模块')
@title('用例名称：下单的脚手架函数写法')
def test_order02(client):
    headers = {
        'Cookie': 'Cookie: sessionid=rg6qrevau94hrnmwwqy41cayk3rk4l9n; suid=4; sukey=ed05155fbf4f7a6373bc7c344be065bd',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    data = {'id': '8'}

    client.set_headers(headers)
    client.set_bodies(data=data)
    client.send
    client.status_code_is_200
    client.check_times_less_than(500)