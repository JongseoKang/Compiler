"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file defines test cases for our ToyPL lexer.
import ply.lex as lex
import lexer as lexer
import unittest
import sys

cases = [
    ["assessment/test01.toypl", "assessment/test01_lex_result", "assessment/no_error_message"] # 2 pts
    ,
    ["assessment/test02.toypl", "assessment/test02_lex_result", "assessment/no_error_message"] # 2 pts
    ,
    ["assessment/test03.toypl", "assessment/test03_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test04.toypl", "assessment/test04_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test05.toypl", "assessment/test05_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test06.toypl", "assessment/test06_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test07.toypl", "assessment/test07_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test08.toypl", "assessment/test08_lex_result", "assessment/no_error_message"] # 7 pts
    ,
    ["assessment/test09.toypl", "assessment/test09_lex_result", "assessment/no_error_message"] # 10 pts
    ,
    ["assessment/test10.toypl", "assessment/test10_lex_result", "assessment/test10_error_message"] # 7 pts
    ,
    ["assessment/test11.toypl", "assessment/test11_lex_result", "assessment/test11_error_message"] # 7 pts
    ,
    ["assessment/test12.toypl", "assessment/test12_lex_result", "assessment/test12_error_message"] # 10 pts
    ,
    ["assessment/test13.toypl", "assessment/test13_lex_result", "assessment/test13_error_message"] # 10 pts
    ,
    ["assessment/test14.toypl", "assessment/test14_lex_result", "assessment/test14_error_message"] # 10 pts
]

def eval_golden(i):
    return str(lexer.lex_str(i))

def check_golden(tester, fs):
    lexer.initialize_error_message()
    # parse files
    if_name = fs[0]
    of_name = fs[1]
    error_name = fs[2]
    # open files and get a lexing result
    if_obj = open(if_name, "r")
    i = if_obj.read()
    if_obj.close()
    o = eval_golden(i)
    of_obj = open(of_name, "r")
    o_golden = of_obj.read()
    of_obj.close()
    error_obj = open(error_name, "r")
    error = error_obj.read()
    error_obj.close()
    error_message = lexer.error_message
    # chek the result
    tester.assertEqual(o, o_golden)
    tester.assertEqual(error, error_message)


class LexerTest(unittest.TestCase):

    def test_case1(self):
        check_golden(self, cases[0])

    def test_case2(self):
        check_golden(self, cases[1])

    def test_case3(self):
        check_golden(self, cases[2])

    def test_case4(self):
        check_golden(self, cases[3])

    def test_case5(self):
        check_golden(self, cases[4])

    def test_case6(self):
        check_golden(self, cases[5])

    def test_case7(self):
        check_golden(self, cases[6])

    def test_case8(self):
        check_golden(self, cases[7])

    def test_case9(self):
        check_golden(self, cases[8])

    def test_case10(self):
        check_golden(self, cases[9])

    def test_case11(self):
        check_golden(self, cases[10])

    def test_case12(self):
        check_golden(self, cases[11])

    def test_case13(self):
        check_golden(self, cases[12])

    def test_case14(self):
        check_golden(self, cases[13])

if __name__ == "__main__":
    unittest.main()
