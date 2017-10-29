#!/usr/bin/env python
# -*-coding:utf-8-*-
from table import Table


class ReconstructResult(object):
    def __init__(self):
        self.err_no = 0
        self.total_lines = 0
        self.ignored_lines = 0
        self.illegal_lines = 0
        self.table = Table()

    def set_err_no(self, err_no):
        self.err_no = err_no

    def get_err_no(self):
        return self.err_no

    def set_total_lines(self, total_lines):
        self.total_lines = total_lines

    def get_total_lines(self):
        return self.total_lines

    def set_ignored_lines(self, ignored_lines):
        self.ignored_lines = ignored_lines

    def get_ignored_lines(self):
        return self.ignored_lines

    def set_illegal_lines(self, illegal_lines):
        self.illegal_lines = illegal_lines

    def get_illegal_lines(self):
        return self.illegal_lines

    def add_column(self, column):
        self.table.add_column(column)

    def get_table(self):
        return self.table

