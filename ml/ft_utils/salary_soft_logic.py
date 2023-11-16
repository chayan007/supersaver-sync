import pandas as pd
import re
from datetime import datetime
from nltk.tokenize import RegexpTokenizer
from fuzzywuzzy import fuzz
import fasttext
import logging
from time import time
import warnings
import pylcs
from itertools import product
warnings.filterwarnings('ignore')
tokenizer = RegexpTokenizer(r'\w+')

logger = logging.getLogger('bank_recat_logger')
var_type = 'BANK_RECAT'

name_comp_model = ""


def get_exact_company(orig_narr, cleaned_narration_ft):
    # print("inside get comp", orig_narr, "---", cleaned_narration_ft)
    final_st = ""
    if orig_narr != '' and cleaned_narration_ft != '':
        for i in cleaned_narration_ft.lower().split(" "):
            pos = orig_narr.lower().find(i)
            if pos != -1:
                final_st += orig_narr[pos:pos + len(i)] + ' '
            # print(final_st, pos, pos+len(i)+1)
        cleaned_narration_ft = re.sub(r"\s+", " ", final_st.strip())
    # print("exact name", cleaned_narration_ft)
    return cleaned_narration_ft


def name_or_comp_pred(cleaned_narration, name_comp_model):
    if re.search(r'myloancare|\bcorp\b|market|\btech|plant|plastic|uber|india|enter()?p|trade|corporate|diagnos|service|\bpvt\b|made|\bfood\b|\bltd\b|private|limit|\bpriv(a)?\b|\bsol\b|solution|business|engine|jewel|\bfina\b|finan|motor|maruti', cleaned_narration.lower()):
            return '__label__company', 1.0
    if len(cleaned_narration.split(' ')) >= 2:
        a = cleaned_narration.split(' ')
        res = ' '.join(j for j in a[1:])
        pred = name_comp_model.predict(res)
        if pred[1][0] < 0.70 and pred[0][0] == '__label__name':
            return "__label__company", pred[1][0]
        else:
            return pred[0][0], pred[1][0]
    else:
        pred = name_comp_model.predict(cleaned_narration)
        return pred[0][0], pred[1][0]



