# -*- coding: utf-8 -*-
# 用于列table合并
# @Author  : white.tie
# @Time    : 2023/4/26 11:45
# @File: combining.py.py

# 列table转json格式
import pandas as pd


def combining_json(table_html, col=[0], tagSep=';',keySep=' '):
    """
    tagSep:多value合并时切分符号
    keySep: 多个key值合并时分隔符
    table_html: 输入需要转成json的列table
    return : 返回的字典组成的列表
    """
    df = pd.read_html(table_html)
    results = list(df[0].T.to_dict().values())
    # print(results)
    # 遍历列数组装
    json_ls = []
    for i in range(max(col)+1, len(results[0])):
        json_dic = {}
        for result_ in results:
            try:
                keys = [result_[i] for i in col if str(result_[i])!= "nan"]
                # 去除重复的key值
                key_after = []
                for key in keys:
                    if key not in key_after:key_after.append(key)
                    else: pass
                key_ = keySep.join(key_after).replace("\xa0"," ")
                value = result_[i]
                if str(value) == "nan":
                    value = ""
                if result_[0] in json_dic.keys():
                    if value != "":
                        json_dic[key_] = json_dic[key_] + tagSep + value
                else:
                    json_dic[key_] = value
            except KeyError:
                break
        if '' in json_dic.keys():
            del json_dic['']
        if len(json_dic) > 0:
            json_ls.append(json_dic)
    return json_ls