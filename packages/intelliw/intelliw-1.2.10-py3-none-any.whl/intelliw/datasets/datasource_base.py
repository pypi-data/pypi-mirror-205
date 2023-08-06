#!/usr/bin/env python
# coding: utf-8
'''
Author: hexu
Date: 2021-10-14 14:54:05
LastEditTime: 2023-04-06 17:06:09
LastEditors: Hexu
Description: Algorithm -> DataSourceReader -> DataSource
FilePath: /iw-algo-fx/intelliw/datasets/datasource_base.py
'''
import datetime
from collections.abc import Iterable
from typing import Iterator

from intelliw.utils.logger import _get_framework_logger
from abc import ABCMeta, abstractmethod

logger = _get_framework_logger()


class DataSourceType:
    '''输入数据源类型'''
    # 大类
    EMPTY = 0   # 空
    TABLE_TYPE = 6  # 表格类别
    CV_TYPE = 7     # 图像类别
    NLP_TYPE = 8    # 文本类别

    # 子类
    REMOTE_CSV = 1  # 远程csv
    INTELLIV = 2  # 智能分析
    LOCAL_CSV = 3  # 本地 csv
    IW_IMAGE_DATA = 4  # 图片数据源
    IW_FACTORY_DATA = 5  # 数据工场数据集
    NLP_CORPORA = 21    # nlp语料
    SEMANTIC = 9   # 语义模型

    SQL = 998
    USER = 999


class AlgorithmsType:
    '''算法类型'''
    CLASSIFICATION = 3  # 分类算法
    TIME_SERIES = 9     # 时间序列


class DatasetType:
    TRAIN = 'train_set'
    VALID = 'validation_set'
    TEST = 'test_set'


class AbstractDataSource(metaclass=ABCMeta):
    """
    数据源定义
    """

    @abstractmethod
    def total(self) -> int:
        """
        获取数据源总数据条数
        :return: 数据源总数据条数
        """
        pass

    @abstractmethod
    def reader(self, page_size=100000, offset=0, limit=0, transform_function=None, dataset_type='train_set') -> Iterable:
        """
        获取一个读取该数据源的 iterator
        :param page_size: 读取分页大小
        :param offset:    开始读取的数据 index
        :param limit:     读取条数
        :param transform_function: 转换函数
        :return: 数据源 iterator
        """
        pass


class DataSourceReaderException(Exception):
    def ignore_stack(self):
        return True


class DataSourceWriterException(Exception):
    def ignore_stack(self):
        return True


class AbstractDataSourceWriter(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.table_columns = None

    @abstractmethod
    def write(self, data, starttime):
        pass


class EmptyDataSourceWriter(AbstractDataSourceWriter):

    def write(self, data, starttime=None):
        if starttime is None:
            starttime = datetime.datetime.now()
        logger.info(
            "datasource output: {}, starttime: {}".format(data, starttime))
        return {'status': 1}


class DataSourceEmpty(AbstractDataSource):
    """
    空数据源
    """

    def __init__(self):
        pass

    def total(self):
        return 0

    def reader(self, page_size=100000, offset=0, limit=0, transform_function=None) -> Iterable:
        return self.__Reader()

    class __Reader:
        def __iter__(self):
            return self

        def __next__(self):
            raise StopIteration


class DataSourceList(AbstractDataSource):
    """
    基于 list 的数据源，便于调试、单测
    """

    def __init__(self, meta: list, data: list):
        self.__meta = meta
        self.__data = data

    def total(self) -> int:
        return len(self.__data)

    def reader(self, page_size=10000, offset=0, limit=0, transform_function=None) -> Iterable:
        return self.__Reader(self.__meta, self.__data, page_size, offset, limit, transform_function)

    class __Reader(Iterator):

        def __init__(self, meta, data, page_size, offset, limit, transform_function):
            self.__meta = meta
            self.__data = data
            total = len(data)
            self.__limit = limit if limit < total - offset else total - offset
            self.__page_size = page_size if page_size < self.__limit else self.__limit
            if offset >= total:
                raise ValueError('offset is greater than total data')
            self.__index = offset  # start index, include
            self.__end_index = offset + self.__limit  # end index, not include
            self.__transform_function = transform_function

        def __iter__(self) -> Iterator:
            return self

        def __next__(self):
            if self.__index >= self.__end_index:
                raise StopIteration
            end = self.__index + self.__page_size
            if end > self.__end_index:
                end = self.__end_index
            result = {'meta': self.__meta,
                      'result': self.__data[self.__index: end]}
            self.__index = self.__index + self.__page_size
            if self.__transform_function is not None:
                result = self.__transform_function(result)
            return result
