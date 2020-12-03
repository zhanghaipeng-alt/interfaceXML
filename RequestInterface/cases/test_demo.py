import pytest
from core.util import *
from core.client import *



# 夹具函数
# @pytest.fixture()
# def record_custom_data():
#
#     def __record_costom_data(name):
#         return {
#             'name' : name,
#             'orders' : []
#         }
#     return __record_costom_data

@feature('模块：demo模块')
@title('用例名称：demo测试')
def test_demo01(client, get, set):
    # headers = {'Cookie' : 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64'}
    # client.set_headers(headers)
    client.send()
    assert False
    client.res_status_code
    client.res_headers
    client.res_times
    client.status_code_is_200
    print(client.res_to_json)
    client.check_json_value('data[0].number', 'Z172')
    set('number', client.json_path_value('data[0].number'))
    print(get('number'))