def find_employer(narr):
    # print("=================narr", narr)
    narr = re.sub(r"\n", "", narr)
    narr = re.sub(r"\b(\w) (?=\w\b)", r"\1", narr)
    orig_narration = narr
    narr = narr.lower()
    cleaned_narration_ft = ""
    try:
        CUSTOM_STOPWORDS_FT = ['ref', 'ifsc', 'tpt', 'trf', 'by transfer', 'inb', 'tfr', 'inf', 'cardlessdeposit',
                               'cardless deposit', 'inft', 'icsp', 'trfr', 'icsp', 'frm', 'inet', 'cms', 'rtgs',
                               'impsab', 'period',
                               'bank', 'icici', 'hdfc', 'sbi', 'axis', 'canara', 'payment', 'tfrinb', 'ebfs', 'total',
                               'dcpos',
                               'neft', 'imps', 'upi', 'cash', 'atm', 'pos', 'p2a', 'ach', 'transfer', 'csp', 'outlet',
                               'from', 'net', 'acct', 'csv', 'txt', 'test', 'text', 'achcr', 'tfrneft', 'eba', 'ebank',
                               'moneytrf', 'sbin', 'opening', 'balance', 'january', 'february', 'march', 'april', 'may',
                               'june', 'july', 'august', 'september',
                               'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug',
                               'sep',
                               'oct', 'nov', 'dec', 'sept', 'cr', 'null', 'neft', 'imps', 'ne', 'neftcr', 'shree',
                               'state',
                               'ban', 'attn', 'outward', 'icic', 'sbil', 'in', 'posting', 'bulk', 'etpc', 'blkift',
                               'blkpay']

        ifsc_set = {'abhy', 'abna', 'abpb', 'adcb', 'adcc', 'airp', 'ajar', 'ajhc', 'akjb', 'alla', 'amcb', 'amdn',
                    'andb', 'anzb', 'apbl', 'apgb', 'apgv', 'apmc', 'asbl', 'aubl', 'aucb', 'bacb', 'bara', 'barb',
                    'barc', 'bbkm', 'bcbm', 'bcey', 'bdbl', 'bkdn', 'bkid', 'bnpa', 'bnsb', 'bofa', 'botm', 'cbin',
                    'ccbl', 'chas', 'citi', 'ciub', 'clbl', 'cnrb', 'cosb', 'cres', 'crly', 'crub', 'csbk', 'csbx',
                    'ctba', 'ctcb', 'dbss', 'dcbl', 'deob', 'deut', 'dicg', 'dlsc', 'dlxb', 'dmkj', 'dnsb', 'dohb',
                    'durg', 'ebil', 'eibi', 'esfb', 'esmf', 'fdrl', 'fino', 'firn', 'fsfb', 'gbcb', 'gdcb', 'ggbk',
                    'gscb', 'harc', 'hcbl', 'hdfc', 'hpsc', 'hsbc', 'hvbk', 'ibbk', 'ibkl', 'ibko', 'icbk', 'icic',
                    'idfb', 'idib', 'iduk', 'indb', 'ioba', 'ipos', 'itbl', 'jaka', 'jana', 'jasb', 'jiop', 'jjsb',
                    'jpcb', 'jsbl', 'jsbp', 'jsfb', 'kace', 'kaij', 'kana', 'kang', 'karb', 'kbkb', 'kcbl', 'kccb',
                    'kdcb', 'kgrb', 'kjsb', 'kkbk', 'klgb', 'knsb', 'koex', 'kolh', 'krth', 'ksbk', 'kscb', 'kucb',
                    'kvbl', 'kvgb', 'lavb', 'mahb', 'mahg', 'mcbl', 'mdbk', 'mdcb', 'mhcb', 'mkpb', 'msbl', 'msci',
                    'mshq', 'mslm', 'msnu', 'mubl', 'mvcb', 'nata', 'nbad', 'nbrd', 'ncub', 'nesf', 'ngsb', 'nicb',
                    'njbk', 'nkgs', 'nmcb', 'nmgb', 'nnsb', 'nosc', 'nspb', 'ntbl', 'nucb', 'nvnm', 'oiba', 'orbc',
                    'orcb', 'payt', 'pjsb', 'pkgb', 'pmcb', 'pmec', 'prth', 'psib', 'pucb', 'punb', 'pusd', 'pytm',
                    'qnba', 'rabo', 'ratn', 'rbih', 'rbis', 'rmgb', 'rnsb', 'rrbp', 'rsbl', 'rscb', 'rssb', 'sabr',
                    'sahe', 'sant', 'sbin', 'sbls', 'scbl', 'sdcb', 'sdce', 'shbk', 'sibl', 'sidb', 'sidc', 'sjsb',
                    'sksb', 'smbc', 'smcb', 'snbk', 'soge', 'spcb', 'srcb', 'stcb', 'sunb', 'sury', 'susb', 'sutb',
                    'svbl', 'svcb', 'svsh', 'synb', 'tbsb', 'tdcb', 'tgmb', 'thrs', 'tjsb', 'tmbl', 'tnsc', 'tsab',
                    'tssb', 'ttcb', 'ubin', 'ucba', 'ujvn', 'uovb', 'upcb', 'urbn', 'utbi', 'utib', 'utks', 'uucb',
                    'vara', 'vasj', 'vcob', 'vijb', 'vsbl', 'vvsb', 'wbsc', 'wpac', 'yesb', 'zcbl', 'zsb'}

        #         narr = re.sub(r"\s+", " ", re.sub(r"[0-9]+", "", narr))
        #         narr = re.sub(r'''(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(?:_2022)''', " ", narr)
        #         narr = re.sub(r'''\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b''', " ", narr)
        #         narr = re.sub(r'''(month|for|s(a)?al(l)?(a|e)?(i)?r(y|ie)?(s)?)(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)''', " ", narr)
        #         narr = re.sub(r'''januar(a)?(y)?|febru|march|april|\bmay\b|june|july|august|augus|septem|octob|novemb|decemb''', " ", narr)
        #         narr = re.sub(r"(indian|axis|deutsche|hdfc|icici)( )?bank( ltd)?|arrear(s)?|pfms|through|money received|received", "", narr)
        #         narr = re.sub(r"\W+", " ", re.sub(r'\b(abhy|abna|abpb|adcb|adcc|airp|ajar|ajhc|akjb|alla|amcb|amdn|andb|anzb|apbl|apgb|apgv|apmc|asbl|aubl|aucb|bacb|bara|barb|barc|bbkm|bcbm|bcey|bdbl|bkdn|bkid|bnpa|bnsb|bofa|botm|cbin|ccbl|chas|citi|ciub|clbl|cnrb|cosb|cres|crly|crub|csbk|csbx|ctba|ctcb|dbss|dcbl|deob|deut|dicg|dlsc|dlxb|dmkj|dnsb|dohb|durg|ebil|eibi|esfb|esmf|fdrl|fino|firn|fsfb|gbcb|gdcb|ggbk|gscb|harc|hcbl|hdfc|hpsc|hsbc|hvbk|ibbk|ibkl|ibko|icbk|icic|idfb|idib|iduk|indb|ioba|ipos|itbl|jaka|jana|jasb|jiop|jjsb|jpcb|jsbl|jsbp|jsfb|kace|kaij|kana|kang|karb|kbkb|kcbl|kccb|kdcb|kgrb|kjsb|kkbk|klgb|knsb|koex|kolh|krth|ksbk|kscb|kucb|kvbl|kvgb|lavb|mahb|mahg|mcbl|mdbk|mdcb|mhcb|mkpb|msbl|msci|mshq|mslm|msnu|mubl|mvcb|nata|nbad|nbrd|ncub|nesf|ngsb|nicb|njbk|nkgs|nmcb|nmgb|nnsb|nosc|nspb|ntbl|nucb|nvnm|oiba|orbc|orcb|payt|pjsb|pkgb|pmcb|pmec|prth|psib|pucb|punb|pusd|pytm|qnba|rabo|ratn|rbih|rbis|rmgb|rnsb|rrbp|rsbl|rscb|rssb|sabr|sahe|sant|sbin|sbls|scbl|sdcb|sdce|shbk|sibl|sidb|sidc|sjsb|sksb|smbc|smcb|snbk|soge|spcb|srcb|stcb|sunb|sury|susb|sutb|svbl|svcb|svsh|synb|tbsb|tdcb|tgmb|thrs|tjsb|tmbl|tnsc|tsab|tssb|ttcb|ubin|ucba|ujvn|uovb|upcb|urbn|utbi|utib|utks|uucb|vara|vasj|vcob|vijb|vsbl|vvsb|wbsc|wpac|yesb|zcbl|zsbl)(.*?)\b', "", narr.lower()))

        ref_num_search = re.findall("ref# [a-zA-Z0-9]*", narr)
        narr = re.sub(r"by\s+clg\s+inst", " ", narr)
        # print("after clg", narr)
        if ref_num_search:
            narr = narr.replace("(" + ref_num_search[0] + ")", "").strip()
            ref_num_search = ref_num_search[0].replace('ref#', '').strip()
            narr = narr.split('ref#')[0]
            cleaned_narration_ft = narr.replace(ref_num_search, '').strip()

        # print(narr)
        # print("before calling if", orig_narration, "\n\n")

        which_regex = ""

        if narr.startswith("a2aint"):
            # print("here in a2aint")
            positions = list(re.finditer(r"-", narr))
            if len(positions) > 1:
                # print("here in a2aint again")
                pos_of_txt_to_extract = narr[positions[0].start() + 1:positions[1].start()]
                cleaned_narration_ft = re.sub(r'[0-9]', '', pos_of_txt_to_extract)
                which_regex = "a2aint"
            elif len(positions) == 1:
                # print("here in a2aint again")
                pos_of_txt_to_extract = narr[positions[0].start() + 1:]
                cleaned_narration_ft = re.sub(r'[0-9]', '', pos_of_txt_to_extract)
                which_regex = "a2aint"

        elif orig_narration.startswith("CMS/"):
            # print("inside cms")
            cleaned_narration_ft = orig_narration.split('/')[-1]
            which_regex = '^cms'
            # print(cleaned_narration_ft)

        elif orig_narration.startswith("EBANK:WIB"):
            cleaned_narration_ft = orig_narration.split('/')[-1]
            which_regex = 'ebank:wib'
            # print(cleaned_narration_ft)


        elif re.search(r"^[0-9]{6,}-tpt", narr.replace(" ", "")):
            narr = re.sub(r"-[0-9]{2}-", "-", narr)
            positions = list(re.finditer(r"-", narr))
            if len(positions) >= 3:
                # print("elif31")
                narr = narr[positions[2].start() + 1:]
                cleaned_narration_ft = narr
            if narr == '' and len(positions) >= 2:
                # print("elif32")
                cleaned_narration_ft = narr[positions[1].start() + 1:positions[2].start() + 1]
            # print("cleaned_narration_ft", cleaned_narration_ft)
            which_regex = "tpt"

        elif re.search(r"^cms-tpt-[a-z]{1,}[0-9]{6,}", narr.replace(" ", "")):
            positions = list(re.finditer(r"-", narr))
            if len(positions) >= 4:
                cleaned_narration_ft = narr.split("-")[-1]
                which_regex = "cms tpt"

        elif re.search(r"(?:^ach\W?)(?:credit|cr|c|sal)?(?:\W+)(?:sal\W+)?(.*?)(?:\-|/)", orig_narration.lower()):
            cleaned_narration_ft = \
                re.findall(r"(?:^ach\W?)(?:credit|cr|c|sal)?(?:\W+)(?:sal\W+)?(.*?)(?:\-|/)", orig_narration.lower())[0]
            which_regex = "^ach"

        elif re.search(r"(?<=^bt).*?(?=standard( )?char)", narr):
            # print("bt standrd func")
            cleaned_narration_ft = re.search(r"(?<=^bt).*?(?=standard( )?char)", narr).group(0)
            which_regex = "standard chart"

        elif narr.startswith(r"bulk posting-"):
            # print("bulk posting")
            positions = list(re.finditer(r"-", narr))
            if len(positions) >= 2:
                narr = narr.split("-")[1]
                narr = re.sub(r"[0-9]", "", narr)

            if re.search(r"[a-z]{1,4}", narr) and len(narr) < 10:
                # print('inside bulk posting if')
                cleaned_narration_ft = ""
            else:
                # print('inside bulk posting else')
                cleaned_narration_ft = narr
            which_regex = "bulk posting"

        elif re.search(r"(?:money\W*received\W*(?:using)?\W*(?:imps)?received\W*from)(.*?)(?:a/c|account|transa)",
                       orig_narration.lower()):
            cleaned_narration_ft = \
                re.findall(r"(?:money\W*received\W*(?:using)?\W*(?:imps)?received\W*from)(.*?)(?:a/c|account|transa)",
                           orig_narration.lower())[0]
            which_regex = "money rcvd paytm"

        elif re.search(r"(?:^by transfer\W+)(?:neft)(?:(?:\*.*?)(?=\*)){1,2}(?:\*)(.*?)(?=\*|\(ref|\-)",
                       orig_narration.lower()):
            # print("by transfer neft")
            cleaned_narration_ft = \
                re.findall(r"(?:^by transfer\W+)(?:neft)(?:(?:\*.*?)(?=\*)){1,2}(?:\*)(.*?)(?=\*|\(ref|\-)",
                           orig_narration.lower())[0]
            which_regex = "by transfer3"

        elif re.search(r"^by transfer.*?transfer from( )?[0-9]{4,}(.*)", narr) and not re.search('neft|imps', narr):
            # print("by transfer and not neft")
            cleaned_narration_ft = re.findall(r"^by transfer.*?transfer from( )?[0-9]{4,}(.*)", narr)[0][1]
            # print("this is by transfer", cleaned_narration_ft)
            which_regex = "by transfer1"

        elif re.search(r"^by transfer-(?:.*?)-(.*?)-(?:\s)?\(?ref(?:\s)?#.*\)?",
                       orig_narration.lower()) and not re.search('neft|imps', narr):
            # print("by transfer and not neft but with ref num")
            cleaned_narration_ft = \
                re.findall(r"^by transfer-(?:.*?)-(.*?)-(?:\s)?\(?ref(?:\s)?#.*\)?", orig_narration.lower())[0]
            which_regex = "by transfer2"

        elif re.search(r"^neft cr", orig_narration.lower()):
            # print("inside ^neft cr")
            orig_narration1 = orig_narration
            if re.search(r"(?:^neft cr\W?)(?:(?:\-(?:.*?)[0-9]+(?:.*?))(?=\-)){1,2}(?:\-)(.*?)(?=\-|\(ref|\-)",
                         orig_narration.lower()):
                cleaned_narration_ft = \
                    re.findall(r"(?:^neft cr\W?)(?:(?:\-(?:.*?)[0-9]+(?:.*?))(?=\-)){1,2}(?:\-)(.*?)(?=\-|\(ref|\-)",
                               orig_narration.lower())[0]
                which_regex = "neft cr starting"

        elif re.search(r"(?:by transfer\W?)(?:inb|cmp)(.*)?(?:\(ref|\-)", orig_narration.lower()):
            cleaned_narration_ft = \
                re.findall(r"(?:by transfer\W?)(?:inb|cmp)(.*)?(?:\(ref|\-)", orig_narration.lower())[0]
            which_regex = "by transfer inb|cmp"

        elif re.search(r"^neft[-|/]", orig_narration.lower()):
            # print("inside ^neft-")
            spl_narr = []
            if orig_narration.count('-') >= 2:
                spl_narr = orig_narration.lower().split('-')
            elif orig_narration.count('/') >= 2:
                spl_narr = orig_narration.lower().split('/')
            # print("spl_narr", spl_narr)
            if len(spl_narr) > 1:
                for part in spl_narr[1:]:
                    # print("inside for", part)
                    # this is to handle cases where we are getting numeric value because of salary
                    # extract_part_till_sal = re.sub(r'(.*)(\bsal.*)', '\1', part)
                    # if not re.search(r"\d+", extract_part_till_sal.strip()):
                    if not len(re.findall(r"\d{1}", part.strip())) > 4 and re.sub(r"\d+", " ",
                                                                                  part) not in ifsc_set and len(
                        re.sub(r"\d+", " ", part)) >= 4:
                        cleaned_narration_ft = re.sub(r"\d+", " ", part).strip()
                        which_regex = "^neft-"
                        break
            # print("cleaned_narration_ft", cleaned_narration_ft)

        elif re.search(r"^neft inward neft in", orig_narration.lower()):
            if re.search(r"(?:^neft\W?inward\W?neft\W?in(?:.*?)from)(.*?)(?:\w{1,}\d\w+)", orig_narration.lower()):
                cleaned_narration_ft = \
                    re.findall(r"(?:^neft\W?inward\W?neft\W?in(?:.*?)from)(.*?)(?:\w{1,}\d\w+)",
                               orig_narration.lower())[0]
                which_regex = "neft inwd starting"

        elif re.search(r"neft", orig_narration.lower()):
            # print("===================neft main1")
            if re.search(
                    r"(?:^neft\W+)(?:[a-z]{1,})?(?:[0-9]{9,})(.*?)(?=\babhy|\babna|\babpb|\badcb|\badcc|\bairp|\bajar|\bajhc|\bakjb|\balla|\bamcb|\bamdn|\bandb|\banzb|\bapbl|\bapgb|\bapgv|\bapmc|\basbl|\baubl|\baucb|\bbacb|\bbara|\bbarb|\bbarc|\bbbkm|\bbcbm|\bbcey|\bbdbl|\bbkdn|\bbkid|\bbnpa|\bbnsb|\bbofa|\bbotm|\bcbin|\bccbl|\bchas|\bciti|\bciub|\bclbl|\bcnrb|\bcosb|\bcres|\bcrly|\bcrub|\bcsbk|\bcsbx|\bctba|\bctcb|\bdbss|\bdcbl|\bdeob|\bdeut|\bdicg|\bdlsc|\bdlxb|\bdmkj|\bdnsb|\bdohb|\bdurg|\bebil|\beibi|\besfb|\besmf|\bfdrl|\bfino|\bfirn|\bfsfb|\bgbcb|\bgdcb|\bggbk|\bgscb|\bharc|\bhcbl|\bhdfc|\bhpsc|\bhsbc|\bhvbk|\bibbk|\bibkl|\bibko|\bicbk|\bicic|\bidfb|\bidib|\biduk|\bindb|\bioba|\bipos|\bitbl|\bjaka|\bjana|\bjasb|\bjiop|\bjjsb|\bjpcb|\bjsbl|\bjsbp|\bjsfb|\bkace|\bkaij|\bkana|\bkang|\bkarb|\bkbkb|\bkcbl|\bkccb|\bkdcb|\bkgrb|\bkjsb|\bkkbk|\bklgb|\bknsb|\bkoex|\bkolh|\bkrth|\bksbk|\bkscb|\bkucb|\bkvbl|\bkvgb|\blavb|\bmahb|\bmahg|\bmcbl|\bmdbk|\bmdcb|\bmhcb|\bmkpb|\bmsbl|\bmsci|\bmshq|\bmslm|\bmsnu|\bmubl|\bmvcb|\bnata|\bnbad|\bnbrd|\bncub|\bnesf|\bngsb|\bnicb|\bnjbk|\bnkgs|\bnmcb|\bnmgb|\bnnsb|\bnosc|\bnspb|\bntbl|\bnucb|\bnvnm|\boiba|\borbc|\borcb|\bpayt|\bpjsb|\bpkgb|\bpmcb|\bpmec|\bprth|\bpsib|\bpucb|\bpunb|\bpusd|\bpytm|\bqnba|\brabo|\bratn|\brbih|\brbis|\brmgb|\brnsb|\brrbp|\brsbl|\brscb|\brssb|\bsabr|\bsahe|\bsant|\bsbin|\bsbls|\bscbl|\bsdcb|\bsdce|\bshbk|\bsibl|\bsidb|\bsidc|\bsjsb|\bsksb|\bsmbc|\bsmcb|\bsnbk|\bsoge|\bspcb|\bsrcb|\bstcb|\bsunb|\bsury|\bsusb|\bsutb|\bsvbl|\bsvcb|\bsvsh|\bsynb|\btbsb|\btdcb|\btgmb|\bthrs|\btjsb|\btmbl|\btnsc|\btsab|\btssb|\bttcb|\bubin|\bucba|\bujvn|\buovb|\bupcb|\burbn|\butbi|\butib|\butks|\buucb|\bvara|\bvasj|\bvcob|\bvijb|\bvsbl|\bvvsb|\bwbsc|\bwpac|\byesb|\bzcbl|\bzsb|\bbarb|axis|deustche|canara|central|axis|bandhan|hdfc|icici|idfc|idbi|indusind|karnataka|rbl|kotak|axis|hdfc|bank of|\bbank|payrol|\(ref|[0-9]{6,})",
                    orig_narration.lower()):
                # print("===================neft main")
                cleaned_narration_ft = re.findall(
                    r"(?:^neft\W+)(?:[a-z]{1,})?(?:[0-9]{9,})(.*?)(?=\babhy|\babna|\babpb|\badcb|\badcc|\bairp|\bajar|\bajhc|\bakjb|\balla|\bamcb|\bamdn|\bandb|\banzb|\bapbl|\bapgb|\bapgv|\bapmc|\basbl|\baubl|\baucb|\bbacb|\bbara|\bbarb|\bbarc|\bbbkm|\bbcbm|\bbcey|\bbdbl|\bbkdn|\bbkid|\bbnpa|\bbnsb|\bbofa|\bbotm|\bcbin|\bccbl|\bchas|\bciti|\bciub|\bclbl|\bcnrb|\bcosb|\bcres|\bcrly|\bcrub|\bcsbk|\bcsbx|\bctba|\bctcb|\bdbss|\bdcbl|\bdeob|\bdeut|\bdicg|\bdlsc|\bdlxb|\bdmkj|\bdnsb|\bdohb|\bdurg|\bebil|\beibi|\besfb|\besmf|\bfdrl|\bfino|\bfirn|\bfsfb|\bgbcb|\bgdcb|\bggbk|\bgscb|\bharc|\bhcbl|\bhdfc|\bhpsc|\bhsbc|\bhvbk|\bibbk|\bibkl|\bibko|\bicbk|\bicic|\bidfb|\bidib|\biduk|\bindb|\bioba|\bipos|\bitbl|\bjaka|\bjana|\bjasb|\bjiop|\bjjsb|\bjpcb|\bjsbl|\bjsbp|\bjsfb|\bkace|\bkaij|\bkana|\bkang|\bkarb|\bkbkb|\bkcbl|\bkccb|\bkdcb|\bkgrb|\bkjsb|\bkkbk|\bklgb|\bknsb|\bkoex|\bkolh|\bkrth|\bksbk|\bkscb|\bkucb|\bkvbl|\bkvgb|\blavb|\bmahb|\bmahg|\bmcbl|\bmdbk|\bmdcb|\bmhcb|\bmkpb|\bmsbl|\bmsci|\bmshq|\bmslm|\bmsnu|\bmubl|\bmvcb|\bnata|\bnbad|\bnbrd|\bncub|\bnesf|\bngsb|\bnicb|\bnjbk|\bnkgs|\bnmcb|\bnmgb|\bnnsb|\bnosc|\bnspb|\bntbl|\bnucb|\bnvnm|\boiba|\borbc|\borcb|\bpayt|\bpjsb|\bpkgb|\bpmcb|\bpmec|\bprth|\bpsib|\bpucb|\bpunb|\bpusd|\bpytm|\bqnba|\brabo|\bratn|\brbih|\brbis|\brmgb|\brnsb|\brrbp|\brsbl|\brscb|\brssb|\bsabr|\bsahe|\bsant|\bsbin|\bsbls|\bscbl|\bsdcb|\bsdce|\bshbk|\bsibl|\bsidb|\bsidc|\bsjsb|\bsksb|\bsmbc|\bsmcb|\bsnbk|\bsoge|\bspcb|\bsrcb|\bstcb|\bsunb|\bsury|\bsusb|\bsutb|\bsvbl|\bsvcb|\bsvsh|\bsynb|\btbsb|\btdcb|\btgmb|\bthrs|\btjsb|\btmbl|\btnsc|\btsab|\btssb|\bttcb|\bubin|\bucba|\bujvn|\buovb|\bupcb|\burbn|\butbi|\butib|\butks|\buucb|\bvara|\bvasj|\bvcob|\bvijb|\bvsbl|\bvvsb|\bwbsc|\bwpac|\byesb|\bzcbl|\bzsb|\bbarb|axis|deustche|canara|central|axis|bandhan|hdfc|icici|idfc|idbi|indusind|karnataka|rbl|kotak|axis|hdfc|bank of|\bbank|payrol|\(ref|[0-9]{6,})",
                    orig_narration.lower())[0]
                which_regex = "main neft"

        elif re.search(r"^imps", orig_narration.lower()):
            if re.search(
                    r"(?:imps)(?:\W+)?(?:[0-9]{1,}\s+[0-9]{1,}|[0-9]+|p2a|inet|mob|\babhy|\babna|\babpb|\badcb|\badcc|\bairp|\bajar|\bajhc|\bakjb|\balla|\bamcb|\bamdn|\bandb|\banzb|\bapbl|\bapgb|\bapgv|\bapmc|\basbl|\baubl|\baucb|\bbacb|\bbara|\bbarb|\bbarc|\bbbkm|\bbcbm|\bbcey|\bbdbl|\bbkdn|\bbkid|\bbnpa|\bbnsb|\bbofa|\bbotm|\bcbin|\bccbl|\bchas|\bciti|\bciub|\bclbl|\bcnrb|\bcosb|\bcres|\bcrly|\bcrub|\bcsbk|\bcsbx|\bctba|\bctcb|\bdbss|\bdcbl|\bdeob|\bdeut|\bdicg|\bdlsc|\bdlxb|\bdmkj|\bdnsb|\bdohb|\bdurg|\bebil|\beibi|\besfb|\besmf|\bfdrl|\bfino|\bfirn|\bfsfb|\bgbcb|\bgdcb|\bggbk|\bgscb|\bharc|\bhcbl|\bhdfc|\bhpsc|\bhsbc|\bhvbk|\bibbk|\bibkl|\bibko|\bicbk|\bicic|\bidfb|\bidib|\biduk|\bindb|\bioba|\bipos|\bitbl|\bjaka|\bjana|\bjasb|\bjiop|\bjjsb|\bjpcb|\bjsbl|\bjsbp|\bjsfb|\bkace|\bkaij|\bkana|\bkang|\bkarb|\bkbkb|\bkcbl|\bkccb|\bkdcb|\bkgrb|\bkjsb|\bkkbk|\bklgb|\bknsb|\bkoex|\bkolh|\bkrth|\bksbk|\bkscb|\bkucb|\bkvbl|\bkvgb|\blavb|\bmahb|\bmahg|\bmcbl|\bmdbk|\bmdcb|\bmhcb|\bmkpb|\bmsbl|\bmsci|\bmshq|\bmslm|\bmsnu|\bmubl|\bmvcb|\bnata|\bnbad|\bnbrd|\bncub|\bnesf|\bngsb|\bnicb|\bnjbk|\bnkgs|\bnmcb|\bnmgb|\bnnsb|\bnosc|\bnspb|\bntbl|\bnucb|\bnvnm|\boiba|\borbc|\borcb|\bpayt|\bpjsb|\bpkgb|\bpmcb|\bpmec|\bprth|\bpsib|\bpucb|\bpunb|\bpusd|\bpytm|\bqnba|\brabo|\bratn|\brbih|\brbis|\brmgb|\brnsb|\brrbp|\brsbl|\brscb|\brssb|\bsabr|\bsahe|\bsant|\bsbin|\bsbls|\bscbl|\bsdcb|\bsdce|\bshbk|\bsibl|\bsidb|\bsidc|\bsjsb|\bsksb|\bsmbc|\bsmcb|\bsnbk|\bsoge|\bspcb|\bsrcb|\bstcb|\bsunb|\bsury|\bsusb|\bsutb|\bsvbl|\bsvcb|\bsvsh|\bsynb|\btbsb|\btdcb|\btgmb|\bthrs|\btjsb|\btmbl|\btnsc|\btsab|\btssb|\bttcb|\bubin|\bucba|\bujvn|\buovb|\bupcb|\burbn|\butbi|\butib|\butks|\buucb|\bvara|\bvasj|\bvcob|\bvijb|\bvsbl|\bvvsb|\bwbsc|\bwpac|\byesb|\bzcbl|\bzsb|\bbarb|\bifsc)?(?:\W)?(?:fund\s+trf\W+)?(?:[0-9]+)?(?:\W+)?(?:(.*?\-)|(.*?\/))",
                    orig_narration.lower()):
                cleaned_narration_ft = re.search(
                    r"(?:imps)(?:\W+)?(?:[0-9]{1,}\s+[0-9]{1,}|[0-9]+|p2a|inet|mob|\babhy|\babna|\babpb|\badcb|\badcc|\bairp|\bajar|\bajhc|\bakjb|\balla|\bamcb|\bamdn|\bandb|\banzb|\bapbl|\bapgb|\bapgv|\bapmc|\basbl|\baubl|\baucb|\bbacb|\bbara|\bbarb|\bbarc|\bbbkm|\bbcbm|\bbcey|\bbdbl|\bbkdn|\bbkid|\bbnpa|\bbnsb|\bbofa|\bbotm|\bcbin|\bccbl|\bchas|\bciti|\bciub|\bclbl|\bcnrb|\bcosb|\bcres|\bcrly|\bcrub|\bcsbk|\bcsbx|\bctba|\bctcb|\bdbss|\bdcbl|\bdeob|\bdeut|\bdicg|\bdlsc|\bdlxb|\bdmkj|\bdnsb|\bdohb|\bdurg|\bebil|\beibi|\besfb|\besmf|\bfdrl|\bfino|\bfirn|\bfsfb|\bgbcb|\bgdcb|\bggbk|\bgscb|\bharc|\bhcbl|\bhdfc|\bhpsc|\bhsbc|\bhvbk|\bibbk|\bibkl|\bibko|\bicbk|\bicic|\bidfb|\bidib|\biduk|\bindb|\bioba|\bipos|\bitbl|\bjaka|\bjana|\bjasb|\bjiop|\bjjsb|\bjpcb|\bjsbl|\bjsbp|\bjsfb|\bkace|\bkaij|\bkana|\bkang|\bkarb|\bkbkb|\bkcbl|\bkccb|\bkdcb|\bkgrb|\bkjsb|\bkkbk|\bklgb|\bknsb|\bkoex|\bkolh|\bkrth|\bksbk|\bkscb|\bkucb|\bkvbl|\bkvgb|\blavb|\bmahb|\bmahg|\bmcbl|\bmdbk|\bmdcb|\bmhcb|\bmkpb|\bmsbl|\bmsci|\bmshq|\bmslm|\bmsnu|\bmubl|\bmvcb|\bnata|\bnbad|\bnbrd|\bncub|\bnesf|\bngsb|\bnicb|\bnjbk|\bnkgs|\bnmcb|\bnmgb|\bnnsb|\bnosc|\bnspb|\bntbl|\bnucb|\bnvnm|\boiba|\borbc|\borcb|\bpayt|\bpjsb|\bpkgb|\bpmcb|\bpmec|\bprth|\bpsib|\bpucb|\bpunb|\bpusd|\bpytm|\bqnba|\brabo|\bratn|\brbih|\brbis|\brmgb|\brnsb|\brrbp|\brsbl|\brscb|\brssb|\bsabr|\bsahe|\bsant|\bsbin|\bsbls|\bscbl|\bsdcb|\bsdce|\bshbk|\bsibl|\bsidb|\bsidc|\bsjsb|\bsksb|\bsmbc|\bsmcb|\bsnbk|\bsoge|\bspcb|\bsrcb|\bstcb|\bsunb|\bsury|\bsusb|\bsutb|\bsvbl|\bsvcb|\bsvsh|\bsynb|\btbsb|\btdcb|\btgmb|\bthrs|\btjsb|\btmbl|\btnsc|\btsab|\btssb|\bttcb|\bubin|\bucba|\bujvn|\buovb|\bupcb|\burbn|\butbi|\butib|\butks|\buucb|\bvara|\bvasj|\bvcob|\bvijb|\bvsbl|\bvvsb|\bwbsc|\bwpac|\byesb|\bzcbl|\bzsb|\bbarb|\bifsc)?(?:\W)?(?:fund\s+trf\W+)?(?:[0-9]+)?(?:\W+)?(?:(.*?\-)|(.*?\/))",
                    orig_narration.lower())[0]
                which_regex = "imps neft"

        # print("after all if else", cleaned_narration_ft)

        if cleaned_narration_ft == "":
            which_regex = "final_if"
            # print("inside final if")
            narr = narr.lower()
            # print("-2----------", narr)
            narr = re.sub(
                r"by clg:chn acct sec|by clg:del accts|by clg:mum clg sec|^transfer to|^transfer from|^transfer credit|^transfer debit|^by chq|^imps|^neft|^upi|\bnach\b|\bach\b|^debit|^credit|^by transfer|^withdrawal transfer|^wdl tfr|^to transfer|^by debit card|^by credit card|^money received received from|^money received using imps received from|^money received via upi received from|^money sent using upi sent to|^money sent using imps sent to|^paid in store using|^paid online using|^paid using your bank account paid successfully at|202[0-9]",
                " ", narr)

            cleaned_narration_ft = re.sub(r"\\n", "", narr)
            # print("02----------", cleaned_narration_ft)

            # To remove name in neft narrations
            if 'neft' in cleaned_narration_ft and '-' in cleaned_narration_ft:
                spl = cleaned_narration_ft.split('-')
                if len(spl) == 5:
                    if spl[2].strip().isalnum():
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-1])
                    else:
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-2])
                elif len(spl) == 4:
                    if spl[1].strip().isalnum():
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-1])
                    else:
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-2])
                        # print("after final if", cleaned_narration_ft)

        # print("2----------", cleaned_narration_ft)
        # Kotak type 7 handle
        regex_for_neft = re.findall("^neft[A-Za-z0-9]{16}", cleaned_narration_ft)
        if regex_for_neft and not cleaned_narration_ft.isspace():
            cleaned_narration_ft = cleaned_narration_ft.replace(regex_for_neft[0], '').strip()

        split_narr = re.split(r"[/|-]", cleaned_narration_ft)

        cleaned_narration_ft = re.sub(r"-|\\|//|/|\*", ' ', cleaned_narration_ft)
        # print("30000----", cleaned_narration_ft)
        cleaned_narration_ft = re.sub('[a-z]+[0-9]+', ' ', cleaned_narration_ft)  # removing alpha-num
        # print("3000----", cleaned_narration_ft)
        cleaned_narration_ft = re.sub('[0-9]+[a-z]+', ' ', cleaned_narration_ft)  # removing num-alpha
        # print("300----", cleaned_narration_ft)
        cleaned_narration_ft = re.sub('[0-9]', '', cleaned_narration_ft)  # removing all numerals
        # print("30----", cleaned_narration_ft)
        cleaned_narration_ft = re.sub(r"[0-9]|\bfi\b|ref|#|c-|\bko\b|\bcsh\b|\bdep\b|\bcdm\b|\bby\b|\btxn\b|[^a-zA-Z]+",
                                      " ", cleaned_narration_ft)
        # print("3----", cleaned_narration_ft)
        cleaned_narration_ft = ' '.join([word for word in cleaned_narration_ft.split(' ')
                                         if word.lower() not in CUSTOM_STOPWORDS_FT
                                         and len(word) >= 2])  # removing stop words
        # print("before applying ", cleaned_narration_ft, "\n\n")
        # cleaned_narration_ft = cleaned_narration_ft.strip()

        # print("before big regex", cleaned_narration_ft)
        regex_stop_words = [
            r'''(?:month|for|s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?(s)?)(?:\W?)(?:jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)''',
            r'''\bjan\b|\bfeb\b|\bmar\b|\bapr\b|\bmay\b|\bjun\b|\bjul\b|\band\b|\baug\b|\bsep\b|\boct\b|\bnov\b|\bdec\b|\bmarc\b|\bfebr\b|\bjanu\b''',
            r'''s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?(s)?|\bslc\b|\bslry\b|arrear(s)?|\bthis\b|wage(s)?\b|\bcin\b|\bifi\b|\bno\b|bonus|funds|^fn\b|\b\b|account|\bof\b|\bto\b|\brrn\b|\bsal_|\bchq\b|pay( )?rol(l)?|\bthe\b''',
            r'''\bemplid|netsal|saltrf|reward|reimb|remmitance|expclaim|incentive|allowanc|cashback|reimburs|_sal_|stipend|diwali|\bcredit\b|\bbulk\b|\bpaid\b|\badvance\b|\bmonth\b|\badv\b|\bagst\b|\bagainst\b|\bau\b|^mb\b|^mbk\b|\bmb$|\bpay\b|payment|payout|trnftrf|\bpipe\b''',
            r'''\bbrn\b|\bfee\b|^bt\b|standard( )?(chart)?(ered)?|\bbank\b|bulk post(ing)?|\bother(s)?|\bcmp\b|\becs\b|\bemp(loy)?(ee|e)?\b|payment|deposit|\bcrtr\b|^ft\b|^ib\b|^idc\b|^ift\b|upload|\bupld\b|^mmt\b|^mob\b|\bhit\b|\bacc\b|\bhsbc\b|\binward\b|\binw\b|\boutward\b|\butr\b|\bbeing\b|\bpaid\b|\breceive(d)?\b''',
            r'''januar(a)?(y)?|febru|march|april|\bmay\b|june|july|august|augus|septem|octob|novemb|decemb''',
            r'''\bkcu\b|\bkcc\b|\bsbi\b|\bicic\b|\baxs\b|\biob\b|\bhdf\b|\byes\b|\bbob\b|\bboi\b|\bfund(s)?\b|\bclg\b|net pay|ecn no|incentive|employe(e)?(s)?|emply|\bcrtr\b|moneyreceivedreceivedfromone97|easebuzz|cashfree|paytmservices|phonepe''',
            r'''wunderbaked|payflashtech|compensa(tion)?|moneyreceivedtransactionid|aggrepaypayments|fiduciarybi|\bchq\b''',
            r'''\bfor\b|\btrc\b|^tb\b|\betxn\b|\bempno\b|\babhy\b|\bmo(n)?\b|\bof\b|credited|\babna\b|\babpb\b|\badcb\b|\badcc\b|\bairp\b|\bajar\b|\byes\b|\bndu\b|\bbwn\b|\bajhc\b|\bakjb\b|\brscb\b|\brssb\b|\bsabr\b|\bsahe\b|\bsant\b|\bsbin\b|\bsbls\b|\bscbl\b|\bsdcb\b|\bsdce\b|\bshbk\b|\bsibl\b|\bsidb\b|\bsidc\b|\bsjsb\b|\bsksb\b|\bsmbc\b|\bsmcb\b|\bsnbk\b|\bsoge\b|\bspcb\b|\bsrcb\b|\bstcb\b|\bsunb\b|\bsury\b|\bsusb\b|\bsutb\b|\bsvbl\b''',
            r'''\bsvcb\b|\bsvsh\b|\bsynb\b|\btbsb\b|\btdcb\b|\btgmb\b|\bthrs\b|\btjsb\b|\btmbl\b|\btnsc\b|\btsab\b|\btssb\b|\bttcb\b|\bubin\b|\bucba\b|\bujvn\b|\buovb\b|\bupcb\b|\burbn\b|\butbi\b|\butib\b|\butks\b|\buucb\b|\bvara\b|\bvasj\b|\bvcob\b|\bvijb\b|\bvsbl\b|\bvvsb\b|\bwbsc\b|\bwpac\b|\byesb\b|\bzcbl\b|\bzsbl\b|^irm\b|^tb\b''',
            r'''\balla\b|\bamcb\b|\bamdn\b|\bandb\b|\banzb\b|\bapbl\b|\bapgb\b|\bapgv\b|\bapmc\b|\basbl\b|\baubl\b|\baucb\b|\bbacb\b|\bbara\b|\bbarb\b|\bbarc\b|\bbbkm\b|\bbcbm\b|\bbcey\b|\bbdbl\b|\bbkdn\b|\bbkid\b|\bbnpa\b|\bbnsb\b|\bbofa\b|\bbotm\b|\bcbin\b|\bccbl\b|\bchas\b|\bciti\b|\bciub\b|\bclbl\b|\bcnrb\b|\bcosb\b|\bcres\b|\bcrly\b|\bcrub\b|\bcsbk\b|\bcsbx\b|\bctba\b|\bctcb\b|\bdbss\b|\bdcbl\b|\bdeob\b|\bdeut\b|\bdicg\b|\bdlsc\b''',
            r'''\bdlxb\b|\bdmkj\b|\bdnsb\b|\bdohb\b|\bdurg\b|\bebil\b|\beibi\b|\besfb\b|\besmf\b|\bfdrl\b|\bfino\b|\bfirn\b|\bfsfb\b|\bgbcb\b|\bgdcb\b|\bggbk\b|\bgscb\b|\bharc\b|\bhcbl\b|\bhdfc\b|\bhpsc\b|\bhsbc\b|\bhvbk\b|\bibbk\b|\bibkl\b|\bibko\b|\bicbk\b|\bicic\b|\bidfb\b|\bidib\b|\biduk\b|\bindb\b|\bioba\b|\bipos\b|\bitbl\b|\bjaka\b''',
            r'''\bthe\b|\bjana\b|\bjasb\b|\bjiop\b|\bjjsb\b|\bjpcb\b|\bjsbl\b|\bjsbp\b|\bjsfb\b|\bkace\b|\bkaij\b|\bkana\b|\bkang\b|\bkarb\b|\bkbkb\b|\bkcbl\b|\bkccb\b|\bkdcb\b|\bkgrb\b|\bkjsb\b|\bkkbk\b|\bklgb\b|\bknsb\b|\bkoex\b|\bkolh\b|\bkrth\b|\bksbk\b|\bkscb\b|\bkucb\b|\bkvbl\b|\bkvgb\b|\blavb\b|\bmahb\b|\bmahg\b|\bmcbl\b|\bmdbk\b|\bmdcb\b|\bmhcb\b|\bmkpb\b|\bmsbl\b|\bmsci\b|\bmshq\b|\bmslm\b|\bmsnu\b|\bmubl\b|\bmvcb\b|\bnata\b|\bnbad\b''',
            r'''\bnbrd\b|\bncub\b|\bnesf\b|\bngsb\b|\bnicb\b|\bnjbk\b|\bnkgs\b|\bnmcb\b|\bnmgb\b|\bnnsb\b|\bnosc\b|\bnspb\b|\bntbl\b|\bnucb\b|\bnvnm\b|\boiba\b|\borbc\b|\borcb\b|\bpayt\b|\bpjsb\b|\bpkgb\b|\bpmcb\b|\bpmec\b|\bprth\b|\bpsib\b|\bpucb\b|\bpunb\b|\bpusd\b|\bpytm\b|\bqnba\b|\brabo\b|\bratn\b|\brbih\b|\brbis\b|\brmgb\b|\brnsb\b|\brrbp\b|\brsbl\b''',
            r'''^ft\b|^ift\b|^mob\b|^bt\b|^mmt\b|\both\b|\bitg\b|^ifn\b''']
        for stop_word in regex_stop_words:
            # print(stop_word, cleaned_narration_ft)
            cleaned_narration_ft = re.sub(r"\s+", " ", re.sub(stop_word, " ", cleaned_narration_ft.lower())).strip()

        cleaned_narration_ft = re.sub(r"\s+", " ", cleaned_narration_ft).strip()
        # print("4=========", cleaned_narration_ft)
        is_name_or_comp = name_or_comp_pred(cleaned_narration_ft, name_comp_model)[0].replace('__label__', '')
        cleaned_narration_ft = '' if len(
            cleaned_narration_ft) < 4 or is_name_or_comp == 'name' else cleaned_narration_ft
        # print("above last line", cleaned_narration_ft)
        cleaned_narration_ft = get_exact_company(orig_narration, cleaned_narration_ft)
        # print("finally", cleaned_narration_ft)

        if re.search(r"^staff(s)?$|^expense(s)?$|^hold(s)?$", cleaned_narration_ft.strip()):
            cleaned_narration_ft = ''

        # print("here set of", set(cleaned_narration_ft), len(set(cleaned_narration_ft)))
        if len(set(cleaned_narration_ft)) <= 2:
            cleaned_narration_ft = ''

    except Exception as e:
        return ""

    return cleaned_narration_ft





