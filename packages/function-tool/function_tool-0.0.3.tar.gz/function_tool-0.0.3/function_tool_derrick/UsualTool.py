# -*- coding: utf-8 -*-
# @Time     : 2023/4/17 12:51
# @Author   : Long-Long Qiu
# @FileName : UsualTool.py
# @Product  : PyCharm
# import packages
import time
from enum import Enum

"""
与日期和时间相关的功能
"""
class TimestampType(Enum):
    """
    时间戳类型：枚举
    """
    SECONDS = 0 # 秒
    MILLISECOND = 1 # 毫秒


class DateTimeTool(object):

    @classmethod
    def timestamp2time(cls, ts: int=int(time.time()), formatter: str="%Y-%m-%d %H:%M:%S", tsType: TimestampType=TimestampType.SECONDS, transfer: bool=False) -> str:
        """
        时间戳转换为指定格式的时间字符串
        :param ts: 待转换的时间戳
        :param formatter: 要转换的时间字符串格式
        :param tsType: 待转换时间戳类型(枚举，秒或毫秒)
        :param transfer: 由于有些机器不能识别当前所在时区，若设置此参数为True，则会转换成东八区时间
        :return: 指定格式的字符串
        """

        if tsType == TimestampType.MILLISECOND:
            ts //= 1000

        if transfer:
            timeArray = time.localtime(ts + 8 * 60 * 60)
        else:
            timeArray = time.localtime(ts)
        otherStyleTime = time.strftime(formatter, timeArray)

        return otherStyleTime

    @classmethod
    def time2timestamp(cls, timeStr: str, formatter: str="%Y-%m-%d %H:%M:%S", tsType: TimestampType=TimestampType.SECONDS, transfer: bool=False) -> int:
        """
        时间字符串转换为时间戳
        :param timeStr: 待转换时间字符串
        :param formatter: 待转换时间字符串的格式
        :param tsType: 要转换的时间戳类型(枚举，秒或毫秒)
        :param transfer: 由于有些机器不能识别当前所在时区，若设置此参数为True，则会转换成东八区时间
        :return: 指定类型的时间戳
        """

        timeArray = time.strptime(timeStr, formatter)
        # 转换为时间戳
        timeStamp = int(time.mktime(timeArray))

        if transfer:
            timeStamp = timeStamp - 8 * 60 * 60

        if tsType == TimestampType.MILLISECOND:
            return timeStamp * 1000
        return timeStamp

    @classmethod
    def get_range_of_date_by_str(cls, date_str: str, formatter: str='%Y-%m-%d', tsType: TimestampType=TimestampType.SECONDS) -> list:
        """
        计算给定时间所在日期的时间戳范围
        :param date_str: 给定的随时间/日期字符串
        :param formatter: date_str对应的格式
        :param tsType: 需要返回的时间戳类型
        :return: [ts_start, ts_end]
        """

        # 1. 转日期字符串格式
        ts = cls.time2timestamp(date_str, formatter=formatter)
        f_date = cls.timestamp2time(ts, formatter="%Y-%m-%d")

        # 2. 获取时间戳范围
        ts_begin = cls.time2timestamp(f"{f_date} 00:00:00")
        ts_end = cls.time2timestamp(f"{f_date} 23:59:59")

        if tsType == TimestampType.SECONDS:
            return [ts_begin, ts_end]
        else:
            return [ts_begin * 1000, ts_end * 1000 + 999]
