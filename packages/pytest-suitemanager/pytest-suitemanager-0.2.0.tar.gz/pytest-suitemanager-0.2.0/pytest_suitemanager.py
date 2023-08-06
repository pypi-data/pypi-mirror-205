# -*- coding: utf-8 -*-
import glob
import itertools
import logging
import os
from typing import Dict, Text

import pytest
import yaml
from _pytest.main import Session


def run_testsuites(session) -> list:

    option = vars(session.config.option)
    suite_path = option.get('suite_path')
    case_path = option.get('case_path')
    file_or_dir = option.get('file_or_dir')
    root_path = str(session.path)
    # 获取测试用例list
    testcases_list = glob.glob(os.path.normpath(root_path + '/**/test_*.py'), recursive=True)

    # 生产将要运行的测试用例集合并返回
    scenario_list = []
    if suite_path:
        suites_path = glob.glob(os.path.normpath(root_path + f'/**/{suite_path}'), recursive=True)[0]
        testsuite_data = get_yaml(suites_path)
        for i in testsuite_data.get('testsuite'):
            features_path = glob.glob(os.path.normpath(root_path + f'/**/{i}.yaml'), recursive=True)[0]
            features_data = get_yaml(features_path)
            # 使用生成器表达式，避免在内存中生成无用数据
            selected_testcases = (j[1] for j in itertools.product(features_data.get('testcases'), testcases_list)
                                  if f"{j[0]}.py" in j[1])
            # 使用extend方法将多个元素一次添加到列表中
            scenario_list.extend(selected_testcases)
    elif case_path:
        features_path = glob.glob(os.path.normpath(root_path + f'/**/{case_path}'), recursive=True)[0]
        features_data = get_yaml(features_path)
        # 使用生成器表达式，避免在内存中生成无用数据
        selected_testcases = (j[1] for j in itertools.product(features_data.get('testcases'), testcases_list)
                              if f"{j[0]}.py" in j[1])
        # 使用extend方法将多个元素一次添加到列表中
        scenario_list.extend(selected_testcases)
    return scenario_list


def get_yaml(yaml_file: Text) -> Dict:
    """
    获取yaml中的数据
    :param yaml_file:
    :return:
    """
    try:
        with open(yaml_file, mode="rb") as stream:
            yaml_content = yaml.unsafe_load(stream)
            return yaml_content
    except yaml.YAMLError as ex:
        err_msg = f"YAMLError:\nfile: {yaml_file}\nerror: {ex}"
        logging.info(err_msg)
    except FileNotFoundError as ex:
        err_msg = f"FileNotFoundError:\nfile: {yaml_file}\nerror: {ex}"
        logging.error(err_msg)


def pytest_addoption(parser):
    """
    给pytest增加 自定义 命令行解析参数
    """
    group = parser.getgroup('suitemanager')
    group.addoption(
        "--suite-path",
        default=None,
        help="指定测试集"
    )
    group.addoption(
        "--case-path",
        default=None,
        help="指定测试集"
    )
    group.addoption(
        "--case-root-dir",
        default=None,
        help="指定测试集"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: Session):
    """
    加载yaml文件中得 测试用例
    :param session:
    :return:
    """
    option = vars(session.config.option)
    suite_path = option.get('suite_path')
    case_path = option.get('case_path')
    file_or_dir = option.get('file_or_dir')
    root_path = str(session.path)
    # 测试用例加载
    if suite_path and not file_or_dir:
        scenario_list = run_testsuites(session)
        session.config.args = scenario_list
