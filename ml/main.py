import pandas as pd
from run import bankCategorization
import json




if __name__=='__main__':
    file_path = "1_fip_processed_da1b9b784.json"
    with open("./inp_data/" + file_path, 'r') as file:
        data = json.load(file)

    df = bankCategorization(data, account_type='', sub_categorization=True, upi_id=True, upi_sub_category_data_df=True)
    df.to_csv("./out_data/" + file_path.replace('.json', '') + '_out' + '.csv', index=False)

