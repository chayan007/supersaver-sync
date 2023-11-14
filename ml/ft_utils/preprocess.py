import pandas as pd
from nltk.tokenize import RegexpTokenizer
import re
import re
import nltk
import warnings
warnings.filterwarnings('ignore')
tokenizer = RegexpTokenizer(r'\w+')
nltk.download('wordnet')


# this is same as clean_narration0  +  numbers - ""  +  xxxxx - ""
# def clean_narration1(text):
#     try:
#         text = text.lower()
#         ifsc_lst = r'(\bdicg|\butib|\bcrly|\bitbl|\bqnba|\babpb|\bjaka|\bkjsb|\bkcbl|\bsahe|\bupcb|\basbl|\bkbkb|\brnsb|\brbis|\bkarb|\brabo|\bdurg|\bkdcb|\bmslm|\bnesf|\bapbl|\bcrub|\borbc|\bsvsh|\bfdrl|\blavb|\bcnrb|\bjsfb|\bjana|\bjsbp|\bsibl|\bttcb|\bctba|\beibi|\bpayt|\bhsbc|\bebil|\bbacb|\bbofa|\bpsib|\bidfb|\bbara|\bknsb|\bkolh|\bmahb|\bsdcb|\bhdfc|\bbarc|\btsab|\bkrth|\bnspb|\bvvsb|\bsmcb|\bsmbc|\bnata|\bibko|\bpunb|\bdeut|\bkace|\bnosc|\btjsb|\brsbl|\bnicb|\bfino|\bprth|\babna|\bdlsc|\bsbls|\bncub|\btssb|\bjiop|\bmhcb|\babhy|\bsbin|\bsusb|\byesb|\bkccb|\bapmc|\bnmcb|\bmdbk|\bdohb|\bsvcb|\buovb|\bvcob|\bandb|\bgdcb|\bdlxb|\bsksb|\bvsbl|\bsidc|\bbcbm|\bratn|\bapgv|\bhvbk|\bnvnm|\bidib|\bmdcb|\bclbl|\baubl|\bciub|\bmahg|\bamdn|\bbcey|\bdmkj|\bpmec|\bsnbk|\bbkdn|\bubin|\bsunb|\bccbl|\bmubl|\bkang|\bajar|\bcbin|\bsrcb|\bjpcb|\bbnpa|\bibbk|\bdcbl|\bntbl|\bdeob|\bciti|\bsidb|\bvijb|\bbbkm|\bnbad|\bchas|\buucb|\bcres|\bctcb|\bnkgs|\bcsbx|\bsoge|\bsvbl|\bfsfb|\badcc|\bmkpb|\bpucb|\bksbk|\btnsc|\bkkbk|\bkoex|\bpkgb|\bkgrb|\boiba|\bggbk|\bgbcb|\bkana|\bwpac|\bpusd|\bkvgb|\bmvcb|\bpmcb|\bbarb|\bcosb|\bpjsb|\bbdbl|\bairp|\bbotm|\bsynb|\baucb|\bmsnu|\brssb|\bhpsc|\bibkl|\bsury|\bakjb|\bsdce|\bspcb|\btdcb|\bsabr|\brrbp|\bsutb|\bnjbk|\bnbrd|\bjsbl|\borcb|\bajhc|\bhcbl|\brscb|\bcsbk|\bstcb|\bzsb|\biduk|\bkucb|\bwbsc|\badcb|\bicic|\bfirn|\bipos|\bshbk|\bsant|\brbih|\bthrs|\bscbl|\bkaij|\balla|\bngsb|\bkvbl|\bnnsb|\bmsbl|\brmgb|\bbnsb|\bzcbl|\bdnsb|\bdbss|\btmbl|\bgscb|\burbn|\bioba|\bkscb|\bsjsb|\bmshq|\bnucb|\bpytm|\btbsb|\bamcb|\besfb|\bucba|\besmf|\bmsci|\bujvn|\butks|\butbi|\bmcbl|\bjjsb|\bapgb|\bindb|\btgmb|\bnmgb|\bklgb|\bharc|\bvasj|\banzb|\bbkid|\bjasb|\bicbk|\bvara)'
#         print(text)
#         text = re.sub(r"rtgs\s+" + ifsc_lst, "", text)
#         print(text)
#         print("\n\n")
#         text = re.sub(r"(x{3,}|[0-9]+|\*{3,}|^transfer to|^transfer from|^transfer credit|^transfer debit|^by chq|^imps|^neft|^upi|^debit|^credit|^by transfer|^withdrawal transfer|^wdl tfr|^to transfer|^by debit card|^by credit card|^money received received from|^money received using imps received from|^money received via upi received from|^money sent using upi sent to|^money sent using imps sent to|^paid in store using|^paid online using|^paid using your bank account paid successfully at)", "", text).strip()
#         text = ' '.join(tokenizer.tokenize(text))
#     except Exception as e:
#         text = ""
#         pass
#     return text if text!="" else " "*5


def clean_narration1(text):
    try:
        text = text.lower()
        text = re.sub(r"(x{3,}|[0-9]+|\*{3,}|by\W*transfer|to\W*transfer|^transfer to|^transfer from|^transfer credit|^transfer debit|^by chq|^imps|^neft|^upi|^debit|^credit|^by transfer|^withdrawal transfer|^wdl tfr|^to transfer|^by debit card|^by credit card|^money received received from|^money received using imps received from|^money received via upi received from|^money sent using upi sent to|^money sent using imps sent to|^paid in store using|^paid online using|^paid using your bank account paid successfully at|idfc(\W*first)?|bank)", "", text).strip()
        text = ' '.join(tokenizer.tokenize(text))
    except Exception as e:
        text = ""
        pass
    return text if text!="" else " "*5
