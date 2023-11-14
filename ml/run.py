from time import time
import logging
import pandas as pd
from ft_utils.transfer_in_sender import sender_info
from ft_utils.transfer_out_receiver import receiver_info
import copy
import re
from ft_utils.sub_category import SubCategory
import fasttext
import json
from ft_utils.preprocess import *
import concurrent.futures
from ft_utils.other_utils import get_upi_details, get_upi_id
from ft_utils.soft_logic import *
from ft_utils.salary_soft_logic import salary_with_out_keyword, loan_salary_with_out_keyword, find_employer
import warnings
warnings.filterwarnings('ignore')
logger = logging.getLogger('bank_recat_logger')
var_type = 'BANK_RECAT'

with open('./ft_utils/category_mapping_credit.json', 'r') as fp:
    ft_to_orig_mapping_credit = json.load(fp)
with open('./ft_utils/category_mapping_debit.json', 'r') as fp:
    ft_to_orig_mapping_debit = json.load(fp)

ft_to_orig_mapping = {}
ft_to_orig_mapping.update(ft_to_orig_mapping_credit)
ft_to_orig_mapping.update(ft_to_orig_mapping_debit)


class Categorise:

    @staticmethod
    def apply_salary_logic(df, is_loan_salary_check=False):
        try:
            model_detected_sal = df[df['category'] == 'salary'].index.tolist()

            if is_loan_salary_check:
                final_sal_idx, cluster_dict, ret_df = loan_salary_with_out_keyword(df)
            else:
                final_sal_idx, cluster_dict, ret_df = salary_with_out_keyword(
                    df[(df['category'].str.startswith('transfer')) | (df['category'] == 'salary')],
                )

            if final_sal_idx:
                df.loc[list(final_sal_idx), 'category'] = 'salary'
            if cluster_dict:
                df.loc[list(cluster_dict.keys()), 'cluster'] = list(cluster_dict.values())
            if model_detected_sal:
                df.loc[model_detected_sal, 'cluster'] = -1
            if not ret_df.empty:
                df.loc[ret_df.index, 'cleaned_narration_ft'] = ret_df['cleaned_narration_ft']
                df.loc[ret_df.index, 'sal_month'] = ret_df['sal_month']
                df.loc[ret_df.index, 'NER_prediction'] = ret_df['NER_prediction']

            # make salaries as rewards if salary amount is less than 0.4*max of salary of that particular month
            df['month'] = df['date'].dt.month
            max_salary_by_month = df[df['category']=='salary'].groupby('month')['amount'].max()
            # print(max_salary_by_month)
            for month, max_salary_amount in max_salary_by_month.iteritems():
                mask = (df['category'] == 'salary') & (df['month'] == month) & (df['amount'] < 0.4 * max_salary_amount)
                df.loc[mask, 'category'] = 'rewards&allowances'

            if 'month' in df.columns.tolist():
                df.drop(columns=['month'], inplace=True)

        except Exception as e:
            print(f"Exception in Salary Function is: {e}")
        return df

    @staticmethod
    def apply_all_soft_logic(df, funcs_to_apply):
        for func in funcs_to_apply:
            df['category'] = df[['narration', 'category', 'amount', 'balance']].apply(func, axis=1)
            df.loc[df.query('category!=keep_track_cat_change').index, 'function'] = func
            df['keep_track_cat_change'] = df['category']

    @staticmethod
    def data_cleanup(df_out):
        # where ever it salary and amount<3000 make them as rewards regardless of the salary keyword
        df_out.loc[(df_out['amount'] < 3000) & (df_out['category'] == 'salary'), 'category'] = 'rewards&allowances'
        df_out.loc[(df_out['amount'] <= 1) & (df_out['amount'] > 0) & (df_out['category'].str.contains('loan', flags=re.IGNORECASE)), 'category'] = 'transferin'
        df_out.loc[(df_out['amount'] >= -1) & (df_out['amount'] <= 0) & (df_out['category'].str.contains('loan', flags=re.IGNORECASE)), 'category'] = 'transferout'

        # if cleaned narration is empty then make it as transfer in / transfer out
        df_out.loc[(df_out['preproc_narration'].str.strip() == "") & (df_out['amount'] > 0), "category"] = "transferin"
        df_out.loc[(df_out['preproc_narration'].str.strip() == "") & (df_out['amount'] <= 0), "category"] = "transferout"

        # replace the category with the normal category
        df_out['model_pred_category'] = df_out['model_pred_category'].replace(ft_to_orig_mapping)
        df_out['category'] = df_out['category'].replace(ft_to_orig_mapping)

        df_out['category'] = df_out[['narration', 'category']].apply(sender_info, axis=1)
        df_out['category'] = df_out[['narration', 'category']].apply(receiver_info, axis=1)

        return df_out

    def __init__(self, data_type: str, apply_salary_logic: bool=False):

        self.data_type = data_type
        self.apply_salary_logic = apply_salary_logic

        if data_type == 'Debit':
            self.funcs_to_apply = (
                loan_insurance_investment_debit_soft_lofic,
                alcohol_bills_travel_wallet_debit_soft_logic,
                minbal_charge_debit_soft_logic,
                bounce_debit_soft_logic
            )

        elif data_type == 'Credit':
            self.funcs_to_apply = (
                reversal_cashdeposit_rewards_tax_credit_soft_logic,
                loan_investment_insurance_credit_soft_logic,
                salary_credit_soft_logic,
                bounce_credit_soft_logic
            )

    def apply(self, df):
        start_time = time()

        try:

            if self.data_type == 'Credit':
                model = fasttext.load_model("./categorization_models/ft_credit_model.bin")
                df['model_pred_category'] = df['preproc_narration'].map(lambda x: model.predict(x)[0][0].replace('__label__', ''))
                df['keep_track_cat_change'] = df['model_pred_category']
                df['category'] = df['model_pred_category']
                model_only_time = time()

                # apply all soft logic
                Categorise.apply_all_soft_logic(df, self.funcs_to_apply)
                soft_logic_time = time()

                # apply salary logic here
                if self.apply_salary_logic:
                    df = Categorise.apply_salary_logic(df, is_loan_salary_check=False)
                sal_logic_time = time()
                print(f"Time taken for Salary Soft logic: {sal_logic_time - model_only_time}")

            elif self.data_type == 'Debit':
                model = fasttext.load_model("./categorization_models/ft_debit_model.bin")
                df['model_pred_category'] = df['preproc_narration'].map(lambda x: model.predict(x)[0][0].replace('__label__', ''))
                df['model_pred_category'] = df['model_pred_category'].str.replace("bounced\xa0i/w\xa0ecscharges", 'bouncedi/wecscharges')
                df['keep_track_cat_change'] = df['model_pred_category']
                df['category'] = df['model_pred_category']
                model_only_time = time()

                # apply all soft logic
                Categorise.apply_all_soft_logic(df, self.funcs_to_apply)
                soft_logic_time = time()

            if self.data_type == 'Credit':
                print(f"credit total time={sal_logic_time - start_time}, "
                      f"credit_model_only_time={model_only_time - start_time}, "
                      f"credit_soft_log_time={soft_logic_time - model_only_time}")
            elif self.data_type == 'Debit':
                print(f"debit total time={soft_logic_time - start_time}, "
                      f"debit_model_only_time={model_only_time - start_time}, "
                      f"debit_soft_log_time={soft_logic_time - model_only_time}")

            return df

        except Exception as e:
            raise e
            print(f"Exception in {self.data_type} is: {e}")
            return None


