# -*- coding: utf-8 -*-
import glob
import itertools
import logging
import os
from typing import Text, Dict

import pytest
import yaml
from _pytest.main import Session

from utils import run_testsuites


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
    file_or_dir = option.get('file_or_dir')
    root_path = str(session.path)

    # 测试用例加载
    if suite_path and not file_or_dir:
        scenario_list = run_testsuites(root_path, suite_path)
        session.config.args = scenario_list
