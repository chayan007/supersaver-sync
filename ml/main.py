import pandas as pd
from run import bankCategorization
import json


def make_user_json(df, data):
    df.sort_values(by='seq', inplace=True)
    asset_or_liab = df['liab_or_asset'].tolist()
    category_lst = df['category'].tolist()
    vendor_lst = df['vendor'].tolist()
    sub_category_lst = df['sub_category'].tolist()
    receiver_name_lst = df['receiver_name'].tolist()
    cnt = 0

    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                masked_acc = value[0].get('masked_account')
                if 'decrypted_data' in item:
                    try:
                        transactions = item['decrypted_data']['Account'].get('Transactions', {}).get('Transaction', [])
                        transactions = [transactions] if isinstance(transactions, dict) else transactions

                        for transaction in transactions:
                            transaction['category'] = category_lst[cnt]
                            transaction['asset_or_liab'] = asset_or_liab[cnt]
                            transaction['vendor'] = vendor_lst[cnt]
                            transaction['sub_category'] = sub_category_lst[cnt]
                            transaction['receiver_name'] = receiver_name_lst[cnt]
                            cnt+=1
                    except Exception as e:
                        # print("here I go on the road again", transaction)
                        raise e

    return data


if __name__=='__main__':

    # read input files
    file_path = "9640764764.json"
    with open("./inp_data/" + file_path, 'r') as file:
        data = json.load(file)
    upi_sub_category_data_df = pd.read_csv("./inp_data/" + file_path.replace(".json", "") + "_upi_response.csv")

    user_df, vendor_agg_df, asset_agg_df, liab_agg_df, neg_event_agg_df = \
        bankCategorization(data, account_type='', sub_categorization=True, upi_sub_category_data_df=upi_sub_category_data_df)
    user_df.to_csv("./out_data/user_data.csv", index=False)

    data = make_user_json(user_df, data)
    with open('./out_data/user_data.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    def save_df_to_json_format(file_path, df):
        data = df.to_json(orient='records')
        with open(file_path, 'w') as file:
            json.dump(json.loads(data), file, indent=4)

    # save_df_to_json_format("./out_data/user_data.json", user_df)
    save_df_to_json_format("./out_data/vendor_agg_data.json", vendor_agg_df)
    save_df_to_json_format("./out_data/asset_agg_data.json", asset_agg_df)
    save_df_to_json_format("./out_data/liab_agg_data.json", liab_agg_df)
    save_df_to_json_format("./out_data/neg_event_agg_data.json", neg_event_agg_df)











