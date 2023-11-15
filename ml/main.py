import pandas as pd
from run import bankCategorization
import json




if __name__=='__main__':
    file_path = "1_fip_processed_da1b9b784.json"
    with open("./inp_data/" + file_path, 'r') as file:
        data = json.load(file)

    df, df1, df2 = bankCategorization(data, account_type='', sub_categorization=True, upi_id=True, upi_sub_category_data_df=True)
    # df.to_csv("./out_data/" + file_path.replace('.json', '') + '_out' + '.csv', index=False)
    # df1.to_csv("./out_data/" + file_path.replace('.json', '') + '_out1' + '.csv', index=False)
    # df2.to_csv("./out_data/" + file_path.replace('.json', '') + '_out2' + '.csv', index=False)

    df.to_json("./out_data/user_data.json", orient='records')
    df1.to_json("./out_data/categorywise_agg_data.json", orient='records')
    df2.to_json("./out_data/vendorwise_agg_data.json", orient='records')

