import logging
from dataclasses import dataclass
from logging import *
from pathlib import Path

import pytest
from icecream import ic

from .log import setup_log

setup_log()

alog = getLogger('app')

rootLog = 'root.log'
appLog = 'app.log'


@dataclass(slots=True)
class Testcase:
    level: int  # Union[INFO, DEBUG, WARN, ERROR, CRITICAL]
    content: str


test_cases = [
    Testcase(DEBUG, 'Hiro-debug'),
    Testcase(INFO, 'Hiro-info'),
    Testcase(WARN, 'Hiro-warn'),
    Testcase(ERROR, 'Hiro-error'),
    Testcase(CRITICAL, 'Hiro-critical'),
]

level_map_files = {
    10: 'debug',
    20: 'info',
    30: 'warn',
    40: 'error',
    50: 'critical',
}


def assert_tokens_in_log(log_file: str | Path, *tokens: str):
    with open(f'logs/{log_file}', 'r+') as f1:
        lines = f1.readlines()
        assert len(lines) != 0
        last_line = lines[-1].strip()
        for token in tokens:
            assert token in last_line


@pytest.mark.run(order=1)
def test_root():
    testcase = test_root.__name__

    logging.info(testcase)
    assert_tokens_in_log(rootLog, testcase)


@pytest.mark.run(order=2)
def test_app():
    testcase = test_app.__name__

    ic(testcase)

    assert_tokens_in_log(appLog, testcase)

# @pytest.mark.run(order=2)
# @pytest.mark.parametrize("testcase", test_cases)
# def test_logs(testcase: Testcase):
#     level = testcase.level
#     cnt = testcase.content
#     log(level, cnt)
#
#     log_file = level_map_files[level]
#
#     with open(f'logs/{log_file}.log') as f1:
#         lines = f1.readlines()
#         assert len(lines) > 0
#         last_line = lines[-1].strip()
#         assert cnt in last_line
#
#
# @pytest.mark.no_cache
# @pytest.mark.run(order=1)
# @pytest.mark.parametrize("testcase", test_cases)
# def test_app_logs(testcase: Testcase):
#     level = testcase.level
#     cnt = f"app{testcase.content}"
#     ignored_levels = []
#
#     if level in ignored_levels: return
#
#     alog.log(level, cnt)
#
#     if level is INFO:
#         log_file = "app"
#     else:
#         log_file = f"app_{level_map_files[level]}"
#
#     with open(f'logs/{log_file}.log') as f1:
#         lines = f1.readlines()
#         assert len(lines) > 0
#         last_line = lines[-1].strip()
#         assert cnt in last_line
