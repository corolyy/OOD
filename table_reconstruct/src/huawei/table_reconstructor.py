#!/usr/bin/env python
# -*-coding:utf-8-*-
from common.reconstruct_result import ReconstructResult
from common.column import Column


class TableReconstructor(object):
    def __init__(self):
        pass

    def do_reconstruct(self, index, count, sort, data):
        ''' 数据表打横业务

        :param index: 待打横的源列索引值; 索引值以0未起始索引值;
                    当指定多个源列时,以','分隔;必选参数
        :param count: 待打横的源列的枚举值上限值;大于等于0的整型值,0表示无限制;必选
        :param sort: 新增列集内部排序规则;(0|1),缺省未0,表示按列名字母升序排列输出;
                    1表示按枚举值的的频度升序排列;
        :param data: 数据源字符串,必选参数;格式:"列名1,列名2,...;类型1,类型2,...;
                    缺省值1,缺省值2,...;值,值,...;..."
        :return:
        '''
        result = ReconstructResult()
        # TODO
        return result
