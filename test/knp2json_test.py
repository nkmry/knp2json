#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
import os.path as path
pardir_path = path.dirname(__file__) + path.sep + os.pardir
sys.path.append(pardir_path)
import knp2json.knp2json as k2j


class Knp2jsonTest(unittest.TestCase):

    def setUp(self):
        file = open('test1_knp.txt')
        self.knp_info = k2j.execute(file.read())
        file.close()

    def test_analyze_knp(self):
        self.assertEqual(len(self.knp_info), 1)
        self.assertEqual(len(self.knp_info[0]["phrases"]), 14)
        self.assertEqual(len(self.knp_info[0]["basics"]), 20)
        self.assertEqual(len(self.knp_info[0]["morphemes"]), 41)
        self.assertEqual(self.knp_info[0]["phrases"][0]["basics"], [0, 1, 2])
        self.assertEqual(self.knp_info[0]["phrases"][0]["morphemes"], [0, 1, 2, 3, 4])
        self.assertEqual(self.knp_info[0]["phrases"][0]["relation"], 6)
        self.assertEqual(self.knp_info[0]["phrases"][0]["relationType"], "D")
        self.assertEqual(self.knp_info[0]["phrases"][-1]["basics"], [19])
        self.assertEqual(self.knp_info[0]["phrases"][-1]["morphemes"], [38, 39, 40])
        self.assertEqual(self.knp_info[0]["phrases"][-1]["relation"], -1)
        self.assertEqual(self.knp_info[0]["phrases"][-1]["relationType"], "D")
        # k2j.show_analyzed_knp_info(self.knp_info[0])
        file = open('test2_knp.txt')
        self.knp_info = k2j.execute(file.read())
        self.assertEqual(len(self.knp_info), 6)


    def test_analyze_basic(self):
        self.assertEqual(self.knp_info[0]["basics"][0]["relation"], 1)
        self.assertEqual(self.knp_info[0]["basics"][0]["relationType"], "D")
        self.assertEqual(self.knp_info[0]["basics"][2]["case"], "ガ")
        self.assertNotIn("解析格:ガ", self.knp_info[0]["basics"][2]["features"])
        self.assertEqual(self.knp_info[0]["basics"][6]["case"], "時間")
        self.assertNotIn("解析格:時間", self.knp_info[0]["basics"][6]["features"])
        self.assertEqual(self.knp_info[0]["basics"][-1]["relation"], -1)
        self.assertEqual(self.knp_info[0]["basics"][-1]["relationType"], "D")

    def test_analyze_case_analysis(self):
        self.assertIn("caseAnalysis", self.knp_info[0]["basics"][-1])
        ca = self.knp_info[0]["basics"][-1]["caseAnalysis"]
        c = ca["ガ"]
        self.assertEqual(c["flag"], "U")
        self.assertEqual(c["expression"], "-")
        self.assertEqual(c["#basics"], "-")
        self.assertEqual(c["sentenceId"], "-")
        c = ca["ヲ"]
        self.assertEqual(c["flag"], "C")
        self.assertEqual(c["expression"], "グッズ")
        self.assertEqual(c["#basics"], 16)
        self.assertEqual(c["sentenceId"], 1)


if __name__ == '__main__':
    unittest.main()
