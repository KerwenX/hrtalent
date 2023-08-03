'''
学习提升得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
from models.layer1_model import A01,A04,Bm_gxsjb

def cal_learning_growing_up_score(session):

    # TODO 还没修改
    #内训师
    df_peixun= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='内训师')
    df_peixun.rename(columns={'工号':'a0188'}, inplace=True)

    df_peixun['考核得分'] = df_peixun['a81884'].apply(lambda x: 0 if x == '无' else int(x))

    def cal_neixunshi_score(x):
        lvl_score = 0
        if x['内训师现等级'] == '初级内训师':
            lvl_score = 20
        elif x['内训师现等级'] == '中级内训师':
            lvl_score = 30
        elif x['内训师现等级'] == '高级内训师':
            lvl_score = 40
        elif x['内训师现等级'] == '专家内训师':
            lvl_score = 50
        jifen_score = 0
        if x['考核得分'] < 80:
            jifen_score = 0
        elif 80 <= x['考核得分'] <= 85:
            jifen_score = 30
        elif 80 < x['考核得分'] <= 90:
            jifen_score = 35
        elif 90 < x['考核得分'] <= 95:
            jifen_score = 40
        elif 95 < x['考核得分'] <= 100:
            jifen_score = 45
        elif x['考核得分'] > 100:
            jifen_score = 50
        final_score = lvl_score + jifen_score
        return final_score


    df_peixun['内训师资格得分'] = df_peixun.apply(cal_neixunshi_score, axis=1)


    #学习平台
    df_pingtai= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='学习平台')
    df_pingtai.rename(columns={'工号':'a0188'}, inplace=True)

    df_pingtai['学习平台得分情况得分'] = df_pingtai['empat181'].astype(float)

    #全员轮训
    df_lunxun= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='2022年全员轮训')
    now_year = 2022
    df_lunxun = df_lunxun[df_lunxun['归属年份'].astype(int) == now_year]
    df_lunxun.rename(columns={'工号':'a0188'}, inplace=True)


    def cal_lunxun_score(x):
        final_score = 0
        bixiuke_score = float(x['必修课'])
        if x['公开课'] == '无需参加':
            final_score = bixiuke_score
        else:
            final_score = (float(x['公开课']) + bixiuke_score) / 2
        return final_score

    df_lunxun['全员轮训情况得分'] = df_lunxun.apply(cal_lunxun_score, axis=1)
    df_lunxun = df_lunxun[['a0188', '全员轮训情况得分']].groupby('a0188').max()


    #在职教育得分

    df_jiaoyu = pd.read_sql(session.query(A04).statement, session.bind)
    df_gaoxiao = pd.read_sql(session.query(Bm_gxsjb).statement, session.bind)
    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfsyl'] == '是']['mc0000'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sf'] == '是']['mc0000'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfjbw'] == '是']['mc0000'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['qs100'] == '是']['mc0000'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['sfqs2'] == '是') & (df_gaoxiao['qs100'] == '否')]['mc0000'].to_list()])


    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['a0447'] == '在职']
    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['a8662'].notnull()]


    def cal_zaizhi_score(x):
        before_2001 = datetime.datetime.strptime(x['a8662'], '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime('2001-01-01', '%Y-%m-%d')
        has_fujian = not(pd.isna(x['fjo']) and pd.isna(x['fjt']) and pd.isna(x['fj3']))

        final_score = 0
        if x is None:
            final_score = 0
        else:
            base_score = 0
            school_coe = 1.1
            zhengshu_coe = 1
            if x['a0429'] == '博士研究生' or x['a0440'] == '博士学位':
                base_score = 100
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0

            elif x['a0429'] in ['硕士研究生', '硕士', '双硕士'] or x['a0440'] == '硕士学位':
                if before_2001:
                    base_score = 100
                else:
                    base_score = 90
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0    
            elif x['a0429'] in ['大学本科', '双本科'] or x['a0440'] == '学士学位':
                if before_2001:
                    base_score = 90
                else:
                    base_score = 80
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            elif x['a0429'] in ['大学专科', '双大专'] :
                if before_2001:
                    base_score = 80
                else:
                    base_score = 70

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            elif x['a0429'] in ['中等专科', '高中'] :
                if before_2001:
                    base_score = 70
                else:
                    base_score = 60

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            else:
                base_score = 0

            final_score = base_score * school_coe * zhengshu_coe

        return final_score


    df_jiaoyu_zaizhi['学校得分'] = df_jiaoyu_zaizhi.apply(cal_zaizhi_score, axis=1)

    df_jiaoyu_zaizhi_group = df_jiaoyu_zaizhi.groupby(['a0188']).apply(lambda x: x['学校得分'].max())

    df_jiaoyu_zaizhi_group.rename('在职教育得分', inplace=True)

    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['dept_code'] != '高管']
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['a0188']], df_peixun[['a0188', '内训师资格得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_pingtai[['a0188', '学习平台得分情况得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_lunxun, on='a0188', how='left')
    df_result = pd.merge(df_result, df_jiaoyu_zaizhi_group, on='a0188', how='left')

    df_result.fillna(0, inplace=True)


    return df_result




