import re
import pandas as pd
import requests
import json
import time
# from utils import prod_config
import basicauth
import asyncio
import aiohttp
import requests

with open('./ft_utils/category_mapping_credit.json', 'r') as fp:
    ft_to_orig_mapping_credit = json.load(fp)
with open('./ft_utils/category_mapping_debit.json', 'r') as fp:
    ft_to_orig_mapping_debit = json.load(fp)


def payment_mode_extraction(row):
    try:
        narration, category = row.iloc[0], row.iloc[1].lower().replace(" ", "")
        narration_proc = narration.lower()

        if category == 'cashwithdrawal':
            return "ATM Transfer"
        elif category == 'cashdeposit':
            return "Cash Transfer"
        elif re.search('bounce', category.lower()):
            return "Others"

        all_modes = re.findall(
            r"mbimps|ftimps|mbft|a2aint|\btpt\b|\bach\b|\bach\W*c(?:r)\b|\bach\W*d(?:r)\b|\bifn\b|mobft|mandate|\bclg\b|by\W*clg|\bift\b|\beft\b|\bmps\b|\bbil\b|\bmpay\b|\becm\b|blkift|bulk\W*posting|cheque|\bnft\b|\bchq\b|\bcmp\b|\bcms\b|\becs\b|\bnach\b|nach\W*dr|\bimps\b|\binb\b|\binet\b|\binft\b|\bmbk\b|\bmob\b|\bneft\b|othpg|othpos|sbipg|sbipos|\bpos\b|\bprcr\b|\brtgs\b|\bupi\b|\bvisa\b|debit\W*card|\bonl\b|_upi|upi_|imps_|_imps|_rtgs|rtgs_|neft_|_neft|_nach|nach_|chq_|_chq",
            narration_proc) + re.findall(
            r"\bIB\b|\bMB\b|\bIMPS|IMPS\b|\bUPI|UPI\b|\bNEFT|NEFT\b|IMPS\b|\bIMPS|\bINB|INB\b|ACHD|POS[0-9]{4,}|UPI/[0-9]{6,}|^FT\W*-", narration)

        all_modes1 = all_modes

        if 'bil' in all_modes and len(all_modes) > 1:
            all_modes.remove('bil')
        elif len(all_modes) == 0:
            if re.search(r"transfer|^trfr|^trf/|by\W*transfer|to\W*transfer", narration_proc):
                return "Fund Transfer"
            return "Others"

        low_level_mode = re.sub("_", "", all_modes[0].lower())
        high_level_mode = "Others"

        mode_conversion = {r"^(?:n?)ach|\becs\b|\becm\b|\bcmp\b|mandate|achd": 'NACH',
                           r"mbimps|ftimps|mbft|ft\W*-|inft|\bib\b|inb|\beft\b|transfer|trf|\binet\b|a2aint|bulk\W*posting|\bcms\b|mobft|by\W*transfer|blkift|\btpt\b|\bonl\b|\bifn\b|\bift\b|othpg|sbipg": 'Fund Transfer',
                           r"imps|\bmb\b|\bmob\b|\bmbk\b|\bmpay\b|\bmps\b": "IMPS",
                           r"nft|neft": "NEFT",
                           r"rtgs": "RTGS",
                           r"\bupi\b|upi/[0-9]{6,}": "UPI",
                           r"chq|cheque|clg|by\W*clg": "Cheque",
                           r"visa|debit\W*card|othpos|sbipos|\bpos\b|pos[0-9]{4,}": "Debit Card"
                          }

        for key, val in mode_conversion.items():
            if re.search(key, low_level_mode):
                high_level_mode = val
                break

        if not high_level_mode:
            high_level_mode = "Others"

        if high_level_mode=='Others' and re.search(r"transfer|^trfr|^trf/|by\W*transfer|to\W*transfer", narration_proc):
            high_level_mode = "Fund Transfer"

        if high_level_mode not in ['UPI', 'RTGS', 'NEFT', 'IMPS']:
            for i in all_modes1:
                i = i.upper()
                if i in ['UPI', 'RTGS', 'NEFT', 'IMPS']:
                    high_level_mode = i

        return high_level_mode

    except:
        return "Others"


