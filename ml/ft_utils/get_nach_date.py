import pandas as pd
import json
from time import time
import os
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime
from dateutil import relativedelta
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils.dataframe import dataframe_to_rows
import xlsxwriter



def get_final_bin(pivot_df):
    '''
    input: pivot_df, contains avg of each bin for each month. Indexed on months and bins are columns.
    output: bins having max avg

    In pivot_df, the last row has the avg of the each bin across months.
    Filter for all the bins whose avg >= 0.9*max avg
    From the filtered bins return the index of bin having the least std
    '''
    avg_lst = pivot_df.iloc[-2, :].tolist()
    std_lst = pivot_df.iloc[-1, :].tolist()
    max_avg = max(avg_lst)
    max_avg_index = avg_lst.index(max_avg)
    min_std_lst = [std_lst[i] for i, val in enumerate(avg_lst) if val >= max_avg * 0.9]
    if min_std_lst:
        return min_std_lst.index(min(min_std_lst))
    else:
        return max_avg_index



def get_nach_date(report_json):
    '''
    Input: type3 json report
    Output: recommended date range based on avg daily balance

    Takes out the daily balance part from the input json and make a user_df out of it.
    Calculates daily avg balance = (opening + closing balance) / 2
    Calculates 2days lag and 2days lead daily_avg_balance to get avg for bins.

    For window size of [5, 3]
        pivot user_df with columns as bins and rows as month_year and values as daily_avg_balance
        add one row to pivot_df having avg of each bin across every month
        call get_final_bin to get the bin having less std and more avg

    Return window of size 5 or 3 based on whichever one is having the max avg.
    '''

    try:
        user_df = pd.DataFrame()
        try:
            for month in range(len(report_json['daily_open_close_balances'])):
                balance_df = pd.DataFrame(report_json['daily_open_close_balances'][month]['dailyBalance'])
                user_df = pd.concat((user_df, balance_df), axis=0, ignore_index=True)
        except KeyError as e:
            print("Got keyerror in function get_nach_date: ", e)
            return None
        except Exception as e:
            print("Got error in function get_nach_date: ", e)
            return None

        if len(user_df) == 0:
            return None

        # these bins_for_window5 will help us in groupby
        user_df.rename(columns={'transaction_date': 'date'}, inplace=True)
        user_df['date'] = user_df['date'].astype('datetime64')
        user_df['day'] = user_df['date'].dt.day
        user_df['month'] = user_df['date'].dt.month
        user_df['year'] = user_df['date'].dt.year
        user_df['dayavg_balance'] = (user_df['opening_balance'] + user_df['closing_balance']) / 2
        user_df['month_year'] = user_df['month'].astype(str) + '-' + user_df['year'].astype('str').apply(lambda x: x[-2:])
        # user_df['dayavg_balance5_avg'] = user_df['dayavg_balance'].rolling(5).mean()
        # user_df['dayavg_balance3_avg'] = user_df['dayavg_balance'].rolling(3).mean()

        # Then adds few lag and lead bins_for_window5 which helps in finding the avg for 3,5 size bins.
        user_df['dayavg_balance_2lag'] = user_df['dayavg_balance'].shift(2)
        user_df['dayavg_balance_1lag'] = user_df['dayavg_balance'].shift(1)
        user_df['dayavg_balance_2lead'] = user_df['dayavg_balance'].shift(-2)
        user_df['dayavg_balance_1lead'] = user_df['dayavg_balance'].shift(-1)
        user_df['dayavg_balance5_avg'] = user_df[['dayavg_balance', 'dayavg_balance_2lag', 'dayavg_balance_1lag', 'dayavg_balance_2lead', 'dayavg_balance_1lead']].mean(axis=1)
        user_df['dayavg_balance3_avg'] = user_df[['dayavg_balance', 'dayavg_balance_1lag', 'dayavg_balance_1lead']].mean(axis=1)

        # add bins for window5 and window3, this is dynamically calculated based on the date range of user_df
        bins_for_window5 = []
        bins_for_window3 = []
        for i in sorted(user_df['day'].unique().tolist()):
            bins_for_window5.append(str(i - 2 if i - 2 > 0 else 31 + i - 2) + '_' + str(i + 2 if i + 2 <= 31 else i + 2 - 31))
            bins_for_window3.append(str(i - 1 if i - 1 > 0 else 31 + i - 1) + '_' + str(i + 1 if i + 1 <= 31 else i + 1 - 31))

        # pivot_df : this stores the avg of each bin for each month, from this we will check for the bin having max avg
        pivot_df = user_df.pivot(columns='day', index='month_year', values='dayavg_balance5_avg')
        pivot_df['month_only'] = [int(x.split('-')[0]) for x in pivot_df.index.tolist()]
        pivot_df['year_only'] = [int(x.split('-')[1]) for x in pivot_df.index.tolist()]
        pivot_df = pivot_df.sort_values(by=['year_only', 'month_only'])
        pivot_df.loc['avg'] = pivot_df.mean(axis=0)
        pivot_df.loc['std'] = pivot_df.std(axis=0)
        pivot_df.drop(columns=['year_only', 'month_only'], inplace=True)
        max_index_lst = pivot_df.idxmax(axis=1).tolist()
        max_avg_bin_for_window5 = get_final_bin(pivot_df)
        max_avg_corrsp_to_window5 = pivot_df.iloc[-2, max_avg_bin_for_window5]

        pivot_df = user_df.pivot(columns='day', index='month_year', values='dayavg_balance3_avg')
        pivot_df['month_only'] = [int(x.split('-')[0]) for x in pivot_df.index.tolist()]
        pivot_df['year_only'] = [int(x.split('-')[1]) for x in pivot_df.index.tolist()]
        pivot_df = pivot_df.sort_values(by=['year_only', 'month_only'])
        pivot_df.loc['avg'] = pivot_df.mean(axis=0)
        pivot_df.loc['std'] = pivot_df.std(axis=0)
        pivot_df.drop(columns=['year_only', 'month_only'], inplace=True)
        max_index_lst = pivot_df.idxmax(axis=1).tolist()
        max_avg_bin_for_window3 = get_final_bin(pivot_df)
        max_avg_corrsp_to_window3 = pivot_df.iloc[-2, max_avg_bin_for_window3]

        # outof window5 and window3 which ever has max avg return that window
        if max_avg_corrsp_to_window5 > max_avg_corrsp_to_window3:
            return bins_for_window5[max_avg_bin_for_window5].split('_')
        else:
            return bins_for_window3[max_avg_bin_for_window3].split('_')

    except Exception as e:
        raise e
        print('Error in funcion get_nach_date : ', e)
        return None



