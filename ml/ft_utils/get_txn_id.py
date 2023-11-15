import re
import pandas as pd


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

            if not match:
                # print("here", narration)
                match = re.search(r"(IN[0-9]{5,}[0-9a-zA-Z]{5,})(?:LOAN)", narration)
                # print(match)

        elif payment_mode == 'IMPS':
            match = re.search(
                r"(?:imps\W*(?:inward|outward)\W*.*(?:ref|reference)\W*(?:no|num|number)\W*)([0-9]{12})|(?:upi\W*topaytmqr.*(?:ref|reference)\W*(?:no|num|number)\W*)([0-9]{12})|(?:(?:imps|imps_|upi|upi_|mbftb|mob|mb)\W*(?:reject|[a-z]+|rib\W*ft\W*rev|_rev|reversal)?\W*(?:p2a|p2p|tcc|rev|charge(?:s)?|credit|chg|fund\W*trf|rrn|txn)?(?:\d{2}\W*(?:[a-z]{1,4}|[0-9]{2})\W*\d{2})?\W*)([1-9][0-9]{11})(?:\W*)|(?:imps(?:[a-z]{1,2})?\W*(?:[0-9a-z]{1,4})\W*)(?<!imps\sfrom\s)(?<!imps\sto\s)([0-9]{12})(?:\W*)|(?:\W*)([1-9][0-9]{11})(?:\W*(?:imps|_imps))|(?:rrn\W*)([0-9]{12})(?:\W+|$)|(?:\W*(?:ref|reference)\W*(?:(?:no|num|number)|(?:#))?\W*)(?:[0-9])*([0-9]{12})(?:\W+|$|remark)|(?:imps\W*charges\W*for\W*(?:[0-9]*)\W*)([1-9][0-9]{11})(?:\W+|$)",
                narration, flags=re.I)
            # if not match:
            #     match = re.search(r"(?:imps\W*(?:inward|outward)\W*.*(?:ref|reference)\W*(?:no|num|number)\W*)([0-9]{12})", narration, flags=re.I)

        elif payment_mode == 'UPI':
            # print(narration)
            match = re.search(r"(?:(?:upi|upi_|upi\W*out|upi\W*in)\W*(?:dr|cr|trtr|in|rev|out|cradj|p2m|p2mpay|p2a|p2p|ret|return|rtn|rtrn|rvsl|cj|refund|rfnd|ref|reversal|failed|fail|credit|dispute)?(?:\W*[a-z]{1,3})?\W*)([0-9]{12})(?:(?:\W+)|(?:$))|(?:(?:" + ifsc_regex + r")(?:\W*)(?:[0-9a-z]{1,8}\W+)?)([1-9]{1}[0-9]{10,11})(?:\W+|$)|(?:\W*rrn\W*)([0-9]{12})(?:\W*)|(?:\W+|^)([0-9]{12})(?:(?:\W*upi$)|(?:\W+upi))|(?:\W+(?:ref|reference)\W*(?:no|num|number)?\W*(?:#)?\W*(?:[0-9]+)?\W*)([1-9]{1}[0-9]{11})|(?:money\W*(?:sent|received))(?:(?:.*)reference\W*number\W*)([1-9]{1}[0-9]{10,})|(?:upi_(?:c|d)_\W*)([0-9]{12})",
                narration, flags=re.I)
            # print(match)
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
            # print(match.groups())
            txn_id = [i for i in match.groups() if i][0]

        if re.search(r"^0{3,}", txn_id):
            txn_id = ""

        return txn_id if txn_id else ""

    except Exception as e:
        print("Exception in txn_id func: ", e)
        return ""



df = pd.DataFrame({
    'narration':['IMPS INWARD ORG IMPSTO from FIDUCIARY BILLINGSOLUTION DIV YES BANK REF NO: - 305721935961CASH WITHDRAWAL @POS'],
    'category':['IMPS']
})


print(df.apply(get_txn_id, axis=1))



