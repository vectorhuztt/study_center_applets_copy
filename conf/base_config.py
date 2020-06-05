#!/usr/bin/env python
# code:UTF-8
# @Author  : SUN FEIFEI
import os


class GetVariable(object):
    """参数化文档"""
    PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), p))  # 获取当前路径
    # 数据库信息
    # =====  dev ======

    TEST_VERSION = 'dev'
    HOST = '172.17.0.200'
    USER_NAME = 'director'
    PASSWORD = 'r0#pX8^V'
    DB = 'learning'
    # DB = "b_vanthink_core"

    # ==== Test =====
    # TEST_VERSION = 'test'
    # HOST = '172.17.0.16'
    # USER_NAME = 'tmp'
    # PASSWORD = 'mysql#0056'
    # DB = "b_vanthink_online"

    # 测试报告存放路径
    REPORT_ROOT = 'storges/test_report'

    # 以下为 devices.py 配置信息
    PACKAGE = 'com.tencent.mm.apk'

    ID_TYPE = 'com.tencent.mm:id/'
    # case统计 配置信息
    SUIT_PATH = 'app'
    CASE_INFO = [
        ('app/passion_applets/test_cases', "test003*.py")
    ]
    # 以下为 appium_server.py 配置信息
    SERVER_URL = 'http://127.0.0.1:%s/wd/hub/status'
    SERVER_LOG = 'appium_server_port_%s.log'
    KILL = 'taskkill /PID %d /F'

    # 做题情况统计 Excel表格存放路径
    EXCEL_PATH = 'storges/games_result_info.xlsx'