def get_nach_date_report(report_json):
    '''
    Input: type3 json report
    Output: recommended date range based on avg daily balance

    Takes out the daily balance part from the input json and make a user_df out of it.
    Calculates daily avg balance = (opening + closing balance) / 2
    Calculates 2days lag and 2days lead daily_avg_balance to get avg for bins.

    For window size of [5, 3]
        pivot user_df with columns as bins and rows as month_year and values as daily_avg_balance
        add one row to pivot_df having avg of each bin across every month
        call get_final_bin to get the bin having less std and more avg

    Return window of size 5 or 3 based on whichever one is having the max avg.
    '''

    try:
        user_df = pd.DataFrame()
        try:
            for month in range(len(report_json['daily_open_close_balances'])):
                balance_df = pd.DataFrame(report_json['daily_open_close_balances'][month]['dailyBalance'])
                user_df = pd.concat((user_df, balance_df), axis=0, ignore_index=True)
        except KeyError as e:
            print("Got keyerror in function get_nach_date: ", e)
            return None
        except Exception as e:
            print("Got error in function get_nach_date: ", e)
            return None

        if len(user_df) == 0:
            return None

        # these bins_for_window5 will help us in groupby
        user_df.rename(columns={'transaction_date': 'date'}, inplace=True)
        user_df['date'] = user_df['date'].astype('datetime64')
        user_df['day'] = user_df['date'].dt.day
        user_df['month'] = user_df['date'].dt.month
        user_df['year'] = user_df['date'].dt.year
        user_df['dayavg_balance'] = (user_df['opening_balance'] + user_df['closing_balance']) / 2
        user_df['month_year'] = user_df['month'].astype(str) + '-' + user_df['year'].astype('str').apply(lambda x: x[-2:])
        # user_df['dayavg_balance5_avg'] = user_df['dayavg_balance'].rolling(5).mean()
        # user_df['dayavg_balance3_avg'] = user_df['dayavg_balance'].rolling(3).mean()

        # Then adds few lag and lead bins_for_window5 which helps in finding the avg for 3,5 size bins.
        user_df['dayavg_balance_2lag'] = user_df['dayavg_balance'].shift(2)
        user_df['dayavg_balance_1lag'] = user_df['dayavg_balance'].shift(1)
        user_df['dayavg_balance_2lead'] = user_df['dayavg_balance'].shift(-2)
        user_df['dayavg_balance_1lead'] = user_df['dayavg_balance'].shift(-1)
        user_df['dayavg_balance5_avg'] = user_df[['dayavg_balance', 'dayavg_balance_2lag', 'dayavg_balance_1lag', 'dayavg_balance_2lead', 'dayavg_balance_1lead']].mean(axis=1)
        user_df['dayavg_balance3_avg'] = user_df[['dayavg_balance', 'dayavg_balance_1lag', 'dayavg_balance_1lead']].mean(axis=1)

        # add bins for window5 and window3, this is dynamically calculated based on the date range of user_df
        bins_for_window5 = []
        bins_for_window3 = []
        for i in sorted(user_df['day'].unique().tolist()):
            bins_for_window5.append(str(i - 2 if i - 2 > 0 else 31 + i - 2) + '_' + str(i + 2 if i + 2 <= 31 else i + 2 - 31))
            bins_for_window3.append(str(i - 1 if i - 1 > 0 else 31 + i - 1) + '_' + str(i + 1 if i + 1 <= 31 else i + 1 - 31))

        # pivot_df : this stores the avg of each bin for each month, from this we will check for the bin having max avg
        pivot_df = user_df.pivot(columns='day', index='month_year', values='dayavg_balance5_avg')
        pivot_df['month_only'] = [int(x.split('-')[0]) for x in pivot_df.index.tolist()]
        pivot_df['year_only'] = [int(x.split('-')[1]) for x in pivot_df.index.tolist()]
        pivot_df = pivot_df.sort_values(by=['year_only', 'month_only'])
        pivot_df.loc['avg'] = pivot_df.mean(axis=0)
        pivot_df.loc['std'] = pivot_df.std(axis=0)
        pivot_df.drop(columns=['year_only', 'month_only'], inplace=True)
        max_index_lst = pivot_df.idxmax(axis=1).tolist()
        max_avg_bin_for_window5 = get_final_bin(pivot_df)
        max_avg_corrsp_to_window5 = pivot_df.iloc[-2, max_avg_bin_for_window5]
        pivot_df.columns = bins_for_window5
        pivot_df.to_csv("/home/ramnaryanpanda/Downloads/Type 3 Reports/just_test5.csv")

        pivot_df = user_df.pivot(columns='day', index='month_year', values='dayavg_balance3_avg')
        pivot_df['month_only'] = [int(x.split('-')[0]) for x in pivot_df.index.tolist()]
        pivot_df['year_only'] = [int(x.split('-')[1]) for x in pivot_df.index.tolist()]
        pivot_df = pivot_df.sort_values(by=['year_only', 'month_only'])
        pivot_df.loc['avg'] = pivot_df.mean(axis=0)
        pivot_df.loc['std'] = pivot_df.std(axis=0)
        pivot_df.drop(columns=['year_only', 'month_only'], inplace=True)
        max_index_lst = pivot_df.idxmax(axis=1).tolist()
        max_avg_bin_for_window3 = get_final_bin(pivot_df)
        max_avg_corrsp_to_window3 = pivot_df.iloc[-2, max_avg_bin_for_window3]
        pivot_df.columns = bins_for_window3
        pivot_df.to_csv("/home/ramnaryanpanda/Downloads/Type 3 Reports/just_test3.csv")

        # outof window5 and window3 which ever has max avg return that window
        if max_avg_corrsp_to_window5 > max_avg_corrsp_to_window3:
            return bins_for_window5[max_avg_bin_for_window5].split('_')
        else:
            return bins_for_window3[max_avg_bin_for_window3].split('_')

    except Exception as e:
        raise e
        print('Error in funcion get_nach_date : ', e)
        return None






