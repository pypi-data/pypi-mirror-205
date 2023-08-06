#!/usr/bin/python3.8+
# -*- coding:utf-8 -*-
from datetime import datetime, timedelta, timezone

# 北京时区
Beijing = timezone(timedelta(hours=8))


def now():
    return datetime.now(tz=Beijing)


def datetime2str(dt: datetime, fmt='%Y-%m-%d %H:%M:%S'):
    """
    datetime格式转字符串日期
    :param dt:
    :param fmt
    :return: "2023-04-18 18:54:59"
    """
    if dt.tzinfo:
        dt = dt.astimezone(Beijing)
    return dt.strftime(fmt)
