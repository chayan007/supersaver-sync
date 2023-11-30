import re
from fuzzywuzzy import fuzz
import pandas as pd


class MerchantNameMapper:
    def __init__(self):
        self.merchant_df = pd.read_csv('./ft_utils/new_merchant_mappings.csv')
        self.clean_name_lst = self.merchant_df['Report_Store_Name'].str.lower().unique().tolist()
        self.boundary_vars_pattern = re.compile(r'itc|uber|dell|nike|wow|lakme|puma|acer|biba|anish|1mg|for|simpl|cred', re.IGNORECASE)
        self.keyword_pattern = re.compile(
            r'itc.*(?=pvt|limited)|\bitc\b|\buber|(?:.*uber.*)\s?(?=rid)|(?=rid).*uber|\bdell\b|\bnike\b|\bwow\s?(?=skin|care|naturals)|\blakme\b|\bpuma\b|\bacer\b|\bbiba\b|\bbooking\b|\b1mg\b|\bforest\s?essentials\s?india\b|(?:simpl.*)(?=skin|care)|cred.*(?=club|club1|cc)')

    def _partial_fuzz_match(self, variation_tokens: str, threshold: int = 95):
        if not isinstance(variation_tokens, str) or len(variation_tokens) <= 2 or variation_tokens.lower() == 'unknown':
            return "NA"
        if re.search(r'\bbank\b', variation_tokens, re.I) or variation_tokens == 'bank':
            return "NA"

        if '@' in variation_tokens:
            variation_tokens = variation_tokens.split('@')[0]

        if '1mg' in variation_tokens:
            if re.search(r'(?<=tata)\s?1mg$', variation_tokens):
                return '1MG'
            else:
                return "NA"
        if 'uber' in variation_tokens:
            if re.search(r'.*uber.*\s?(?=rid)|(?=rid).*uber', variation_tokens):
                return 'Uber'

        matches = self.boundary_vars_pattern.findall(variation_tokens)

        if matches:
            max_match_score = max(fuzz.ratio(variation_tokens, match) for match in matches)
            threshold_1 = 60
            if max_match_score >= threshold_1 and self.keyword_pattern.search(variation_tokens):
                return max(matches, key=lambda match: fuzz.ratio(variation_tokens, match)).capitalize()
            elif max_match_score >= 40:
                return "NA"
            else:
                for match in matches:
                    match_pattern = r'\b' + re.escape(match.replace('%s', r'\w+')) + r'\b'
                    if re.search(match_pattern, variation_tokens, re.IGNORECASE) and self.keyword_pattern.search(variation_tokens):
                        return match.capitalize()
                return 'NA'

        max_score = -1
        best_match = None
        for clean_name in self.clean_name_lst:
            score = fuzz.partial_ratio(variation_tokens, clean_name)
            score1 = fuzz.ratio(variation_tokens.replace(' ', ''), clean_name.replace(' ', ''))
            if (score >= threshold or score1 >= threshold) and score > max_score:
                best_match = clean_name.capitalize()
                max_score = max(score, score1)

        return best_match

    def get_merchant_name(self, df):
        df['merchant_name_fuzzy'] = df['receiver_name'].str.lower().map(self._partial_fuzz_match, na_action='ignore')
        return df
