#!/usr/bin/env python
# -*-coding:utf-8-*-
class TableReconstruct(object):
    def __init__(self):
        pass

    @staticmethod
    def result_2_str(result):
        '''Convert table to string

        :param result: object to be convert
        :return: string
        '''
        if not result:
            return 'Invalid result'

        err_no = 'ErrNo:%s\r\n' % result.get_err_no()
        if result.get_err_no() != 0:
            return ''.join(err_no)

        totalLines = 'TotalLines:%s\r\n' % result.get_total_lines()
        ignoredLines = 'IgnoredLines:%s\r\n' % result.get_ignored_lines()
        illegalLines = 'IllegalLines:%s\r\n' % result.get_illegal_lines()

        rtn_list = []
        rtn_list.append(err_no)
        rtn_list.append(totalLines)
        rtn_list.append(ignoredLines)
        rtn_list.append(illegalLines)

        # 说明能被get到的column只包含正确的，illegal和ignore都被忽略了
        max_row_index = (result.get_total_lines() -
                         (result.get_ignored_lines() +
                          result.get_illegal_lines())
                         - 1)

        if max_row_index > 0:
            columns = result.get_table().get_columns()
            column_value = ''
            for column in columns:
                column_value = column_value + column.get_column_name() + ','
            column_value = column_value[0: len(column_value) - 1] + ';'

            index = 0

            while index <= max_row_index:
                for column in columns:
                    column_value += (str(column.get_values()[index]) + ',')
                column_value = column_value[0: len(column_value) - 1] + ';'
                index += 1
            rtn_list.append(column_value)
        return ''.join(rtn_list) #  'Total..Ig...Il...names;line1;line2...'