def clean_function_new_new(row):
    try:
        narr, category = row.iloc[0], row.iloc[1]
        # if not (re.search(r'\bneft\b|\bneft_|\brtgs\b|\bbulk( )?post|transfer/tb', narr.lower()) or re.search(r'^NEFT', narr))  and category.lower()!='salary':
        #     return '', ''

        CUSTOM_STOPWORDS_CLEAN = ['ref', 'ifsc', 'tpt', 'trf', 'by transfer', 'inb', 'tfr', 'inf', 'cardlessdeposit',
                                  'cardless deposit', 'inft', 'icsp', 'trfr', 'icsp', 'frm', 'inet', 'cms', 'rtgs',
                                  'impsab', 'bank', 'icici', 'limit', 'limited', 'pvt', 'solutions', 'private', 'software', 'hdfc', 'sbi', 'axis', 'canara', 'payment',
                                  'neft', 'imps', 'upi', 'cash', 'atm', 'pos', 'p2a', 'ach', 'transfer', 'csp', 'outlet', 'from',
                                  'moneytrf', 'sbin', 'opening', 'balance', 'january', 'february', 'march', 'april', 'may',
                                  'june', 'july', 'august', 'september', 'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep',
                                  'oct', 'nov', 'dec', 'sept', 'sbil', 'loan', 'disbursement', 'disburse', 'disbur']

        CUSTOM_STOPWORDS_FT = ['ref', 'ifsc', 'tpt', 'trf', 'by transfer', 'inb', 'tfr', 'inf', 'cardlessdeposit',
                               'cardless deposit', 'inft', 'icsp', 'trfr', 'icsp', 'frm', 'inet', 'cms', 'rtgs', 'impsab',
                               'bank', 'icici', 'hdfc', 'sbi', 'axis', 'canara', 'payment',
                               'neft', 'imps', 'upi', 'cash', 'atm', 'pos', 'p2a', 'ach', 'transfer', 'csp', 'outlet',
                               'from',
                               'moneytrf', 'sbin', 'opening', 'balance', 'january', 'february', 'march', 'april', 'may',
                               'june', 'july', 'august', 'september',
                               'october', 'november', 'december', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep',
                               'oct', 'nov', 'dec', 'sept', 'cr', 'null', 'neft', 'imps', 'ne', 'neftcr', 'shree', 'state',
                               'ban', 'attn', 'outward', 'and', 'icic', 'sbil']

        narr = narr.lower()
        # non_salary = re.findall(r'\bbil\b|\binf\b|by transfer-inb|\bupi\b|\bbupi\b|\bearlysalary\b|\bearly salary\b|\bupiab\b|\bupi[0-9]{1,}|cheque|mmt/imps|upi|/rev/|imps|mbk/|ib itg|chq|ib funds|ifn/bt|mobft from|angel broking|rzpx|\bpos\b|^pos\b|ebanking|dream11|bil\|\binf\b|\binft\b|\bsbil|mb:|\btds\b|\btcs\b', narr)
        non_salary = re.findall(r'^mb\b|^clg\b|\bself\b|\bby( )?clg\b|\bbil(l)?\b|\binf\b|\bupi\b|\bbupi\b|\bearlysalary\b|\bearly salary\b|\bupiab\b|\bupi[0-9]{1,}|cheque|upi|/rev/|mbk/|ib itg|chq|ib funds|ifn/bt|mobft from|angel broking|rzpx|\bpos\b|^pos\b|ebanking|dream11|bil\|\binf\b|\binft\b|\bsbil|mb:|\btds\b|\btcs\b', narr)
        paytm_clean_fun = re.findall(r'moneyreceivedreceivedfromone97|easebuzz|cashfree|paytmservices|phonepe|incentive|wunderbaked|payflashtech|moneyreceivedtransactionid|aggrepaypayments|fiduciarybi', narr.replace(' ', '').strip())
        salary_keywords = re.findall(r'neft|imps|rtgs|\bnft\b|bulk( )?post|\binb\b', narr)  # sometimes by transfer with neft comes, to handle those cases I created this variable

        if (non_salary or paytm_clean_fun) or (re.search(r"by( )?transfer", narr) and not salary_keywords):
            # print("coming here for narr", narr)
            return '', ''

        else:
            # remove ref number
            cleaned_narration_ft = re.sub(r"\\n", "", narr)
            ref_num_search = re.findall("ref# [a-zA-Z0-9]*", cleaned_narration_ft)
            if ref_num_search:
                cleaned_narration_ft = cleaned_narration_ft.replace("(" + ref_num_search[0] + ")", "").strip()
                ref_num_search = ref_num_search[0].replace('ref#', '').strip()
                cleaned_narration_ft = cleaned_narration_ft.split('ref#')[0]
                cleaned_narration_ft = cleaned_narration_ft.replace(ref_num_search, '').strip()
            # To remove name in neft narrations
            if 'neft' in cleaned_narration_ft and '-' in cleaned_narration_ft:
                spl = cleaned_narration_ft.split('-')
                if len(spl) == 5:
                    if spl[2].strip().isalnum():
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-1])
                    else:
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-2])
                elif len(spl) == 4:
                    if spl[1].strip().isalnum():
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-1])
                    else:
                        cleaned_narration_ft = ' '.join(a for a in spl[0:-2])
            # Kotak type 7 handle
            regex_for_neft = re.findall("^neft[A-Za-z0-9]{16}", cleaned_narration_ft)
            if regex_for_neft and not cleaned_narration_ft.isspace():
                cleaned_narration_ft = cleaned_narration_ft.replace(regex_for_neft[0], '').strip()
            cleaned_narration_ft = re.sub(r"-|\\|//|/|\*", ' ', cleaned_narration_ft)
            cleaned_narration_ft = re.sub('[a-z]+[0-9]+', ' ', cleaned_narration_ft)  # removing alpha-num
            cleaned_narration_ft = re.sub('[0-9]+[a-z]+', ' ', cleaned_narration_ft)  # removing num-alpha
            cleaned_narration_ft = re.sub('[0-9]', '', cleaned_narration_ft)  # removing all numerals
            cleaned_narration_ft = re.sub(r"[0-9]|\bfi\b|ref|#|c-|\bko\b|\bcsh\b|\bdep\b|\bcdm\b|\bby\b|\btxn\b|[^a-zA-Z]+", " ", cleaned_narration_ft)
            cleaned_narration_ft = ' '.join([word for word in cleaned_narration_ft.split(' ')
                                             if word.lower() not in CUSTOM_STOPWORDS_FT and len(word) >= 2])  # removing stop words

            # this is for cleaned salary
            cleaned_narration = re.sub(r"limite d\b", "limited", narr)
            cleaned_narration = re.sub(r"(\(ref# .*\))|\(|\)|\n|ref# [a-zA-Z0-9]*|ref#|\bltd\b|\bsol\b|limite( )?(d)?|\bpvt\b|privat(e)?|Ref# [a-zA-Z0-9]*", "", narr)
            cleaned_narration = re.sub(r"-|\\|//|/|\*", ' ', cleaned_narration)
            cleaned_narration = re.sub('[a-z]+[0-9]+', ' ', cleaned_narration)  # removing alpha-num
            cleaned_narration = re.sub('[0-9]+[a-z]+', ' ', cleaned_narration)  # removing num-alpha
            cleaned_narration = re.sub(r"\bfi\b|\bref\b|#|c-|\bko\b|\bcsh\b|\bdep\b|\bcdm\b|\bby\b|\btxn\b|[^a-zA-Z]+", " ", cleaned_narration)
            cleaned_narration = ' '.join([word for word in cleaned_narration.split(' ') if
                                          word.lower() not in CUSTOM_STOPWORDS_CLEAN and len(word) >= 1])
            cleaned_narration = re.sub(r"loan|disburs(e)?(m)?(ent)?|bajaj\W*pay|\bnach\b|\bach\b|\bmpay\b|imps|trtr", "", cleaned_narration)

        if re.search("money\W*2\W*me", narr):
            return "money2me"
    except:
        return "", ""

    return cleaned_narration, cleaned_narration_ft



