import pandas as pd
from run import bankCategorization

df = pd.read_csv("/home/ramnaryanpanda/Documents/just_check.csv")
df['date'] = df['date'].astype('datetime64')
df = bankCategorization(df, account_type='', sub_categorization=True, upi_id=True, upi_sub_category_data_df=True)
df.to_csv("/home/ramnaryanpanda/Documents/just_check_out.csv", index=False)

