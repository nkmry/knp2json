#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json


def execute(knp_tab_output):
    # phrase = {type, relation, relationType, basics, morphemes, features}
    # basic = {type, relation, relationType, phrase, features [, case, caseAnalysis]}
    # morpheme = {type, phrase, morpheme, features}
    results = []
    lines = knp_tab_output.split('\n')
    for l in lines:
        if len(l) < 1:
            continue
        if l[0] == "#":
            phrases = []
            basics = []
            morphemes = []
            continue
        if l == "EOS":
            results.append({"phrases": phrases, "basics": basics, "morphemes": morphemes})
            continue
        d = {}
        f = re.split('>?<?', l)
        if l[0] == '*':
            d['features'] = f[1:-1]  # 最初は係り受けの情報、最後は空
            d['relation'] = int(f[0][2:-2])
            d['relationType'] = f[0][-2]
            d['basics'] = []
            d['morphemes'] = []
            phrases.append(d)
        elif l[0] == '+':
            d['phrase'] = len(phrases) - 1
            d.update(_analyze_basic(f[:-1]))
            basics.append(d)
            phrases[-1]['basics'].append(len(basics)-1)
        else:
            d['phrase'] = len(phrases) - 1
            d.update(_analyze_morpheme(f[:-1]))
            morphemes.append(d)
            phrases[-1]['morphemes'].append(len(morphemes)-1)
    return results


def _analyze_basic(basic_info):
    d = {'relation': int(basic_info[0][2:-2]), 'relationType': basic_info[0][-2]}
    basic_info = basic_info[1:]
    removed = []
    for f in basic_info:
        splited = f.split(':')
        if len(splited) > 1:
            removed.append(f)
            if splited[0] == "解析格":
                d['case'] = splited[1]
            if splited[0] == "格解析結果":
                d['caseAnalysis'] = _analyze_case_analysis(splited[-1])
    for f in removed:
        basic_info.remove(f)
    d['features'] = basic_info
    return d


def _analyze_case_analysis(case_analysis_string):
    elements = case_analysis_string.split(';')
    d = {}
    for element in elements:
        splited = element.split('/')
        e = {'flag': splited[1],
             'expression': splited[2],
             '#basics': _change_int(splited[3]),
             'sentenceId': _change_int(splited[5])}
        d[splited[0]] = e
    return d


def _change_int(int_string):
    if int_string.isdigit():
        return int(int_string)
    else:
        return int_string


def _analyze_morpheme(morpheme_info):
    s = morpheme_info[0].split(' ')
    d = {'input': s[0], 'pronunciation': s[1], 'original': s[2], 'pos': s[3], 'posId': s[4], 'subPos': s[5],
         'subPosId': s[6], 'inflectionType': s[7], 'inflectionTypeId': s[8], 'inflection': s[9], 'inflectionId': s[10],
         'others': s[11]}
    morpheme_info = morpheme_info[1:]
    removed = []
    for f in morpheme_info:
        splited = f.split(':')
        if len(splited) > 1:
            removed.append(f)
            if splited[0] == 'Wikipediaエントリ':
                d['wikipedia'] = splited[1]
            else:
                d[splited[0]] = splited[1:]
    for f in removed:
        morpheme_info.remove(f)
    d['features'] = morpheme_info
    return d


def show_analyzed_knp_info(analyzed_knp_info):
    phrases = analyzed_knp_info["phrases"]
    basics = analyzed_knp_info["basics"]
    morphemes = analyzed_knp_info["morphemes"]
    print("### 文節 ###")
    attr = ['relation', 'relationType', 'basics', 'morphemes', 'features', 'type']
    for i in range(len(phrases)):
        print(str(i) + ': ' + _convert_dictionary_to_string(phrases[i], attr))
    print("### 形態素 ###")
    attr = ['phrase', 'input', 'pos', 'subPos', 'wikipedia', 'features', 'type']
    for i in range(len(morphemes)):
        print(str(i) + ': ' + _convert_dictionary_to_string(morphemes[i], attr))
    print("### 基本句 ###")
    attr = ['relation', 'relationType', 'phrase', 'case', 'caseAnalysis', 'features', 'type']
    for i in range(len(basics)):
        print(str(i) + ': ' + _convert_dictionary_to_string(basics[i], attr))


def _convert_dictionary_to_string(dictionary, keys):
    s = '{'
    for k in keys:
        if k in dictionary.keys():
            s += '\'' + k + '\':' + str(dictionary[k]) + ', '
    s += '}'
    return s


if __name__ == "__main__":
    syntactic_info = execute(sys.stdin.read())
    print(json.dumps(syntactic_info, indent=2, ensure_ascii=False))
