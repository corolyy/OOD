#!/usr/bin/env python
# -*-coding:utf-8-*-
from common.reconstruct_result import ReconstructResult
from common.column import Column


class TableReconstructor(object):
    ROW_SP = ';'
    COL_SP = ','
    def __init__(self):
        pass

    def _reformat(self):
        '''reformat


        :return: err code
        '''
        def check_type(type, value):
            try:
                if type == 'string':
                    str(value)
                elif type == 'int':
                    int(value)
                elif type == 'long':
                    long(value)
                elif type == 'float':
                    float(value)
                elif type == 'boolean':
                    bool(value)
                else:
                    return False # not in condition
                return True
            except Exception as e:
                return False
        # data not string
        if not isinstance(self.data, str):
            return 1

        data = self.data.strip()
        data = data[:-1] if data.endswith(self.ROW_SP) else data

        raw_lines = data.split(self.ROW_SP)
        # only meta data
        if len(raw_lines) <= 3:
            return 1

        '''meta data'''
        self.name_row = raw_lines[0].split(self.COL_SP)
        self.type_row = raw_lines[1].split(self.COL_SP)
        self.def_row = raw_lines[2].split(self.COL_SP)
        # check index is valid: --> list
        if not isinstance(self.index, (int, str)):
            return 1 #  index err
        elif isinstance(self.index, int):
            if self.index < 0 or self.index >= len(self.name_row):
                return 1 # index value err
            self.index = [self.index]
        else:
            try:
                if self.COL_SP not in self.index:
                    self.index = [int(self.index)]
                else:
                    indexes = self.index.split(self.COL_SP)
                    self.index = {int(index) for index in indexes}
                    self.index = list(self.index)
                    self.index.sort()
            except Exception as e:
                return 1 # can't convert to int
        # check meta col num equal
        meta_len_set = {len(self.name_row), len(self.type_row),
                        len(self.def_row)}
        if len(meta_len_set) == 1:
            return 2  # meta rows should have same col num
        # check type and def match
        self.type_row = [t.lower() or 'string' for t in self.type_row]
        for i in range(len(self.def_row)):
            if self.def_row[i]:
                check_ret = check_type(self.type_row[i], self.def_row[i])
                if not check_ret:
                    return 2 # type and def not match
            else:
                self.def_row[i] = None # if no def set to Noe

        '''process data lines'''
        self.total_lines = len(raw_lines) - 3
        # filter ignored and illegal; generate data lines
        ignored_rows = []
        illegal_rows = []
        self.data_rows = []
        for i in range(3, len(raw_lines)):
            line_items = raw_lines[i].split(self.COL_SP)
            if len(line_items) != len(self.name_row):
                illegal_rows.append(i)  # col count not match
            else:
                for j in range(len(line_items)):
                    if not line_items[j] and self.def_row[j] is None:
                        ignored_rows.append(i)  # no value and no default
                    else:
                        value = line_items[j]
                        type = self.type_row[j]
                        if not check_type(type, value):
                            illegal_rows.append(i) # type not match
                        else:
                            # set to default
                            line_items[j] = line_items[i] or self.def_row[j]
                            self.data_rows.append(line_items)
        self.ignored_lines = len(ignored_rows)
        self.illegal_lines = len(illegal_rows)

    def _set_org_columns(self):
        columns = []
        for i in range(len(self.name_row)):
            column = Column(self.name_row[i], [])
            for row in self.data_rows:
                column.add_value(row[i])
        return columns

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
        self.index, self.count, self.sort, self.data = index, count, sort, data
        # check whether error
        format_code = self._reformat()
        if format_code != 0:
            result.set_err_no(format_code)
            return result

        # set total, ignored, illegal
        result.set_total_lines(self.total_lines)
        result.set_ignored_lines(self.ignored_lines)
        result.set_illegal_lines(self.illegal_lines)
        if self.ignored_lines + self.illegal_lines == self.total_lines:
            return result

        '''process columns'''
        # set origin columns
        org_columns = self._set_org_columns()
        for column in org_columns:
            assert isinstance(column, Column)
            result.add_column(column)

        # set ext columns
        return result
