'''
行外工作经历得分计算
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
from models.layer1_model import A01,A866

def calculate_in_bank_working_experience_score(session):
    
    def cal_working_time(x):
        #计算行外工作时间
        x['a8661'] = pd.to_datetime(x['a8661'])
        x['a8662'] = pd.to_datetime(x['a8662'])
        merged_intervals = []
        for _, row in x.iterrows():
            start_time = row['a8661']
            end_time = row['a8662']
            print(start_time, end_time)
            mark = 0
            for i, interval in enumerate(merged_intervals):
                if (interval[0] <= start_time <= interval[1]) or (interval[0] <= end_time <= interval[1]):
                    print(merged_intervals[i])
                    if mark == 0:
                        merged_intervals[i] = (min(start_time, interval[0]), max(end_time, interval[1]))
                        mark = 1
                    else:
                        merged_intervals[i] = (max(start_time, interval[0]), min(end_time, interval[1]))
            if mark == 0:
                merged_intervals.append((start_time, end_time))

        total_work_time = sum((end_time - start_time).days / 365 for start_time, end_time in merged_intervals)
        return total_work_time * 10


    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base = df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    # df_base = df_base[df_base['任职形式'] == '担任'] # TODO 任职形式字段不清楚
    df_base = df_base[df_base['dept_code'] != '高管']
    # df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)] # TODO code error

    df_working = pd.read_sql(session.query(A866).statement, session.bind)

    df_working_merge_base = pd.merge(df_working, df_base[['a0188', 'a0141', 'a01145']], on='a0188', how='left')

    df_working_merge_base = df_working_merge_base[df_working_merge_base['a8662'] < df_working_merge_base['a0141']]

    df_working_merge_base_g = df_working_merge_base.groupby('a0188').apply(cal_working_time)
    df_working_merge_base_g.rename('过去工作经验得分',inplace=True)

    df_result = pd.merge(df_base[['a0188']], df_working_merge_base_g, on='a0188', how='left')
    df_result.fillna(0, inplace=True)


    return df_result