def removing_narrations_higher_than_threshold(df, clean_text_list, months, df_3large):
    '''
    get all the distinct cleaned narrations.
    find the index of all those cleaned narrations on the original df for which the count is greater than month*3.
    '''
    group_by_df = df.groupby(['cleaned_narration']).count()
    selected_index = group_by_df[group_by_df['date'] > months].index
    if len(list(selected_index)) != 0:
        for i, val in clean_text_list:
            orig_narration_row = df.loc[(df['narration'] == df_3large.loc[i]['narration']) & (df['transaction_date'] == df_3large.loc[i]['transaction_date'])]
            if list(orig_narration_row['cleaned_narration'])[0] in list(selected_index):
                clean_text_list = [j for j in clean_text_list if j[1] != val]
    return clean_text_list



def remove_narrations(row):
    try:
        # this will remove imps / upi type of narrations
        orig_narration, category = row.iloc[0], row.iloc[1]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")
        if re.search(r"\bimps\b|transfer-inb|\becs\b|\bupi|upi\b|fiduciary|incentive|\bsbil", narration) \
                or re.search(r'earlysal|fiduciary|incentive', narration_proc):
            return "transferin"
    except:
        return ""
    return ""


def clustering(clean_text_list):
    """Clustering based on narrations"""

    cluster_dict = {}  # intialise cluster
    c = 0
    for i, [idx1, text1] in enumerate(clean_text_list):
        flag=0 # this flag is helpful when we have a single narration that forms one cluster, no other elements fall into that cluster
        for idx2, text2 in clean_text_list[i:]:
            ratio = fuzz.ratio(text1.lower(), text2.lower())

            if ratio > 80 and idx1 != idx2 and len(text1) > 2:
                flag=1
                val = cluster_dict.get(idx1, None)
                if val is None:
                    c += 1
                    cluster_dict.update({idx1: c})
                    cluster_dict.update({idx2: c})
                else:
                    cluster_dict.update({idx2: val})
        if flag == 0 and idx1 not in cluster_dict:
            c += 1
            cluster_dict.update({idx1: c})
    return cluster_dict