def find_valid_upi_handle(cur_handle):
    try:
        upi_handles = ['abfspay', 'airtel', 'allbank', 'amazonpay', 'andb', 'apgb', 'apl', 'aubank', 'aubl', 'axb',
                       'axis', 'axisb', 'axisbank',
                       'axisgo', 'axl', 'bandhan', 'barb', 'barodamp', 'barodampay', 'bdbl', 'bkid', 'bob', 'boi',
                       'cbin', 'cboi',
                       'centralbank', 'citi', 'ciub', 'cmsidfc', 'cnrb', 'csbpay', 'dbs', 'dcb', 'dcbl', 'denabank',
                       'dlb',
                       'eazypay', 'equitas', 'fbl', 'fbpe', 'fdrl', 'federal', 'finobank', 'freecharge', 'goaxb',
                       'hdfcbank',
                       'hsbc', 'ibl', 'icici', 'idbi', 'idfb', 'idfc', 'idfcbank', 'idfcfirst', 'idib',
                       'ikwik', 'imobile', 'indianbank', 'indus', 'iob', 'jaka', 'jio', 'jkb', 'jsb', 'jsbl',
                       'jupiteraxis',
                       'karb', 'karurvysyabank', 'kaypay', 'kbl', 'kkbk', 'kmbl', 'kotak', 'kvb', 'kvbank', 'kvbl',
                       'kvgb', 'lvb',
                       'mahb', 'mairtel', 'myicici', 'obc', 'okaxis', 'okbizaxis', 'okbizicici', 'okhdfcbank',
                       'okicici', 'oksbi',
                       'paytm', 'payzapp', 'pingpay', 'pnb', 'pockets', 'postbank', 'psb', 'rapl', 'ratn', 'rbl',
                       'rmhdfcbank',
                       's2b', 'sbi', 'sbls', 'scb', 'sib', 'sliceaxis', 'syndicate', 'tapicici', 'timecosmos', 'tjsb',
                       'tmbl',
                       'ubi', 'uboi', 'uco', 'ucobank', 'ujvn', 'unionbank', 'united', 'upi', 'utbi', 'utib', 'vijb',
                       'waaxis',
                       'wahdfcbank', 'waicici', 'wasbi', 'yapl', 'ybl', 'yesbank', 'yespay', 'yesbankltd', 'zoicici']

        if cur_handle != cur_handle or cur_handle == '':
            return None, None

        if cur_handle in upi_handles:
            return cur_handle, None

        possible_handles = []
        for upi_handle in upi_handles:
            len_to_match = min(len(upi_handle), len(cur_handle))
            if upi_handle == cur_handle:
                return cur_handle, None
            if upi_handle[:len_to_match] == cur_handle[:len_to_match]:
                possible_handles.append(upi_handle)
        #     print(possible_handles)
        if len(possible_handles) == 1:
            return possible_handles[0], None
        else:
            return None, None

    except Exception as e:
        return None, e


def get_upi_id(narr):
    try:
        # print(narr)
        if '@' in narr and 'upi' in narr.lower():
            narr = narr.lower()
            # preprocess to get the narration in format to handle
            narr = re.sub(r"@/", "@ /", narr)
            orig_narr = narr

            # if more than 1 @ are present, then take narrtion till the 2nd @
            if narr.count('@')>1:
                narr = narr[:list(re.finditer(r"@", narr))[1].start()]

            narr = re.findall(
                r"(/|:|-|upi\W*(?:from|to)|oid)([ 0-9a-zA-Z.*]+@[ 0-9a-zA-Z.*]+)(?:(?:\(|-|/|:|(\()?ref\b|,)|$)", narr)
            if len(narr) > 1:
                narr = narr[1][1]
            elif len(narr) == 1:
                narr = narr[0][1]
            else:
                return None

            if len(narr.split('@')[0]) == 1:
                narr = re.findall(
                    r"(/|:|upi\W*(?:from|to)|oid|-)([ 0-9a-zA-Z.*]+(-?)[ 0-9a-zA-Z.*]+@[a-zA-Z ]+)(?:(?:\(|-|/|:|(\()?ref\b|,)|$)",
                    orig_narr)
                # print("again narr", narr)
                if len(narr) > 1:
                    narr = narr[1][1]
                elif len(narr) == 1:
                    narr = narr[0][1]
                else:
                    return None

            # handlong one case for Paytm -  UPI-ABFLPOSTPAID-PAYTM-72651047@PAYTM-PYTM0123456-354766527940-OID21375470375@ONE (Ref# 0000354766527940)
            if narr.split('@')[1]=='paytm':
                if re.search(r"paytm\W*-\W*$", orig_narr[:orig_narr.find(narr)]):
                    narr = "paytm-"+narr

            # print("narr", narr)
            narr_proc = re.sub(r'(/|:|^\.)', '', narr).strip()
            narr_proc = narr_proc.strip()
            upi_name, upi_handle = narr_proc.replace(" ", "").split('@')
            upi_handle, exception = find_valid_upi_handle(upi_handle)
            if exception:
                return None

            upi_id = upi_name + '@' + upi_handle
            # here as upi can have max of size 20 for name, check if the name is more than 20 then return empty
            if len(upi_name) > 40 or len(upi_name) < 4 or '*' in upi_name or 'xxx' in upi_name or upi_handle == '':
                return None

            return upi_id

        else:
            return None

    except Exception as e:
        return None


