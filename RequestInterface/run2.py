'''
    使用读取Excel方式，重新编写框架，不使用pytest单元测试框架和allture出报告；
    1.读取全局配置，放到全局变量中
    2.读取接口模板信息，拼接参数，创建client对象
    3.拼接请求参数，发送请求，接收响应信息；
    4.添加检查点
'''
from core.util import *
from core.client import *
# 提取Excel表格中主要配置信息
DATA = get_data_excel('全局变量')
TEMPLES = get_dic_excel('接口模板')
cases = get_dic_excel('测试用例')
info = []
def run_cases():
    for index, case in enumerate(cases):
        if case.get('是否运行') != 0:
            cid = case.get('用例编号')
            template_name = case.get('模板名称')
            depends = case.get('关联表达式（用例编号=参数路径=临时变量名）')
            params = case.get('参数')
            data = case.get('数据引用')
            checks1 = case.get('响应内容校验1')
            checks2 = case.get('响应内容校验2')
            checks3 = case.get('响应内容校验3')
            status = case.get('响应状态码')

            if cid:
                if template_name:
                    for T in TEMPLES:
                        if T.get('接口名称') == template_name:
                            url = T.get('地址')
                            method = T.get('方法类型')
                            body_type = T.get('参数类型')
                            hearders = T.get('请求头', '')

                            #判断头信息
                            if hearders:
                                try:
                                    hearders = json.loads(hearders)
                                except:
                                    info.append({'id': cid, 'result': 'skip', 'log': ['请求头数据格式错误！']})
                                    continue

                            # 拼接client对象
                            if url and method and body_type:
                                # 创建client对象
                                if body_type == '标准表单':
                                    body_type = 'form'
                                elif body_type == 'JSON':
                                    body_type = 'json'
                                elif body_type == '复合表单':
                                    body_type = 'file'
                                client = Client(url=DATA.get('base_url', '') + url, method=method, body_type=body_type)
                                client.set_headers(hearders)

                                if params:
                                    # 转化params
                                    try:
                                        params = json.loads(params)
                                    except:
                                        info.append({'id': cid, 'result': 'skip', 'log': ['正文参数格式错误']})

                                    if method == 'POST':
                                        client.set_bodies(params)
                                    elif method == 'GET':
                                        client.params = params

                                    client.send

                                    # 添加检查点
                                    if status:
                                        client.check_status_code(int(status))
                                    else:
                                        client.status_code_is_200

                                    if checks1:
                                        check_list = checks1.split(',')
                                        if check_list[0] == '响应时间':
                                            client.check_times_less_than(int(check_list[1]))
                                        elif check_list[0] == '响应包含':
                                            client.check_respond_in(check_list[1])
                                        elif check_list[0] == '响应等于':
                                            client.check_respond_equal(check_list[1])
                                        elif check_list[0] == '节点响应':
                                            client.check_json_value(check_list[1], check_list[2])
                                        elif check_list[0] == '响应头包含':
                                            client.check_headers_in(check_list[1])
                                        else:
                                            print('不支持的检查点格式')
                                else:
                                    info.append({'id':cid, 'result':'skip', 'log':['正文参数格式错误']})
                            else:
                                info.append({'id':cid, 'result':'skip', 'log':['接口模板数据错误。']})
                            continue
                    else:
                        info.append({'id':cid, 'result':'skip', 'log':['引用的接口模板不存在。']})
                        continue
                else:
                    info.append({'id':cid, 'result':'skip', 'log': ['模板名称为空。']})
                    continue
            else:
                info.append({'id':'', 'result':'skip', 'log':['第{index}行测试用例，标号为空值！'.format(
                    index=index+1
                )]})
                continue

        else:
            continue