def get_salary_month(row):
    min_year, min_month, cur_year, cur_month, cur_date = row
    """Salary month is defined as 23 of one month to 23 of next month"""
    month_diff = (cur_year-min_year)*12 + (cur_month-min_month) + 1
    if cur_date>=23:
        month_diff += 1
    return month_diff


def filter_clusters(cluster_dict, company_idx, df_3large, unique_sal_months, total_number_of_months):
    try:
        # print("here", cluster_dict)
        # print("CAME TO FILTER CLUSTER FUNCTION")
        filtered_cluster_dict = {}
        for key, value in cluster_dict.items():
            if key in company_idx:
                filtered_cluster_dict[key] = value
        # print("cluster_dict, filtered_cluster_dict", cluster_dict, filtered_cluster_dict)
        df_3large['cluster'] = ''

        # check if the filtered_cluster_dict is empty then no need to go ahead, just break here
        if len(filtered_cluster_dict)==0:
            return filtered_cluster_dict

        # print("df_3large.index", df_3large.index.tolist())
        # print("filtered_cluster_dict", list(filtered_cluster_dict.keys()))
        df_3large.loc[list(filtered_cluster_dict.keys()), 'cluster'] = list(filtered_cluster_dict.values())
        df_new = df_3large.loc[filtered_cluster_dict.keys(), ['cleaned_narration', 'sal_month', 'cluster', 'amount']]
        df_new = df_new.groupby(['cluster', 'cleaned_narration']).agg({'sal_month': ['unique', 'nunique'], 'amount': ['var', 'sum']}).reset_index()

        df_new.columns = ['cluster', 'cleaned_narration', 'sal_month_unique', 'sal_month_nunique', 'amount_var', 'amount_sum']
        df_new = df_new.sort_values(by=['sal_month_nunique', 'amount_var', 'amount_sum'], ascending=[False, True, False])

        # df_new.to_csv("/home/ramnaryanpanda/Documents/ds_utility_codebackup/ds-utitlity-codebackup/testing_data/salary_test/out5_just_test.csv", index=False)

        final_cluster_selected = {}
        for cluster in df_new['cluster']:
            uniq_months_of_cur_cluster = set()
            for sal_month_unique in df_new[df_new['cluster'] == cluster]['sal_month_unique']:
                uniq_months_of_cur_cluster.update(sal_month_unique.tolist())
            # print("printing months", uniq_months_of_cur_cluster, unique_sal_months, set(uniq_months_of_cur_cluster) - unique_sal_months, total_number_of_months)
            #if (cluster==-1 or (set(uniq_months_of_cur_cluster) - unique_sal_months) or len(uniq_months_of_cur_cluster) >= total_number_of_months - 2) and len(uniq_months_of_cur_cluster)>=2:
            if (cluster == -1) or (set(uniq_months_of_cur_cluster) - unique_sal_months):
                # print("inside if", uniq_months_of_cur_cluster)
                unique_sal_months.update(uniq_months_of_cur_cluster)
                for key, val in cluster_dict.items():
                    if val == cluster:
                        final_cluster_selected[key] = val
        # print("1st fileter", final_cluster_selected)
        # print()

        cluster_and_unique_months = {}
        for cluster in set(final_cluster_selected.values()):
            if cluster!=-1:
                uniq_months_of_cur_cluster = set()
                for sal_month_unique in df_new[df_new['cluster'] == cluster]['sal_month_unique']:
                    uniq_months_of_cur_cluster.update(sal_month_unique.tolist())
                cluster_and_unique_months[cluster] = list(uniq_months_of_cur_cluster)
        # print("cluster_and_unique_months", cluster_and_unique_months)

        sal_key_cluster_and_unique_months = {}
        for cluster in set(final_cluster_selected.values()):
            if cluster==-1:
                uniq_months_of_cur_cluster = set()
                for sal_month_unique in df_new[df_new['cluster'] == cluster]['sal_month_unique']:
                    uniq_months_of_cur_cluster.update(sal_month_unique.tolist())
                sal_key_cluster_and_unique_months[cluster] = list(uniq_months_of_cur_cluster)
        # print("sal_key_cluster_and_unique_months", sal_key_cluster_and_unique_months)


        final_clusters_to_delete = set()
        # if only one cluster is present and it has number of salaries detected less than<3 and total_number_of_months should not be <=2, then delete this
        if len(set(final_cluster_selected.values()))==1 and list(final_cluster_selected.values())[0]!=-1 and len(cluster_and_unique_months[list(final_cluster_selected.values())[0]])<3 and not total_number_of_months<=2:
            final_clusters_to_delete.add(list(final_cluster_selected.values())[0])
        # print("2nd fileter", final_cluster_selected, final_clusters_to_delete)

        # if more than one cluster present with no of unique_months<=2, then delete those clusters
        clusters_to_remove = [i for i,j in cluster_and_unique_months.items() if len(j)<=2]
        if len(clusters_to_remove)>=2:
            for cluster in clusters_to_remove:
                final_clusters_to_delete.add(cluster)
        # print("3rd fileter", final_cluster_selected, final_clusters_to_delete)

        final_clusters_to_delete_copy = final_clusters_to_delete.copy()
        # finally do one more check, if the remove cluster and not to remove cluster has more than 15common alphabets then do not remove those clusters
        for not_remove_cluster, remove_cluster in product(set(final_cluster_selected.values()) - set(final_clusters_to_delete_copy), set(final_clusters_to_delete_copy)):
            # print(not_remove_cluster, remove_cluster)
            not_remove_cluster_narr, remove_cluster_narr = df_new[df_new['cluster'] == not_remove_cluster]['cleaned_narration'].iloc[0], df_new[df_new['cluster'] == remove_cluster]['cleaned_narration'].iloc[0]
            # print(not_remove_cluster_narr, remove_cluster_narr, pylcs.lcs_sequence_length(not_remove_cluster_narr, remove_cluster_narr))
            if pylcs.lcs_sequence_length(not_remove_cluster_narr, remove_cluster_narr) >= 12:
                final_clusters_to_delete.discard(remove_cluster)
        # print("4th fileter", final_cluster_selected, final_clusters_to_delete)


        # remove clusters if they have any where in the range 3 to (no_of_months/2)+1 months of salary, but are not continuous
        # but also these clusters should not be -1 clusters
        # clusters_to_remove = [i for i, j in cluster_and_unique_months.items() if 1<=len(j)<(total_number_of_months//2)+1]  # want to check with 1
        clusters_to_remove = [i for i, j in cluster_and_unique_months.items() if 2<=len(j)<(total_number_of_months//2)+1]  # original
        # print("before 5th filter", clusters_to_remove)
        for cluster in clusters_to_remove:
            cluster_and_unique_months_lst = cluster_and_unique_months[cluster]
            for i in range(len(cluster_and_unique_months_lst)-1):
                if abs(cluster_and_unique_months_lst[i] - cluster_and_unique_months_lst[i+1])>1:
                    final_clusters_to_delete.add(cluster)
        # print("5th fileter", final_cluster_selected, final_clusters_to_delete)

        # if some cluster covers only one month and the amount is wayoff than other clusters then remove that cluster having one month
        one_month_only_clusters = {cluster for cluster, unique_sal_months in cluster_and_unique_months.items() if len(unique_sal_months)==1}
        more_than_one_month_clusters = set( list(cluster_and_unique_months.keys())+list(sal_key_cluster_and_unique_months.keys()) ) - one_month_only_clusters
        # print("one_month_only_clusters, more_than_one_month_clusters", one_month_only_clusters, more_than_one_month_clusters)
        # sal_cluster is the cluster with highest number of salaries detected
        cluster_with_max_noof_unique_months = -2
        max_noof_unique_months = 0
        sal_and_non_sal_cluster_and_unique_months = cluster_and_unique_months.copy()
        sal_and_non_sal_cluster_and_unique_months.update(sal_key_cluster_and_unique_months)
        # print("sal_and_non_sal_cluster_and_unique_months", sal_and_non_sal_cluster_and_unique_months)
        for cluster in more_than_one_month_clusters:
            if len(sal_and_non_sal_cluster_and_unique_months[cluster]) > max_noof_unique_months:
                max_noof_unique_months = len(sal_and_non_sal_cluster_and_unique_months[cluster])
                cluster_with_max_noof_unique_months = cluster

        # print("cluster_with_max_noof_unique_months", cluster_with_max_noof_unique_months)
        # print("6th fileter", final_cluster_selected, final_clusters_to_delete)

        if cluster_with_max_noof_unique_months!=-2:
            avg_sal_of_biggest_cluster = df_3large[df_3large['cluster']==cluster_with_max_noof_unique_months]['amount'].mean()
            clusters_to_remove = [cluster for cluster in one_month_only_clusters if abs(df_3large[df_3large['cluster']==cluster]['amount'].mean()-avg_sal_of_biggest_cluster)>avg_sal_of_biggest_cluster*0.2 and cluster!=max_noof_unique_months]
            # print("it is coming to this line", clusters_to_remove)
            # clusters_to_remove = [cluster for cluster in one_month_only_clusters if abs(df_3large[df_3large['cluster'] == cluster]['amount'].mean() - avg_sal_of_biggest_cluster) > 10000]
            for cluster in clusters_to_remove:
                final_clusters_to_delete.add(cluster)
        # print("7th fileter", final_cluster_selected, final_clusters_to_delete)

        final_cluster_selected = {i: j for i, j in final_cluster_selected.items() if j not in final_clusters_to_delete}
        # print("6th fileter", final_cluster_selected, final_clusters_to_delete)
        # at last check if the unique months till now is <= 2, then remove all the cluster
        if len(final_cluster_selected.keys())==2:
            if not abs(df_3large.loc[list(final_cluster_selected.keys())[0], 'sal_month'] - df_3large.loc[list(final_cluster_selected.keys())[1], 'sal_month'])<=1:
                final_cluster_selected = {}
        if len(final_cluster_selected.keys())<2:
            final_cluster_selected = {}
        # print("after removing clusters with less than 2 length", final_cluster_selected)

        # adding one more filter, this is since v2.2
        # REASON: there are some cases where we will get one extra record at the top

        return final_cluster_selected

    except Exception as e:
        print("Exception in salary filter function")
        raise e
        return {}



def name_or_comp_pred(cleaned_narration, name_comp_model):
    if re.search(r'(n)?achcr|export|import|pvtltd|myloancare|resour|micro|bulk\W*post|facility|infot|staff|manage|trad(e|i)|consult|\bcorp\b|market|\btech|plant|plastic|uber|india|enter()?p|trade|corporate|diagnos|service|\bpvt\b|made|\bfood\b|\bltd\b|private|limit|\bpriv(a)?\b|\bsol\b|solution|business|engine|jewel|\bfina\b|finan|motor|maruti', cleaned_narration.lower()):
            return '__label__company', 1.0
    if len(cleaned_narration.split(' ')) >= 2:
        a = cleaned_narration.split(' ')
        res = ' '.join(j for j in a[1:])
        pred = name_comp_model.predict(res)
        if pred[1][0] < 0.70 and pred[0][0] == '__label__name':
            return "__label__company", pred[1][0]
        else:
            return pred[0][0], pred[1][0]
    else:
        pred = name_comp_model.predict(cleaned_narration)
        return pred[0][0], pred[1][0]



def salary_with_out_keyword(df):
    print("inside salary soft logic", df.shape)
    if df.empty:
        return [], {}, pd.DataFrame()
    sal_start_time = time()

    # t1 = time()
    # print("model loading time", time()-t1)
    # print('=================salary inside func: ', psutil.cpu_percent(2))

    global name_comp_model
    name_comp_model = fasttext.load_model('./categorization_models/ft_name_or_comp_2.2.bin')
    # name_comp_model = fasttext.load_model('/home/ramnaryanpanda/Documents/ds_utility_codebackup/name_vs_comp/weights/good_80epc_10dim_1wng_2ws_3maxn_2minn_1mincnt.bin')

    try:
        # t1 = time()
        start_date, end_date = pd.to_datetime(df['date']).min(), pd.to_datetime(df['date']).max()
        month_diff = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1

        df['min_year'] = pd.to_datetime(df['date']).min().year
        df['min_month'] = pd.to_datetime(df['date']).min().month
        df['cur_year'] = pd.to_datetime(df['date']).dt.year
        df['cur_month'] = pd.to_datetime(df['date']).dt.month
        df['cur_date'] = pd.to_datetime(df['date']).dt.day
        df['sal_month'] = df[['min_year', 'min_month', 'cur_year', 'cur_month', 'cur_date']].apply(get_salary_month, axis=1)
        df['index_soft'] = df.index
        # print("extract every column", time()-t1)

        # print(pd.to_datetime(pd.to_datetime(df['date']).max()).to_period('M') - pd.to_datetime(pd.to_datetime(df['date']).min()).to_period('M'))
        total_number_of_months = (pd.to_datetime(pd.to_datetime(df['date']).max()).to_period('M') - pd.to_datetime(pd.to_datetime(df['date']).min()).to_period('M'))

        # print("tille point0", df.shape)
        unique_sal_months = set(df[df['category']=='salary']['sal_month'].unique())
        model_detected_sal = df[df['category'] == 'salary'].index.tolist()
        # print("model_detected_sal", model_detected_sal)

        # else come and do the clustering, in below steps
        # step1: filter for amount>10000 and category==transferin
        # step2: groupby month and get 3 highest narrations from each month
        # step3: preprocess using function clean_function_clean_text_list, this will help in clustering
        # step4: remove all narrations with freq more than months*3
        # step5: cluster remaining narrations from step4, using the preprocessed narrations
        # step6: use ft to filter only the clusters with company names
        # step7: how to choose cluster out of all the clusters formed in step6
        #      case1: if we have N company cluster(s), then take all the company clusters
        #      case2: if we have only person cluster(s), then dont take anything, here there won't be salary if the model did not predict,
        #             or else only the records predicted by model will be considered as salary
        # step8: find all the narrations similar to the final cluster using cleaned_narration
        # step9: add all the narrations from step8 as salary

        # t1 = time()
        df['transaction_date'] = pd.to_datetime(df['date'], utc=True)
        # df = df[df['category'].str.lower().str.startswith('transfer')]
        df['cleaned_narration'], df['cleaned_narration_ft'] = zip(*df[['narration', 'category']].apply(clean_function_new_new, axis=1))
        # df = preprocess_cleaned_func_output(df)
        df.loc[((df['category']=='salary') & (df['cleaned_narration']=='')), 'cleaned_narration'] = 'emptysal'
        # print("clean narration", time()-t1)

        # step1
        # t1 = time()
        df['is_remove'] = df[['narration', 'category']].apply(remove_narrations, axis=1) #this will mark only transferin records

        # print("tille point1", df.shape)
        df_3large = df[((df['amount'] >= 8000) & (df['is_remove'] == "") & (df['cleaned_narration']!='')) | (df['category'].str.lower()=='salary')]
        # print("df_3large.index", df_3large.index.tolist())

        try:
            assert len(df_3large)>0
        except AssertionError:
            # this means there are no transferin narrations(except upi,imps,transfer-inb) with amount>8000
            print("length of filtered df is zero")
            return [], {}, pd.DataFrame()
        # print("time for step1 to complete", time()-t1)

        # step2
        # t1 = time()
        # df_3large = df_filtered[df_filtered['amount']>=10000]
        # print("time for step2 to complete", time() - t1)

        # step3
        # t1 = time()
        cleaned_text_list = list(zip(df_3large['cleaned_narration'].index, df_3large['cleaned_narration'].tolist()))
        # print("cleaned_text_list", cleaned_text_list)
        # print("time for step3 to complete", time() - t1)

        # step4
        # t1 = time()
        cleaned_text_list = removing_narrations_higher_than_threshold(df_3large, cleaned_text_list, month_diff * 3, df_3large)

        if len(cleaned_text_list)==0:
            print("length of cleaned list is zero")
            return [], {}, pd.DataFrame()
        # print("time for step4 to complete", time() - t1)

        # step5
        # t1 = time()
        cluster_dict = clustering(cleaned_text_list)
        # print("cluster_dict", cluster_dict)
        for key in model_detected_sal:
            cluster_dict[key] = -1
        # print("time for step5 to complete", time() - t1)

        # step6, done above
        # t1 = time()
        df.loc[cluster_dict.keys(), 'NER_prediction'], df.loc[cluster_dict.keys(), 'score'] = \
            zip(*df.loc[cluster_dict.keys(), 'cleaned_narration_ft'].map(lambda x: name_or_comp_pred(x, name_comp_model=name_comp_model)))
        # print("time for step6 to complete", time() - t1)

        # step7
        # t1 = time()
        company_idx = []
        for idx in cluster_dict.keys():
            if df.loc[idx, 'NER_prediction'] == '__label__company' or cluster_dict[idx]==-1:
                company_idx.append(idx)
        # print("time for step7 to complete", time() - t1)

        # step 7B
        # first store all the months from the big cluster in one set, then comapre smaller clusters where we have extra months take records from those clusters
        # this will handle cases where  narrations are only a little bit different and falls in different clusters
        # t1 = time()
        filtered_cluster_dict = filter_clusters(cluster_dict, company_idx, df_3large, unique_sal_months, total_number_of_months)
        # print("this function is also done filter_clusters")
        # print("time for step8 to complete", time() - t1)
        # print("filtered_cluster_dict", filtered_cluster_dict)

        # step8
        # t1 = time()
        # this is to handle the case, (Added on oct 2023)
        # 1st month: 1600, 500, 234, 13456
        # 2nd month: 1236, 230, 123, 14523
        # 1st month: 1600, 423, 32, 18343
        # in this case if we remove remove all less than 8000, then later we can make these as rewards instead of salary,
        # similar_nar_idx = df[(df['cleaned_narration']==df.loc[idx, 'cleaned_narration']) & (df['amount']>=5000)].index.tolist()
        # neewly added & (df['amount']>=3000)

        final_sal_idx = set()
        # print("after func", filtered_cluster_dict)
        for idx in filtered_cluster_dict.keys():
            # df['cleaned_narration_substring'] = df['narration'].map(lambda x: pylcs.lcs_sequence_length(x, df.loc[idx, 'narration']))
            # similar_nar_idx = df[(df['cleaned_narration']==df.loc[idx, 'cleaned_narration']) | (df['cleaned_narration_substring']>50)].index.tolist()
            similar_nar_idx = df[df['cleaned_narration']==df.loc[idx, 'cleaned_narration']].index.tolist()
            # print("similar_nar_idx", similar_nar_idx)
            sub_df = df.loc[similar_nar_idx, ['index_soft', 'sal_month', 'amount']]
            sub_df = sub_df[sub_df['amount']>3000]
            sub_df.drop(columns=['amount'], inplace=True)
            months_count = sub_df.groupby('sal_month').agg({"index_soft": lambda x: x.nunique()})
            if months_count[months_count['index_soft'] > 4].shape[0] > 1 and filtered_cluster_dict[idx]!=-1:
                continue
            # print("similar_nar_idx", similar_nar_idx)
            final_sal_idx.update(set(similar_nar_idx))
        # print("final_sal_idx=======", final_sal_idx)
        # print("time for step9 to complete", time() - t1)
        # df.loc[list(final_sal_idx), 'category'] = 'salary'

        # these are indexes which are present more than month*3 times or present less than month-2 times
        # finally again remove narrations with count>month*3 and count<month-2
        # df['total_clsuters'] = len(cluster_dict)
        # df.loc[list(cluster_dict.keys()), 'cluster'] = list(cluster_dict.values())
        # print("Total time taken by salary soft logic", time() - sal_start_time)
        # print("tille point1", df.shape)


        # if only one cluster is present and that is only for one month then do not consider that cluster
        df_check = df[df['amount']>=8000]
        if len(df_check.loc[list(final_sal_idx), 'cur_month'].dropna().unique().tolist())==1:
            # print("printing type", type(final_sal_idx))
            final_sal_idx = set()

        # return df, sal_preproc_time, time()-sal_start_time
        # print("---------------Salary completed----------------")
        return final_sal_idx, cluster_dict, df[['cleaned_narration_ft', 'sal_month', 'NER_prediction']]

    except Exception as e:
        print("Exception in salary without keyword func")
        raise e
        logger.error("Exception occured at func: salary_soft_logic V3.0", extra={'var': var_type, 'type': 'EXCEPTION', 'cid': customer_id, 'bank_data_id': bank_data_id, 'exception': e})
        return [], {}, pd.DataFrame()



def loan_salary_with_out_keyword(df):
    try:
        t1 = time()
        # print("=====================Inside loan disbursed===============")

        loan_comp_lst = pd.read_csv("./ft_utils/loan_Salary_company_names.csv").values.tolist()

        stop_words = r"pvt|private|ltd|limited|finance|\bfin\b|service|finserv|pvtltd"

        if df.empty:
            return [], {}, pd.DataFrame()
        df['cleaned_narration'], df['cleaned_narration_ft'] = zip(*df[['narration', 'category']].apply(clean_function_new_new, axis=1))
        # df = preprocess_cleaned_func_output(df)
        disb_df = df[((df['category']=='loandisbursed') | (df['category']=='insurance') | (df['category']=='investmentincome'))]
        repay_df = df[(df['amount']<0) & ((df['category'].str.contains('loan')) | (df['category']=='insurance') | (df['category']=='investmentexpense'))]

        disb_and_repay_comps = set()
        user_disb_comps = set(disb_df.loc[disb_df['cleaned_narration'].str.len()>3, 'cleaned_narration'].unique())
        user_repay_comps = set(repay_df['narration'].unique())

        for user_disb_comp in user_disb_comps:
            user_disb_comp = re.sub(stop_words, "", user_disb_comp, flags=re.I)
            user_disb_comp = user_disb_comp.replace(' ', '')
            is_disb_comp_present_in_mapp = 0
            for comp in [comp[0] for comp in loan_comp_lst]:
                if comp in user_disb_comp:
                    is_disb_comp_present_in_mapp = 1
                    break
            if is_disb_comp_present_in_mapp==0:
                loan_comp_lst.append([user_disb_comp, user_disb_comp])


        # this dict is there to check the condition
        # here check the case if ach to repay comp or at least one amount<-3000 to repay comp or 3 amounts < -500 then add it to repay comp
        dct_with_repay_cnt = {}
        for repay_comp in set([i[1] for i in loan_comp_lst]):
            for ind in repay_df.index.tolist():
                user_repay_comp = repay_df.loc[ind, 'narration']
                if repay_comp in re.sub("\W+", "", user_repay_comp).lower():
                    is_ach_txn = False
                    if re.search(r"\b(n)?ach\b|\becs\b|(n)?ach\W*dr|ecs\W*dr|(n)?ach_|_(n)?ach|_ecs|ecs_", user_repay_comp.lower()):
                        is_ach_txn = True

                    # print(type(repay_df.loc[ind, 'date']))
                    if repay_comp not in dct_with_repay_cnt:
                        dct_with_repay_cnt[repay_comp] = {'user_repay_months':[repay_df.loc[ind, 'date'].month],
                                                          'amounts':[repay_df.loc[ind, 'amount']],
                                                          'is_ach_txn':is_ach_txn}
                    else:
                        # if we have found already one ach txn then make ach as True always, can be optimized, if we find one ach then break
                        if dct_with_repay_cnt[repay_comp]['is_ach_txn']==True:
                            is_ach_txn = True
                        dct_with_repay_cnt[repay_comp]['user_repay_months'].append(repay_df.loc[ind, 'date'].month)
                        dct_with_repay_cnt[repay_comp]['amounts'].append(repay_df.loc[ind, 'amount'])
                        dct_with_repay_cnt[repay_comp]['is_ach_txn'] = is_ach_txn

                    if is_ach_txn:
                        break

        # print(dct_with_repay_cnt)

        # run this logic only when there are loan repay records, otherwise no need to check this if only disb is there then just pass this to salary function
        if user_repay_comps:
            for user_disb_comp in user_disb_comps:
                # this if condition makes sure that the disbursal company should present in our list,
                # On removing this, we can not find if some company has some name in disbursal and has different name in loan repayment
                # that is why we are removing those, so that in the final list we only have companies which are there in our loan disburse list and are not there in loan repayment list
                # if use_it:
                if not [user_disb_comp for comp in [comp[0] for comp in loan_comp_lst] if comp in user_disb_comp.replace(' ', '')]:
                    disb_and_repay_comps.add(user_disb_comp)
                    continue

                for user_repay_comp in repay_df['narration'].str.lower():
                    is_break = False
                    for disb_comp, repay_comp in loan_comp_lst:
                        if disb_comp in user_disb_comp.replace(' ', '') and repay_comp in user_repay_comp.replace(' ', ''):
                            # print('==================if========')
                            # here check the case if ach to repay comp or at least one amount<-3000 to repay comp or 3 amounts < -500 then add it to repay comp
                            if ( dct_with_repay_cnt[repay_comp]['is_ach_txn']==True or
                                    len([amount for amount in dct_with_repay_cnt[repay_comp]['amounts'] if amount<=-500])>=3 or
                                    len([amount for amount in dct_with_repay_cnt[repay_comp]['amounts'] if amount <= -3000])>=1 ):
                                disb_and_repay_comps.add(user_disb_comp)
                                is_break = True
                                break
                    if is_break:
                        break
                    # print()

        # if loan_disb > 2 months:
        #     if any one ach txn is present in repay then make it as repay comp
        #     if ach is not present:
        #         then check if the debit amount for any one is > 3000 or the number of txns are greater than 2with amount > 500, Mpokket/SiCreva are disbursig every month, but also they are taking money back every month, so not an issue

        # print(user_disb_comps, disb_and_repay_comps)
        only_disb_comps = user_disb_comps - disb_and_repay_comps
        # print("only_disb_comps=============", only_disb_comps)
        if len(only_disb_comps)==0:
            return [], {}, pd.DataFrame()

        disb_df = disb_df[disb_df['cleaned_narration'].isin(only_disb_comps)]
        already_sal_df = df[df['category']=='salary']
        # print(disb_df.dtypes)

        # added the below if, cause we were having issues in detecting salary when one perfect salary is present, also loan disburse is present every month
        # in those cases we were making those loan disbursed as salary, so below I am checking if there are difference in months
        uniq_sal_months = set(already_sal_df['date'].astype('datetime64').dt.month.unique())
        uniq_disb_months = set(disb_df['date'].astype('datetime64').dt.month.unique())
        if len(uniq_disb_months-uniq_sal_months)>1 or len(uniq_sal_months)==0:
            # print("calling salary func inside loan func")
            ret_val = salary_with_out_keyword(disb_df)
        else:
            ret_val = [], {}, pd.DataFrame()
        print("Time taken for loan salary func: ", time()-t1)
        return ret_val

    except Exception as e:
        print("Exception is salary vs loan function: ", e)
        raise e
        ret_val = [], {}, pd.DataFrame()
        return ret_val
