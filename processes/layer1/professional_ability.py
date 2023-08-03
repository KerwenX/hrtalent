'''
计算专业能力得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re
from models.layer1_model import A01,A04,Bm_gxsjb,A832


def cal_professional_ability_score(session):

    #教育情况
    df_jiaoyu = pd.read_sql(session.query(A04).statement, session.bind)

    df_gaoxiao = pd.read_sql(session.query(Bm_gxsjb).statement, session.bind)

    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfsyl'] == '是']['mc0000'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sf'] == '是']['mc0000'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfjbw'] == '是']['mc0000'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['qs100'] == '是']['mc0000'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['sfqs2'] == '是') & (df_gaoxiao['qs100'] == '否')]['mc0000'].to_list()])

    df_jiaoyu_quanrizhi = df_jiaoyu[df_jiaoyu['a0447'] == '全日制']


    def cal_quanrizhi_score(x):
        final_score = 0
        if x is None:
            final_score = 40
        else:
            base_score = 40
            school_coe = 1
            zhengshu_coe = 0.8
            if x['a0429'] == '博士研究生' or x['a0440'] == '博士学位':
                base_score = 100
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3
                if x['a0429'] == '博士研究生' and x['a0440'] == '博士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8
            elif x['a0429'] in ['硕士研究生', '硕士', '双硕士'] or x['a0440'] == '硕士学位':
                base_score = 90
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3
                if x['a0429'] in ['硕士研究生', '硕士', '双硕士'] and x['a0440'] == '硕士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8           
            elif x['a0429'] in ['大学本科', '双本科'] or x['a0440'] == '学士学位':
                base_score = 80
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3
                if x['a0429'] in ['大学本科', '双本科'] and x['a0440'] == '学士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8 
            elif x['a0429'] in ['大学专科', '双大专'] :
                base_score = 60
            elif x['a0429'] in ['中等专科', '高中'] :
                base_score = 50
            else:
                base_score = 40

            final_score = base_score * school_coe * zhengshu_coe

        return final_score


    df_jiaoyu_quanrizhi['学校得分'] = df_jiaoyu_quanrizhi.apply(cal_quanrizhi_score, axis=1)

    df_jiaoyu_quanrizhi_group = df_jiaoyu_quanrizhi.groupby(['a0188']).apply(lambda x: x['学校得分'].max())
    df_jiaoyu_quanrizhi_group.rename('全日制教育得分', inplace=True)

    #职称情况得分
    #员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', '聘任职业技术等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['dept_code'] != '高管']
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]


    def cal_zhicheng_score(x):
        final_score = 20
        if x == '高级':
            final_score = 100
        elif x == '中级':
            final_score = 60
        elif x == '初级':
            final_score = 20
        return final_score
    

    df_base['职称情况得分'] = df_base['聘任职业技术等级'].apply(cal_zhicheng_score)
    
    
    #技术资格得分
    df_zhengshu_score = pd.read_excel('seqdata\江南农商银行_专业序列资质标签加分表 v5 20230713.xlsx', sheet_name='Sheet3')
    df_zhengshu = pd.read_sql(session.query(A832).statement, session.bind)
    df_zhengshu_defen = pd.merge(df_zhengshu[['a0188', 'a83213']], df_zhengshu_score[['a83213', '名称', '等级', '标签得分']], on='a83213', how='left')
    
    def cal_zhengshu_score(x):
        final_score = 0
        zhengshu_dict = {}
        for _, row in x.iterrows():
            if not pd.isna(row['标签得分']):
                if not pd.isna(row['名称']):
                    if row['名称'] in zhengshu_dict:
                        zhengshu_dict[row['名称']] = max(row['标签得分'], zhengshu_dict[row['名称']])
                    else:
                        zhengshu_dict[row['名称']] = row['标签得分']
                else:
                    final_score += row['标签得分']
        for k in zhengshu_dict:
            final_score += zhengshu_dict[k]
        
        return final_score


    df_zhengshu_defen_g = df_zhengshu_defen.groupby(['a0188']).apply(cal_zhengshu_score)
    df_zhengshu_defen_g.rename('技术资格情况得分', inplace=True)


    df_result = df_base[['a0188', '职称情况得分']]
    df_result = pd.merge(df_result, df_jiaoyu_quanrizhi_group, on='a0188', how='left')
    df_result = pd.merge(df_result, df_zhengshu_defen_g, on='a0188', how='left')

    return df_result




