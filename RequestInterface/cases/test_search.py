from core.client import *
from core.util import *


# @allure.feature('模块：车次查询')
# @allure.title('用例名称：车次查询全量')
# @pytest.mark.run(order=2)
@feature('模块：车次查询')
@title('用例名称：车次查询全量')
@order(2)
def test_search01(client):
    '''
    查询票务成功
    :return:
    '''
    # url = 'http://140.143.171.176:9000/ticket/api/search/'
    # headers = {'Cookie' : 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64'}
    # client = Client(url=url, method=Client.METHOD.GET)
    # client = api('search')
    client.send()
    client.status_code_is_200()
    client.check_times_less_than(500)

    # res = requests.get(url=url, headers=headers,params={'page':1, 'limit':10})
    # print(res.content)
    # print(res.text)
    # assert res.status_code==200, '返回状态码非200'



