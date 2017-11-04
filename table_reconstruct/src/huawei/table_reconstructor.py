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
        print 'name_row: ', self.name_row
        print 'type_row: ', self.type_row
        print 'def_row: ', self.def_row
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
        if len(meta_len_set) != 1:
            return 2  # meta rows should have same col num
        print 'meta_len: ', meta_len_set
        # check type and def match
        self.type_row = [t.lower() or 'string' for t in self.type_row]
        for i in range(len(self.def_row)):
            if self.def_row[i]:
                check_ret = check_type(self.type_row[i], self.def_row[i])
                if not check_ret:
                    return 2 # type and def not match
            else:
                self.def_row[i] = None # if no def set to Noe
        print '==== meta row after process'
        print 'name_row: ', self.name_row
        print 'type_row: ', self.type_row
        print 'def_row: ', self.def_row
        print 'index', self.index

        '''process data lines'''
        self.total_lines = len(raw_lines) - 3
        # filter ignored and illegal; generate data lines
        ignored_rows = []
        illegal_rows = []
        self.data_rows = []
        for i in range(3, len(raw_lines)):
            line_items = raw_lines[i].split(self.COL_SP)
            print 'line {}: {}'.format(i, line_items)
            if len(line_items) != len(self.name_row):
                illegal_rows.append(i)  # col count not match
            else:
                for j in range(len(line_items)):
                    if not line_items[j] and self.def_row[j] is None:
                        ignored_rows.append(i)  # no value and no default
                        break
                    else:
                        value = line_items[j]
                        tp = self.type_row[j]
                        if not check_type(tp, value):
                            illegal_rows.append(i) # type not match
                            break
                        else:
                            # set to default
                            line_items[j] = line_items[j] or self.def_row[j]
                self.data_rows.append(line_items)
        self.ignored_lines = len(ignored_rows)
        self.illegal_lines = len(illegal_rows)
        return 0

    def _set_org_columns(self):
        columns = []
        print 'pre data: ', self.data_rows
        for i in range(len(self.name_row)):
            column = Column(self.name_row[i], [])
            for row in self.data_rows:
                column.add_value(row[i])
            columns.append(column)
        return columns

    def extend_column(self, column):
        assert isinstance(column, Column)
        base_name = column.get_column_name()
        base_values = column.get_values()

        # get keys and sort
        key_set = {value for value in base_values}
        keys = list(key_set)
        if self.sort == 0:
            keys.sort() # alphabetic
        elif self.sort == 1:
            # sort by frequency then alphabetic
            frequence_map = {}
            for key in base_values:
                if key not in frequence_map:
                    frequence_map[key] = 1
                else:
                    frequence_map[key] += 1
            keys.sort(cmp=lambda x, y:
                True if frequence_map[x] > frequence_map[y] or
                    (frequence_map[x] == frequence_map[y] and x > y)
                else False)

        # get reserved keys
        if self.count == 0 or self.count > len(keys):
            reserved_keys = keys
        else:
            reserved_keys = keys[:self.count]

        # generate new columns
        ext_columns = []
        for key in reserved_keys:
            name = 'Flag_{0}_{1}'.format(base_name, key)
            values =  ['True' if value == key else 'False'
                       for value in base_values]
            print '\t name: {}, values: {}'.format(name, values)
            ext_columns.append(Column(name, values))
        return ext_columns

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
        result.set_err_no(format_code)
        if format_code != 0:
            return result

        # set total, ignored, illegal
        result.set_total_lines(self.total_lines)
        result.set_ignored_lines(self.ignored_lines)
        result.set_illegal_lines(self.illegal_lines)
        if self.ignored_lines + self.illegal_lines == self.total_lines:
            return result
        print 'err: {}, total: {}, ig: {}, ill: {}'.format(
            result.err_no, result.total_lines, result.ignored_lines,
            result.illegal_lines)

        '''process columns'''
        # set origin columns
        org_columns = self._set_org_columns()
        print '==== org column'
        for column in org_columns:
            assert isinstance(column, Column)
            print '\t name: {}, values: {}'.format(
                column.column_name, column.values)
            result.add_column(column)

        # set ext columns
        print '==== ext column'
        for index in self.index:
            pre_column = result.table.columns[index]
            ext_columns = self.extend_column(pre_column)
            map(result.add_column, ext_columns)
        return result

tableR = TableReconstructor()
data = 'Name,Gender;,;,Male;a,Male;b,Female'
result = tableR.do_reconstruct('1', 2, 0, data)
print result.err_no
