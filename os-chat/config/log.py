import logging
import logging.config as log_config
import time

from icecream import ic


def _prefix_time():
    return f"info | {time.strftime('%X')} | "


def setup_log():
    log_config.fileConfig(
        fname='config/log_config.ini',
        disable_existing_loggers=True,
    )

    _alog = logging.getLogger('app')

    def _info(s): return _alog.info(s)

    ic.configureOutput(
        prefix=_prefix_time,
        outputFunction=_info, includeContext=True,
    )


"""
Logging Config

# https://docs.python.org/3/library/logging.config.html

"""
