import re
import pandas as pd

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


def get_txn_id(row):
    try:
        narration, payment_mode = row.iloc[0].strip(), row.iloc[1]
        txn_id = ""
        match = None
        ifsc_regex = r"axo|axs|fbb|fbl|gsc|ibn|ici|icnu|in[0-9]{1}on|sbi|sin|srm|srw|tutr|axa|fbw|kumb|abhy|abna|abpb|adcb|adcc|airp|ain|ajar|ajhc|akjb|alla|amcb|amdn|andb|anzb|apbl|apgb|apgv|apmc|asbl|aubl|aucb|axi|axm|axn|axt|bacb|bara|barb|barc|bbkm|bcbm|bcey|bdbl|bkdn|bkid|bnp|bnsb|bofa|botm|cbin|ccbl|chas|citi|ciub|clbl|cnrb|corp|cosb|cres|crly|crub|csbk|csbx|ctba|ctcb|dbss|dcbl|deob|deut|dicg|dlsc|dlxb|dmkj|dnsb|dohb|durg|ebil|eibi|esfb|esmf|fdrl|fino|firn|fsfb|gbcb|gdcb|ggbk|gscb|harc|hcbl|hdfc|hpsc|hsbc|hvbk|ibbk|ibkl|ibko|icbk|icic|idfb|idib|iduk|indb|ioba|ipos|itbl|jaka|jana|jasb|jiop|jjsb|jpcb|jsbl|jsbp|jsfb|kace|kaij|kang|karb|kbkb|kcbl|kccb|kdcb|kgrb|kjsb|kkbk|klgb|knsb|koex|kolh|krth|ksbk|kscb|kucb|kvbl|kvgb|lavb|mahb|mahg|mcbl|mdbk|mdcb|mhcb|mkpb|msbl|msci|mshq|mslm|msnu|mubl|mvcb|nata|nbad|nbrd|ncub|nesf|ngsb|nicb|njbk|nkgs|nmcb|nmgb|nnsb|nosc|nspb|ntbl|nucb|nvnm|oiba|orbc|orcb|pjsb|pkgb|pmcb|pmec|prth|psib|pucb|punb|pusd|pytm|qnba|rbi|rabo|ratn|rbih|rbis|rmgb|rnsb|rrbp|rsbl|rscb|rssb|sabr|sahe|sant|sbin|sbls|scbl|sdcb|sdce|shbk|sibl|sidb|sidc|sjsb|sksb|smbc|smcb|snbk|soge|spcb|srcb|stcb|sunb|sury|susb|sutb|svbl|svcb|svsh|synb|tbsb|tdcb|tgmb|thrs|tjsb|tmbl|tnsc|tsab|tssb|ttcb|ubin|ucba|ujvn|uovb|upcb|urbn|utbi|utib|utks|uucb|vara|vasj|vcob|vijb|vsbl|vvsb|wbsc|wpac|yes|zcbl|zsbl"

        # if imps to or from then some numbers is present then remove this
        narration = re.sub(r"(imps|upi|imps_|upi_|transfer)\W*(to|from)\W*[0-9]+\W+", " ", narration, flags=re.I)
        # this is to handle things like
        # ....[0-9]\n[0-9] - replace with "" |  [a-z]\n - replace with " "
        narration = re.sub(r"([0-9])(\n)([0-9])", r"\1\3", narration, flags=re.I)
        narration = re.sub(r"\n", " ", narration, flags=re.I)
        # remove dates
        narration = re.sub(r"[0-9]{2}-[0-9]{2}-[0-9]{4}", " ", narration)
        # remove upi ids
        narration = re.sub(r"([0-9a-z.]@[a-z]{2,10})", " ", narration, flags=re.I)
        # this is to handle narrations like  RATN0000329#405006001234/IMPS/RATN/307427033076/PHYGICART
        narration = re.sub(r"[0-9a-z]{4,7}#[0-9]{12}", " ", narration, flags=re.I)
        # print(narration)

        if payment_mode == 'NEFT':
            match = re.search(
                r"(?:\W*)((" + ifsc_regex + r")\W*[a-z]{0,3}\s?[0-9]{8,}([a-z]{0,3}))(?:\W*)|(?:\W+)([0-9]{10,}dc)(?:\W+|$)|(?:\W+)((n|p|r|bd)([0-9M]{10,}))(?:\W+|$)|(?:\W+)((n|p|r|bd)([0-9]{15}))(?:\W*)|(?:\W+rrn\W+)([0-9]{10,})(?:\W+|neft)|(?:neft\W*(?:cr|dr)?\W+)([0-9]{12,})(?:\W+|$)",
                narration, flags=re.I)
            if not match:
                match = re.search(r"(?:neft\W*(?:cr|dr)?\W+)([0-9a-z]{15,16})(?:\W+|$)", narration, flags=re.I)
                if match:
                    _txn_id = [i for i in match.groups() if i][0]
                    if not len(re.findall(r"[0-9]", _txn_id)) > 8:
                        match = None

            if not match:
                match = re.search(
                    r"(?:neft\W+)([0-9]{12})(?:\W+|$)|(?:\W+)([0-9]{12})(?:\W+|$)|(?:\W+)(cms[0-9]{9,})(?:\W+|$)|(?:\W*)(cms[0-9]{10})(?:\W*)",
                    narration, flags=re.I)
            if not match:
                for _txn_id in re.split(r"\W+", narration):
                    # print(_txn_id)
                    if re.match(r"^[a-z0-9]{15,16}$|^[0-9]{12}$", _txn_id, flags=re.I) and len(
                            re.findall(r"[0-9]", _txn_id)) > 8:
                        return _txn_id

        elif payment_mode == 'IMPS':
            match = re.search(
                r"(?:(?:imps|imps_|upi|upi_|mbftb|mob|mb)\W*(?:reject|[a-z]+|rib\W*ft\W*rev|_rev|reversal)?\W*(?:p2a|p2p|tcc|rev|charge(?:s)?|credit|chg|fund\W*trf|rrn|txn)?(?:\d{2}\W*(?:[a-z]{1,4}|[0-9]{2})\W*\d{2})?\W*)([1-9][0-9]{11})(?:\W*)|(?:imps(?:[a-z]{1,2})?\W*(?:[0-9a-z]{1,4})\W*)(?<!imps\sfrom\s)(?<!imps\sto\s)([0-9]{12})(?:\W*)|(?:\W*)([1-9][0-9]{11})(?:\W*(?:imps|_imps))|(?:rrn\W*)([0-9]{12})(?:\W+|$)|(?:\W*(?:ref|reference)\W*(?:(?:no|num|number)|(?:#))?\W*)(?:[0-9])*([0-9]{12})(?:\W+|$|remark)|(?:imps\W*charges\W*for\W*(?:[0-9]*)\W*)([1-9][0-9]{11})(?:\W+|$)",
                narration, flags=re.I)
            # print(match.groups())
            # print(match)

        elif payment_mode == 'UPI':
            # print(narration)
            match = re.search(
                r"(?:(?:upi|upi_|upi\W*out|upi\W*in)\W*(?:dr|cr|trtr|in|rev|out|cradj|p2m|p2mpay|p2a|p2p|ret|return|rtn|rtrn|rvsl|cj|refund|rfnd|ref|reversal|failed|fail|credit|dispute)?(?:\W*[a-z]{1,3})?\W*)([0-9]{12})(?:(?:\W+)|(?:$))|(?:(?:" + ifsc_regex + r")(?:\W*)(?:[0-9a-z]{1,8}\W+)?)([1-9]{1}[0-9]{10,11})(?:\W+|$)|(?:\W*rrn\W*)([0-9]{12})(?:\W*)|(?:\W+|^)([0-9]{12})(?:(?:\W*upi$)|(?:\W+upi))|(?:\W+(?:ref|reference)\W*(?:no|num|number)?\W*(?:#)?\W*(?:[0-9]+)?\W*)([1-9]{1}[0-9]{11})",
                narration, flags=re.I)
            # print(narration)
            if not match:
                for num in re.split(r'\W+', narration):
                    # print(num)
                    match1 = re.search(r"(^[1-9][0-9]{11}$)", num)
                    if match1:
                        return match1.groups()[0]

            # this is for indusindbank
            if not match:
                match = re.search(r"(?:upi\W*)([0-9]{12})(?:\W+|$|cr|dr)", narration, flags=re.I)

            # bank of maharastra has narrations like    UPI 313127233497Merchant 20QR
            if not match:
                match = re.search(r"(?:(?:upi|upir)\W+)([0-9]{12})(?:(?:[a-z])|(?:$))", narration, flags=re.I)

        elif payment_mode == 'RTGS':
            match = re.search(
                r"(?:utr\W*no\W*)([a-z]{4,6}[0-9]+)(?:\W*)|((" + ifsc_regex + r")(\s)?([a-z]{1,3})?([0-9]{10,22}))|(?:rtgs\W+)([0-9]{12})(?:\W*)|(?:utr\W*)([0-9]{12,})(?:\W*)",
                narration, flags=re.I)

        elif payment_mode == 'Cheque':
            match = re.search(
                r"(?:(?:chq\W*(?:no|num|number|paid\W*(?:to)?|issu(?:e)?(?:d)?|dep(?:o)?(?:s)?(?:i)?(?:t)?(?:e)?(?:d)?)?\W*)|(?:(?:" + ifsc_regex + ")[a-z]+[0-9]+\W*))(?:bounce\W*)?([0-9]{5,6})(?:\W+|$)|(?:no|number|rtn|retn|return|charge(?:s)?|chg(?:s)?|chrg(?:s)?|refund|rfnd|incl(?:ude)?|gst)\W*([0-9]{5,8})|(?:\W+)([0-9]{5,7})(?:$)|(?:chq\W*)([0-9]{4,10})(?:\W*)",
                narration, flags=re.I)

        else:
            if not match:
                match = re.search(r"(?:\W*(?:ref|reference)\W*(?:(?:no|num|number)|(?:#))?\W*)(?:0)*([0-9]{12})(?:\W+|$)",
                                  narration, flags=re.I)
            # print(match)

        if match:
            txn_id = [i for i in match.groups() if i][0]

        if re.search(r"^0{3}", txn_id):
            txn_id = ""

        return txn_id if txn_id else ""

    except:
        return ""



if __name__=="__main__":
    df = pd.read_excel("/home/ramnaryanpanda/Documents/transaction_id_extraction/001_consolidated/payment_mode_wise_txn_id_oct_20/Others.xlsx")
    df['payment_mode'] = df[['narration', 'category']].apply(payment_mode_extraction, axis=1)
    df['txn_id'] = df[['narration', 'payment_mode']].apply(get_txn_id, axis=1)
    df.to_csv("/home/ramnaryanpanda/Documents/just_check2.csv", index=False)