def get_upi_id_only(df):
    try:
        if df.empty:
            raise ValueError("Passed df has length zero")
        df = df[df['amount']<0]
        if df.empty:
            raise ValueError("Passed df has no debit txns")

        df['upi_id'] = df['narration'].map(get_upi_id)
        unique_vpa_list = df.loc[~((df['upi_id'].isna()) | (df['upi_id'].str.strip()=='')), 'upi_id'].unique().tolist()
        if len(unique_vpa_list)==0:
            raise ValueError("Could not extract any upi_id for debit txns")
        print(f"Unique VPAs found {len(unique_vpa_list)}")
        return pd.DataFrame({'upi_id':unique_vpa_list})
    except Exception as e:
        print("Exception in get_only_upi_id func: ", e)
        return None
      

def get_upi_details(df, upi_response_lst, bank_data_id=""):

    batch_size = 25

    async def call_api(session, payload):
        client_id = '42165571'
        client_secret = 'lZ9MQS0HrbFdkmeYW4Fr5o79jTsaFVbK'
        url = 'https://svcstage.digitap.work/validation/bank/v1/upi-categorization'

        # client_id = prod_config.upi_client_id
        # client_secret = prod_config.upi_client_secret
        # url = prod_config.upi_url

        encoded_authorization = basicauth.encode(client_id, client_secret)
        headers = {
            "Authorization": encoded_authorization,
            "Content-Type": "application/json"
        }

        async with session.post(url, headers=headers, data=payload) as response:
            return await response.text()

    async def main():
        upi_response_lst = []
        async with aiohttp.ClientSession() as session:
            tasks = [call_api(session, payload) for payload in payloads]
            responses = await asyncio.gather(*tasks)

            for i, response_text in enumerate(responses):
                print(i)
                try:
                    # print(response_text)
                    response_dict = json.loads(response_text)
                    if response_dict['http_response_code'] == 200:
                        result_lst = response_dict['result']['vpa_details']
                        for dct in result_lst:
                            if dct["result_code"] == 101:
                                upi_response_lst.append((dct['vpa'], dct['entity_type'],
                                                         dct['account_holder_name'], dct['merchant_category'],
                                                         response_dict['request_id'], response_dict['client_ref_num'],
                                                         dct['result_code'], response_dict['http_response_code']))
                            else:
                                upi_response_lst.append((dct['vpa'], '', '', '',
                                                         response_dict['request_id'], response_dict['client_ref_num'],
                                                         dct['result_code'], response_dict['http_response_code']))
                    else:
                        raise Exception(str(response_dict['error']))
                except Exception as e:
                    upi_response_lst.extend([(vpa, '', '', '', response_dict['request_id'], response_dict['client_ref_num'],
                                              '', response_dict['http_response_code'])
                                             for vpa in unique_vpa_list[i*batch_size : (i+1)*batch_size]])
                    print("Got error: ", e)
                    print(response_text)
                    print(unique_vpa_list[i*batch_size : (i+1)*batch_size], "\n\n")

        return pd.DataFrame(upi_response_lst, columns=['upi_id', 'entity_type', 'merchant_name', 'MWT Cat Mapping',
                                                       'request_id', 'client_ref_num', 'result_code', 'http_response_code'])

    t1 = time.time()
    try:
        df['upi_id'] = df['narration'].map(get_upi_id)
        unique_vpa_list = df['upi_id'].dropna().unique().tolist()
        # unique_vpa_list = unique_vpa_list[:20]
        print(f"Unique VPAs found {len(unique_vpa_list)}")
        payloads = []
        for i in range(0, len(unique_vpa_list), batch_size):
            payload = json.dumps({
                "client_ref_num": bank_data_id + "_" + str(i),
                "vpa": unique_vpa_list[i:i + batch_size],
                "strategy":"2"   # 1->fetch from db,  2->using external api
            })
            payloads.append(payload)

        # loop = asyncio.get_event_loop()
        # upi_response_lst = loop.run_until_complete(main())
        # upi_response_lst.to_csv("./inp_data/9640764764_upi_response.csv")

        # upi_response_lst = pd.read_csv("./inp_data/1_fip_processed_da1b9b784_upi_response.csv")
        upi_cat_mapping_df = pd.read_csv("./ft_utils/upi_categorisation_mapping.csv").drop(columns=['MCC']).drop_duplicates()
        response_df = pd.DataFrame(upi_response_lst, columns=['upi_id', 'entity_type', 'merchant_name', 'MWT Cat Mapping',
                                                              'request_id', 'client_ref_num', 'result_code', 'http_response_code'])
        response_df['MWT Cat Mapping_proc'] = response_df['MWT Cat Mapping'].str.lower().str.replace(' ', '')
        upi_cat_mapping_df['MWT Cat Mapping_proc'] = upi_cat_mapping_df['MWT Cat Mapping'].str.lower().str.replace(' ', '')
        response_df = pd.merge(response_df, upi_cat_mapping_df, on='MWT Cat Mapping_proc', how='left')
        # print(response_df.columns)
        cols_to_take = df.columns.tolist()
        df = pd.merge(df, response_df, on='upi_id', how='left')
        df.loc[(df['Master Category'].isin(ft_to_orig_mapping_credit.values())) & (df['amount']>=0), 'category'] = df.loc[(df['Master Category'].isin(ft_to_orig_mapping_credit.values())) & (df['amount']>=0), 'Master Category']
        df.loc[(df['Master Category'].isin(ft_to_orig_mapping_debit.values())) & (df['amount']<0), 'category'] = df.loc[(df['Master Category'].isin(ft_to_orig_mapping_debit.values())) & (df['amount']<0), 'Master Category']

        # if some category is coming which is not present in our category list then make it as transfer
        df.loc[(~df['Master Category'].isin(ft_to_orig_mapping_credit.values())) & (~df['Master Category'].isna()) & (df['Master Category'].str.strip()!='') & (df['amount']>=0), 'category'] = "Transfer from " + df.loc[(~df['Master Category'].isin(ft_to_orig_mapping_credit.values())) & (~df['Master Category'].isna()) & (df['Master Category'].str.strip()!='') & (df['amount']>=0), 'merchant_name']
        df.loc[(~df['Master Category'].isin(ft_to_orig_mapping_debit.values())) & (~df['Master Category'].isna()) & (df['Master Category'].str.strip()!='') & (df['amount']<0), 'category'] = "Transfer to " + df.loc[(~df['Master Category'].isin(ft_to_orig_mapping_debit.values())) & (~df['Master Category'].isna()) & (df['Master Category'].str.strip()!='') & (df['amount']<0), 'merchant_name']

        df.loc[(df['entity_type']=='INDIVIDUAL')&(df['amount']>=0), 'category'] = "Transfer from " + df.loc[(df['entity_type']=='INDIVIDUAL')&(df['amount']>=0), 'merchant_name']
        df.loc[(df['entity_type'] == 'INDIVIDUAL')&(df['amount']<0), 'category'] = "Transfer to " + df.loc[(df['entity_type'] == 'INDIVIDUAL')&(df['amount']<0), 'merchant_name']
        df.loc[(df['entity_type'] == 'INDIVIDUAL'), 'sub_category'] = 'INDIVIDUAL'
        df.loc[(df['entity_type'] == 'MERCHANT') & (df['sub_category'].isna()), 'sub_category'] = 'Others'

        df = df[cols_to_take + ['merchant_name', 'sub_category', 'request_id', 'client_ref_num', 'result_code', 'http_response_code']]

    except Exception as e:
        print("Final Exception in function get_upi_details is: ", e)
        # raise e
        df['merchant_name'] = ''
        df['sub_category'] = ''
        df['request_id'] = ''
        df['client_ref_num'] = ''
        df['result_code'] = ''
        df['http_response_code'] = ''

    # handle null cases for null
    if 'upi_id' in df.columns.tolist():
        df['upi_id'].fillna("", inplace=True)

    print("UPI details time taken: ", time.time() - t1)
    return df













