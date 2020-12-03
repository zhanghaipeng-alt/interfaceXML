import requests
import jsonpath
import allure
import json
import traceback
'''
    使用allure装饰器：allure.step 可以在allure报告中将执行的函数作为步骤现实在执行结果中。
    allure.step()还可以添加文字注释，会在报告中展示。
    报告定制：使用allure的attach功能给结果添加报告详细步骤，在send函数中获取发送的详细信息和响应详情
    
    traceback包，可以捕捉到最近的代码的错误堆栈信息。有两种方法：
        print_exc()直接输出；format_exc()输出字符串
'''
# 添加收集的日志
infos = []

# 给每一天执行的测试用例增加log
def log(cid, result=None, info=None, error=None):
    for i in infos:
        if i['id'] == cid:
            # 测试用例执行结果存在，更新结果
            if result is not None:
                i['result'].append(result)
            if info is not None:
                i['log'].append(info)
            if error is not None:
                i['error'].append(error)
            break
    else:
        # 新增一条日志信息
        dic = {'id':cid, 'log':[], 'error':[]}
        if result is not  None:
            dic['result'] = result
        if info is not None:
            dic['log'].append(info)
        if error is not None:
            dic['error'].append(error)


# 写一个添加日志的装饰器
def add_log(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except:
            traceback.format_exc()
            args[0].flag += 1
            return None
        return res
    return wrapper


class Client(object):

    def __init__(self, url, method, body_type=None, timeout=3, params=None):
        self.url = url
        self.method = method
        self.body_type = body_type
        self.timeout = timeout
        self.headers = {}
        self.data = {}
        self.res = None
        self.params = params

        # 定义一个flag，统计测试用例执行的时候 检查点失败的次数
        self.flag = 0

    def set_header(self, key, value):
        self.headers['key'] = value

    def set_headers(self, data):
        if isinstance(data, dict):
            self.headers = data
        else:
            raise Exception('请求头必须以字典格式传递！')

    # 使用property装饰器，使用的时候可以直接调取。
    # @property
    # def set_headers(self):
    #     return self.set_headers()
    #
    # @property
    # def set_params(self):
    #     return self.params()


    def set_body(self, key, value):
        self.data['key'] = value

    def set_bodies(self, data):
        if isinstance(data, dict):
            self.data = data
        else:
            raise  Exception('正文必须以字典格式传递！')

    # 响应状态码获取验证
    @property
    @allure.step('获取响应状态码')
    def res_status_code(self):
        if self.res is not None:
            return  self.res.status_code
        else:
            print('响应内容为空，状态码获取失败！')
            return None

    # 获取响应时间
    @property
    @allure.step('获取响应时间')
    def res_times(self):
        if self.res is not None:
            return round(self.res.elapsed.total_seconds()* 1000)
        else:
            print('响应内容为空，未获取到响应时间')
            return None


    # 获取响应正文
    @property
    @allure.step
    def res_text(self):
        if self.res is not None:
            return  self.res.text
        else:
            print('响应内容为空！')
            return None

    # 获取响应内容
    @property
    @allure.step
    def res_content(self):
        if self.res is not None:
            return self.res.content
        else:
            print('响应内容为空！')
            return None

    # 获取响应头信息
    @property
    @allure.step('获取响应头')
    def res_headers(self):
        if self.res is not None:
            return self.res.headers
        else:
            print('响应内容为空，未获取头信息！')
            return None

    # 直接获取响应内容转成json格式
    @property
    @allure.step('获取响应正文json格式')
    def res_to_json(self):
        if  self.res is not None:
            return self.res.json()
        else:
            print('响应内容为空，未获取到正文！')
            return  None


    # 获取想用中某参数值,path为路径表达式
    def json_path_value(self, path):
        if not path.startswith('$.'):
            path = '$.' + path
        result = jsonpath.jsonpath(self.res_to_json, path)
        if result:
            return result[0]
        else:
            print(f'响应为空或者没有{path}字段')
            return None


    # 获取cookies
    @property
    @allure.step('获取cookies')
    def res_cookies(self):
        if self.res is not None:
            return self.res.cookies
        else:
            print('响应内容为空，未获取到cookies')
            return  None

    # 判断响应状态码是否是200
    @add_log
    @allure.step('响应状态码是否为200检查')
    def status_code_is_200(self):
        assert self.res.status_code == 200, '响应状态码错误，预期结果是200，实际结果是【{b}】！'.format(
            b=self.res.status_code)

    # 另外一种统计失败次数
    #     try:
    #         assert self.res.status_code == 200, '响应状态码错误，预期结果是200， 实际结果是【{b}】'.format(
    #             b=self.res.status_code
    #         )
    #     except:
    #         traceback.print_exc()
    #         self.flag += 1


    # 判断响应状态码
    @add_log
    @allure.step('响应状态码检查')
    def check_status_code(self, code):
        assert str(self.res.status_code) == str(code), '响应状态码检查失败，预期结果是【{a}】,实际结果是【{b}】'.format(
            a=code, b=self.res.status_code
        )

    # 判断响应时间
    @add_log
    @allure.step('响应时间是否小于预期值检查')
    def check_times_less_than(self, times):
        assert self.res_times < times, '响应时间检查失败，预期结果是小于【{a}】，实际结果是【{b}】'.format(
            a=times, b=self.res_times
        )

    # 判断响应内容全等
    @add_log
    @allure.step('响应结果等于预期值检查')
    def check_respond_equal(self, content):
        assert self.res_text == content, f'响应内容不一致。预期结果是【{content},实际结果是【{self.res_text}】】'

    # 判断响应内容包含某信息
    @add_log
    @allure.step('响应内容包含预期结果检查')
    def check_respond_in(self, content):
        assert content in self.res_text, f'响应内容不包含预期结果。预期结果是包含【{content}】，实际结果为【{self.res_text}】'

    # 判断头信息中含有某参数值
    @add_log
    @allure.step('响应头包含预期值检查')
    def check_headers_in(self, content):
        assert content in self.res_headers, f'响应头中不包含预期结果。预期结果包含【{content}】,实际结果为【{self.res_headers()}】'

    # 检查响应的中某参数值
    @add_log
    @allure.step('响应结果节点中包含预期值检查')
    def check_json_value(self, path, value):
        result = self.json_path_value(path=path)
        if result is not None:
            assert result == value, f'响应内容不一致。预期结果为{value},实际结果为{result}'
        else:
            assert False, f'响应字段获取失败：无{value}'



    # 发送请求
    @allure.step('发送请求')
    def send(self):
        if self.method == 'get':
            self.res = requests.get(url=self.url, headers=self.headers, params=self.params,
                                    timeout=self.timeout)

        elif self.method == 'post':
            if self.body_type == 'form':
                self.set_header('Content-Type', 'application/x-www-form-urlencoded')
                self.res = requests.post(url=self.url, headers=self.headers, params=self.params,
                                         data=self.data, timeout=self.timeout, allow_redirects=False)

            elif self.body_type == 'file':
                self.res = requests.post(url=self.url, headers=self.headers, params=self.params,
                                         files=self.data, timeout=self.timeout)

            elif self.body_type == 'json':
                self.set_header('Content-Type', 'application/json')
                self.res = requests.post(url=self.url, headers=self.headers, params=self.params,
                                         json=self.data, timeout=self.timeout)
            else:
                raise Exception('请求正文格式错误！')
        # 三个参数：内容，标题，格式
        # allure.attach(self.res.request.url, '请求地址', allure.attachment_type.TEXT)
        # allure.attach(self.method, '请求方法', allure.attachment_type.TEXT)
        # allure.attach(json.dumps(self.headers), '请求头', allure.attachment_type.TEXT)
        # allure.attach(json.dumps(self.data), '请求正文', allure.attachment_type.TEXT)
        # allure.attach(str(self.res_headers), '响应头', allure.attachment_type.TEXT)
        # allure.attach(str(self.res_status_code), '响应状态码', allure.attachment_type.TEXT)
        # allure.attach(str(self.res_text), '响应正文', allure.attachment_type.TEXT)
        # allure.attach(str(self.res_cookies), 'response cookies', allure.attachment_type.TEXT)


    class METHOD():
        POST = 'post'
        GET = 'get'

    class BODY_TYPE():
        FROM = 'form'
        FILES = 'file'
        JSON = 'json'

