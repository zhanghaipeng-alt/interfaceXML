import subprocess
import time
import sys
# from dingtalkchatbot.chatbot import  DingtalkChatbot
from core.util import *
sys.path.append('/Users/zhanghaipeng/Documents/allure-2.13.3/bin')

import cases.conftest as cc

'''
    -s：展示print信息
    -k：分组
    
    使用pytest allure生成报告
'''
if __name__ == '__main__':
    # pytest.main(['./cases','-s','--html=./report/reprot.html'])

    # 加上一个时间戳
    tmp = time.strftime('%Y%m%d_%H:%M:%S', time.localtime(time.time()))
    # print(tmp)

    # 执行cases下所有测试用例
    pytest.main(['./cases', '-s', '--alluredir=./report/json', '--clean-alluredir'])

    # 按照测试用例名称执行cases下测试用例
    # pytest.main(['./cases/test_login.py::test_login02','./cases/test_login.py::test_login01', '-s', '--alluredir=./report/json', '--clean-alluredir'])


    #引用配置文件的写法
    # cmd = get_cases()
    # cmd.append('-s')
    # cmd.append('--alluredir=./report/json')
    # cmd.append('--clean-alluredir')
    # # 重跑次数为3，添加pytest-rerunfailure==9.0版本
    # cmd.append('--reruns=3')
    # # 添加重跑延时3s
    # cmd.append('--reruns-delay=3')
    # pytest.main(cmd)
    # time.sleep(3)

    # 创建一个定定机器人
    # xiaoding = DingtalkChatbot.post()

    # 使用命令行执行allure插件
    # subprocess.Popen('/Users/zhanghaipeng/Documents/allure-2.13.3/bin/allure generate ./report/json -o ./report/html/final'+tmp, shell=True)
    # os.popen('/Users/zhanghaipeng/Documents/allure-2.13.3/bin/allure generate ./report/json -o ./report/html/final')
    # print(cc.DATA)