def runcases_test():
    # print(cases)
    for index, case in enumerate(cases):
        if case.get('是否运行') == 1:
            cid = case.get('用例编号')
            template_name = case.get('模板名称')
            depends = case.get('关联表达式（用例编号=参数路径=临时变量名）')
            params = case.get('参数','')
            data = case.get('数据引用')
            checks1 = case.get('响应内容校验1')
            checks2 = case.get('响应内容校验2')
            checks3 = case.get('响应内容校验3')
            status = case.get('响应状态码')

            if cid:
                if template_name:
                    for T in TEMPLES:
                        # 获得接口模板中的内容
                        if T.get('接口名称') == template_name:
                            url = T.get('地址')
                            method = T.get('方法类型')
                            body_type = T.get('参数类型')
                            headers = T.get('请求头')

                            # 判断头信息
                            if headers:
                                try:
                                    headers = json.loads(headers)
                                except:
                                    info.append({'id': cid, 'result': 'skip', 'log': ['请求头数据格式错误！']})
                                    continue

                            # 拼接client对象
                            if url and method and body_type:
                                # 判断请求格式
                                if body_type == '标准表单':
                                    body_type = 'form'
                                elif body_type == 'JSON':
                                    body_type = 'json'
                                elif body_type == '复合表单':
                                    body_type == 'file'
                                client = Client(url=DATA.get('base_url', '') + url, method=method, body_type=body_type)
                                client.set_headers(headers)
                                # 添加参数
                                if params:
                                    try:
                                        params = json.loads(params)
                                        if method == 'get':
                                            client.params = params
                                        elif method == 'post':
                                            client.set_bodies(params)
                                    except:
                                        raise info.append({'id': cid, 'result': 'skip', 'log': ['测试用例中参数格式错误。']})
                                        continue
                                client.send()
                                # 添加检查点
                                if status == '' or int(status) == 200:
                                    client.status_code_is_200
                                else:
                                    info.append({'id': cid, 'result': 'skip', 'log': ['接口用例中响应状态码填写错误。']})

                                if checks1:
                                    check_list = checks1.split(',')
                                    if check_list[0] == '响应时间':
                                        client.check_times_less_than(int(check_list[1]))
                                    elif check_list[0] == '响应包含':
                                        client.check_respond_in(check_list[1])
                                    elif check_list[0] == '响应等于':
                                        client.check_respond_equal(check_list[1])
                                    elif check_list[0] == '节点响应':
                                        client.check_json_value(check_list[1], check_list[2])
                                    elif check_list[0] == '响应头包含':
                                        client.check_headers_in(check_list[1])
                                    else:
                                        info.append({'id': cid, 'result': 'skip', 'log': ['测试用例中检查点填写错误。']})

                                if checks2:
                                    check_list = checks2.split(',')
                                    if check_list[0] == '响应时间':
                                        client.check_times_less_than(int(check_list[1]))
                                    elif check_list[0] == '响应包含':
                                        client.check_respond_in(check_list[1])
                                    elif check_list[0] == '响应等于':
                                        client.check_respond_equal(check_list[1])
                                    elif check_list[0] == '节点响应':
                                        client.check_json_value(check_list[1], check_list[2])
                                    elif check_list[0] == '响应头包含':
                                        client.check_headers_in(check_list[1])
                                    else:
                                        info.append({'id': cid, 'result': 'skip', 'log': ['测试用例中检查点填写错误。']})

                                if checks3:
                                    check_list = checks3.split(',')
                                    # print(check_list)
                                    if check_list[0] == '响应时间':
                                        client.check_times_less_than(int(check_list[1]))
                                    elif check_list[0] == '响应包含':
                                        client.check_respond_in(check_list[1])
                                    elif check_list[0] == '响应等于':
                                        client.check_respond_equal(check_list[1])
                                    elif check_list[0] == '节点响应':
                                        if check_list[2].isdigit():
                                            client.check_json_value(check_list[1], int(check_list[2]))
                                        else:
                                            client.check_json_value(check_list[1], check_list[2])
                                    elif check_list[0] == '响应头包含':
                                        client.check_headers_in(check_list[1])
                                    else:
                                        info.append({'id': cid, 'result': 'skip', 'log': ['测试用例中检查点填写错误。']})

                            else:
                                info.append({'id': cid, 'result': 'skip', 'log': ['接口模板中数据填写错误。']})
                        # else:
                        #     info.append({'id': cid, 'result': 'skip', 'log': ['测试用例中模板名称填写错误。']})
                        continue
                else:
                    info.append({'id': cid, 'result': 'skip', 'log': ['测试用例sheet中模板名称为空。']})
                    continue
            else:
                info.append({'id': '', 'result': 'skip', 'log': ['测试用例sheet中第{index}行测试用例，用例编号为空值！'.format(
                    index=index + 1
                )]})
                continue
        else:
            continue

    print(info)


def gtest():
    headers = {'Cookie': 'sessionid=ws80m521m0bnk7ndaivatkl67b3t0erk; suid=5; sukey=64552911e6d300d26b00639e5cdbbf64'}
    res = requests.get(url='http://140.143.171.176:9000/ticket/api/search/', headers=headers)
    print(res.status_code, res.content)



if __name__ == '__main__':
    runcases_test()
    # print(TEMPLES)
    # gtest