def bankCategorization(bankdata, account_type='', sub_categorization=False, upi_id=False, upi_sub_category_data_df=None):
    input_cols = bankdata.columns.tolist()
    output_cols = ['category', 'employer', 'sub_category']
    start_time = time()

    try:
        print(bankdata.shape)
        bankdata['preproc_narration'] = bankdata['narration'].map(eval('clean_narration1'))
        bankdata['function'] = ''
        bankdata['cluster'] = ''
        bankdata['NER_prediction'] = ''
        bankdata['cleaned_narration'] = ''
        bankdata['cleaned_narration_ft'] = ''
        bankdata['sal_month'] = ''
        bankdata['employer'] = ''
        bankdata['category'] = ''
        bankdata['keep_track_cat_change'] = ''
        bankdata['model_pred_category'] = ''
        bankdata['seq_id'] = bankdata.index

        # check if we need to apply salary logic or not
        apply_salary_logic = True
        number_of_days_data = (bankdata['date'].astype('datetime64').max() - bankdata['date'].astype('datetime64').min()).days
        current_account_match = re.search(r"\bsme\b|small\W*enter|^ca\b|^cur\b|(c)?urrent|^cc\b", account_type.lower())
        if number_of_days_data<=32 or current_account_match:
            apply_salary_logic = False

        categorise_credit = Categorise(data_type="Credit", apply_salary_logic=apply_salary_logic)
        categorise_debit = Categorise(data_type="Debit")

        credit_df = bankdata[bankdata['amount'] >= 0]
        debit_df = bankdata[bankdata['amount'] < 0]

        futures_to_call = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit the functions to the executor for concurrent execution
            if not credit_df.empty:
                future1 = executor.submit(categorise_credit.apply, credit_df)
                futures_to_call.append(future1)

            if not debit_df.empty:
                future2 = executor.submit(categorise_debit.apply, debit_df)
                futures_to_call.append(future2)

        # Wait for both functions to complete
        concurrent.futures.wait(futures_to_call)
        if not credit_df.empty:
            credit_df = future1.result()
        else:
            credit_df = pd.DataFrame()
        if not debit_df.empty:
            debit_df = future2.result()
        else:
            debit_df = pd.DataFrame()

        df_out = pd.concat((credit_df, debit_df), axis=0).sort_index()

        if number_of_days_data>32 and pd.to_datetime(df_out[(df_out['category'] == 'loandisbursed') & (df_out['amount'] >= 8000)]['date']).dt.to_period('M').shape[0] > 2 or \
           pd.to_datetime(df_out[(df_out['category'] == 'insurance') & (df_out['amount'] >= 8000)]['date']).dt.to_period('M').shape[0] > 2 or \
           pd.to_datetime(df_out[(df_out['category'] == 'investmentincome') & (df_out['amount'] >= 8000)]['date']).dt.to_period('M').shape[0] > 2:
            df_out = Categorise.apply_salary_logic(df_out, is_loan_salary_check=True)

        df_out = Categorise.data_cleanup(df_out)

        # find employer for salaried records
        df_out.loc[df_out['category'] == 'Salary', 'employer'] = df_out.loc[df_out['category'] == 'Salary', 'narration'].apply(find_employer)

        # get sub category
        sub_category_obj = SubCategory()
        df_out = sub_category_obj.get_sub_category(df_out)

        # this will be set only when sub_category is off, when sub_category is on we can not do this
        if upi_id and not sub_categorization:
            df_out['upi_id'] = df_out['narration'].map(get_upi_id)
            df_out.loc[df_out['upi_id'].isna(), 'upi_id'] = ''

        # upi sub categorisation
        if sub_categorization and not upi_id:
            output_cols.extend(['merchant_name', 'upi_id', 'result_code'])
            formated_cols = df_out.columns.tolist() + ['merchant_name', 'upi_id', 'result_code']
            df_out_debit = get_upi_details(df_out[df_out['amount']<0], upi_sub_category_data_df)
            df_out_credit = df_out[df_out['amount']>=0]
            df_out = pd.concat((df_out_debit, df_out_credit), axis=0)[formated_cols]
            df_out.loc[df_out['sub_category'].isna(), 'sub_category'] = ''
            df_out.loc[df_out['merchant_name'].isna(), 'merchant_name'] = ''
            df_out.loc[df_out['upi_id'].isna(), 'upi_id'] = ''
            df_out.loc[df_out['result_code'].isna(), 'result_code'] = ''

        mask = ~(df_out['sub_category'].isin(['', 'Others']))
        df_out.loc[mask, 'category'] = df_out.loc[mask, 'sub_category']

        assert df_out.shape[0] == bankdata.shape[0]
        df_out = df_out.sort_values(by='seq_id')
        df_out.drop(columns=['seq_id'], inplace=True)

    except Exception as e:
        raise e
        df_out = None

    df_out = df_out[input_cols + output_cols]
    df_out.rename(columns={'cleaned_narration_ft': 'cleaned_narration_salary'}, inplace=True)
    print(f"Total time for Version 3.0={time() - start_time}")
    return df_out





