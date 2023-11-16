import pandas as pd
from run import bankCategorization
import json




if __name__=='__main__':

    # read input files
    file_path = "1_fip_processed_da1b9b784.json"
    with open("./inp_data/" + file_path, 'r') as file:
        data = json.load(file)
    upi_sub_category_data_df = pd.read_csv("/home/ramnaryanpanda/Downloads/hackhack1/supersaver-sync/ml/inp_data/1_fip_processed_da1b9b784_upi_response.csv")

    user_df, vendor_agg_df, asset_agg_df, liab_agg_df, neg_event_agg_df = \
        bankCategorization(data, account_type='', sub_categorization=True, upi_sub_category_data_df=upi_sub_category_data_df)
    user_df.to_csv("./out_data/user_data.csv", index=False)

    def save_df_to_json_format(file_path, df):
        data = df.to_json(orient='records')
        with open(file_path, 'w') as file:
            json.dump(json.loads(data), file, indent=4)

    save_df_to_json_format("./out_data/user_data.json", user_df)
    save_df_to_json_format("./out_data/vendor_agg_data.json", vendor_agg_df)
    save_df_to_json_format("./out_data/asset_agg_data.json", asset_agg_df)
    save_df_to_json_format("./out_data/liab_agg_data.json", liab_agg_df)
    save_df_to_json_format("./out_data/neg_event_agg_data.json", neg_event_agg_df)











