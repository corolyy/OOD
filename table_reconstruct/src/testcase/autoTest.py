#!/usr/bin/env python
# -*-coding:utf-8-*-
import unittest
import sys
sys.path.append('..')
from huawei.table_reconstructor import TableReconstructor
from huawei.common.table_reconstruct import TableReconstruct

class Test(unittest.TestCase):
    def testCase01(self):
        tableR = TableReconstructor()
        data = 'Name,Gender;,;,Male;a,Male;b,Female'
        result = tableR.do_reconstruct('1', 2, 0, data)

        rtn = TableReconstruct.result_2_str(result)

        self.assertEqual(rtn,
                         'ErrNo:0\r\n'
                         'TotalLines:2\r\n'
                         'IgnoredLines:0\r\n'
                         'IllegalLines:0\r\n'
                         "Name,Gender,Flag_Gender_Female,Flag_Gender_Male;a,Male,False,True;b,Female,True,False;")