with open("/home/ramnaryanpanda/Downloads/with_category_vars_data_dafaf20 (1).json") as file:
    report_json = json.load(file)
print(get_nach_date_report(report_json))




















































# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data/"
# df = pd.DataFrame(columns=['client', 'file'])
# cnt = 0
# for folder in os.listdir(src_path):
#     if os.path.isdir(src_path+folder):
#         for file in os.listdir(src_path+folder):
#             try:
#                 df1 = pd.read_excel(src_path+folder+'/'+file)
#                 cnt+=1
#                 if len(df1[(df1['category']!=df1['category_2.0']) & ((df1['category']=='Salary') | (df1['category_2.0']=='Salary'))])>0:
#                     df.loc[len(df)] = [folder, file]
#                 if cnt%500==0:
#                     print(cnt)
#             except:
#                 print(file)
# df.to_excel("/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data/non_matching_salaries.xlsx", index=False)




# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data/mismatch/"
# df = pd.DataFrame(columns=['client', 'file'])
# cnt = 0
# lst = []
# for file in os.listdir(src_path):
#     try:
#         df1 = pd.read_excel(src_path+file)
#         cnt+=1
#         if len(df1[ (df1['category']!=df1['category_2.0']) & (df1['category_2.0'].str.lower().str.contains('loan') & (df1['category']=='Salary')) ])>0:
#             lst.append(file)
#     except:
#         print("except", file)
# print(len(lst))
# print(lst)




# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/user_data/"
# df = pd.DataFrame(columns=['client', 'file'])
# cnt = 0
# lst = []
# for file in os.listdir(src_path):
#     try:
#         df1 = pd.read_csv(src_path+file)
#         cnt+=1
#         if len(df1[ (df1['category']!=df1['category_2.0']) & (df1['category']=='Salary') & (df1['category_2.0'].str.lower().str.contains('loan')) ])>0:
#             lst.append(file)
#     except:
#         print("except", file)
# print(len(lst))
# print(lst)


# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/user_data/"
# files = os.listdir(src_path)
# files = sorted([file for file in files if file.replace('.csv', '').isdigit()])
# lst = []
# cnt = 0
# for file in files:
#     file_path = src_path+file
#     df = pd.read_csv(file_path)
#     month_diff = relativedelta.relativedelta(datetime.strptime(df['date'].max(), '%Y-%m-%d'), datetime.strptime(df['date'].min(), '%Y-%m-%d')).months
#     lst.append([file.replace('.csv', ''), month_diff,
#                 df[df['category_1.31'] == 'Salary'].shape[0],
#                 df[df['category_2.0']=='Salary'].shape[0],
#                 df[df['category'] == 'Salary'].shape[0],
#                 df[(df['category']=='Salary') & (df['category_2.0'].str.lower().str.contains('loan'))].shape[0]])
#     cnt+=1
#     # if cnt==1000:
#     #     break
#
# df = pd.DataFrame(lst, columns=['file', 'no_of_months', 'version_1.31', 'version_2.0', 'version_new', 'loans_as_salary'])
# df['is_v1.31_v2.0_old_match'] = (df['version_1.31']==df['version_2.0']).astype(str)
# df['is_v2.0_old_and_new_match'] = (df['version_2.0']==df['version_new']).astype(str)
# df['is_v1.31_v2.0_new_match'] = (df['version_1.31']==df['version_new']).astype(str)
#
# cols = ['file', 'no_of_months', 'version_1.31', 'version_2.0', 'is_v1.31_v2.0_earlier_match', 'version_new',
#         'is_v2.0_earlier_and_new_match', 'is_v1.31_v2.0_new_match', 'loans_as_salary']
#
# df.to_excel("/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/salary_comparison.xlsx", index=False)






# df = pd.read_excel("/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/salary_comparison.xlsx")
# df = df[(df['loans_as_salary']!=0) | (df['is_v2.0_old_and_new_match']==False)]
# print(df.shape)
# import shutil
# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/user_data/"
# df['file_name'] = src_path + df['file'].astype(str) + '.csv'
# for file in df['file_name']:
#     shutil.copyfile(file, "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/mismatch/"+file.split("/")[-1])



# src_path = "/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/mismatch/"
# for file in os.listdir(src_path):
#     if '.csv' in file:
#         df = pd.read_csv(src_path+file)
#         df.to_excel("/home/ramnaryanpanda/Documents/loan_salary_analysis/recent_data_new/mismatch1/"+file.replace('.csv','.xlsx'), index=False)






























