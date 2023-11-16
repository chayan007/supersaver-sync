from nltk.tokenize import RegexpTokenizer
import re
import nltk
import warnings
warnings.filterwarnings('ignore')
tokenizer = RegexpTokenizer(r'\w+')
nltk.download('wordnet')


class SubCategory:
    def __init__(self):
        # investment
        self.crypto_regex = r"coin(switch|dcx|ome|tracker|delta|gabbar|gecko|marketcap|store)|wazirx|zebpay|bitbns|(uno|buyu|un)coin|vauld|bitinning|giottus|btcx|lunoind|cryptowire|bitxoxo|koinly|neblio"
        self.fd_regex = r"(prema(ture|t|tu)?)\W*(credit|debit|db|cr|deb|cre|cred|clos)(.*)?(\brd|\bfd|rd\b|fd\b)|(\brd|\bfd|rd\b|fd\b|\btd|td\b)\W*(pre|post)?\W*clos|(debit|credit|deb|cre|db|cr)\W*sweep|(rd|fd|td)\W*(red(e|em)?|install|book|premat|maturity|through|draw|fund)|closure\W*proceeds|fixed\W*deposit\W*(rede|creat)|(installment|installm|acct|account)(.*)?(\brd|\bfd|rd\b|fd\b|\btd|td\b)|deposit\W*(closu|creat)|online(rd|fd)|rd\W*inst|sweep\W*(trf|transfer)\W*(from|to)|maturity\W*claim|(fixed|flexi|term|recu((r)?ring)?)\W*dep|(\bfd\b|\brd\b|\btd\b)(.*)(b( )?o( )?o( )?k|proce)"
        self.share_regex = r"stock|angel\W*(bro|nse|bse|tra|one)|rksvsecu|sharekhan|sharemarket|sharesandholding|zerodha|infoline|choiceequity|coimbatorecap|(bse|nse)\W*ltd"
        self.mf_regex = r"mutu(al)?fun|mutualf|pruicic|(tata|dsp|kotak(mahindra)?|mahindra|birla|ppfas|idfc|sbi|hdfc|mirae|icici\W*(pru(dential)?)|axis|pnb|paytmmoney|nippon|navi|quant|birlasunlife|edelweiss|paribas|motilal|hsbc|samco|sundar(am)?|uti|km|invesco|franklin|ft|robeco|cr)(mf|mut|asset|secu)|miraeasset|paragparikh|prumf|navi(redemp|amc)|mf\W*utilities|nippon\W*(life)?\W*ind(ia)?|cclmf|(flexi|long|multi|small|large|med(ium)?)\W*cap|licmf|alice\W*blue"
        self.share_regex_caps = r"\b(N|B)SE\b"
        self.small_savings_caps = r"\bEPF\b|\bPPF|PPF\b|\bPF\b|EPFO\b|\bEPFO|\bAPY|APY\b|^APY|^EPF|PPF\b|\bPPF|^PF|^EPFO|ATAL\W*PENSION|PFMS|EPPF"
        self.small_savings_lower = r"provid(ent)?\W*fun|pension|\bppf\b|\bapy\b|\bepfo\b|\bpfo\b|\bepf\b|[0-9]{4}ppf[0-9]{3,}"
        self.dividend_regex = r"int\W*div|divdnd|dividend|fnldiv|int\W*spl\W*div|(div2|fnl|fin(al)?)[0-9]{2,}|findiv|dividend|finaldiv|fin(a)?(l)?set|fullandfin|provid(ent)?fun"

        # bills
        self.electric_regex = r"adani\W*elec|neepco|apepdcl|apdcl|bescom|dhbvn|gerc|guvnl|gescom|hescom|jbvnl|kpcl|kptcl|msedcl|mescom|njpc|\bntpc\b|rrvunl|tangedco|\bthdc\b|tgenco|tsspdcl|tpnodl|upjvnl|upptcl|uhbvn|uppcl|uprvun|\baerc\b|apnpdcl|apspdcl|aptranscorp|bsesdelhi|cercind|cescoorissa|delhividyut|dercind|dvcindia|ercap|gseb|ipgcl|\bh(p)?erc\b|hpseb|ireda|\bkerc\b|kseboa|meseb|mperc|mppkvvcl|msebindia|ndplonline|nhpcindia|\bnhpc\b|\bnpti\b|orierc|pfcindia|powercitykorba|powergridindia|psebindia|ptcindia|rajenergy|recindia|\brerc\b|\btneb\b|\btnerc\b|uperc|wberc|wbseb|(southco|wesco|eastco|nesco|hubli(e)?)\W*(orissa|elect)|\bbypl\b|\bcesc\b|(adani|(state)?\W*power|energy|vidyut|bijli|vijli|\bvij\b|(state)?\W*elect(ricity|rical|rification)?|delhi|urja\W*vikas|trans(mission)?)\W*(vitran|generation|(navi)?\W*mumbai|supply|company|\bcomp\b|transco|nigam|prasaran|dev(elopment)?|trans(mission)?|vit(a)?ran|manag(ement)?|finance|grid|system|trading|utpadan|licensing)?\W*(distr|nigam|limited|\bltd\b|regulatory|corp|board|operation|authority|holding|inspector|comp(any)?|utilit|depart|co\.)|damodar\W*val|\bppcl\b|(central|east|west|north|south|torrent)\W*(.*)\W*power|\btpddl\b|puvnl|(elec(tric)?(tricity)?|light|power)\W*(bil|suppl)|sbpdclrapd|npdcl|bil(l)?(s)?elec|ugvcl|kseb|dgvcl|pgvcl|cesc|wbsedcl|pspcl|vidyut\W*vi|(tata|sun|bihar|pradesh|orissa|odisha)\W*pow|tpdowl|avvnl|apcpdcl|bsesr|cspdcl|nbpdcl|mgvcl|mvvnl|jvvnl|pvvnl|dvvnl|pzelectricity|mspdcl|kesco|kseb|sspdcl|tpddl|tpcodl|puvvn|sbpdcl|tneb|tsnp|wbsedc|assam\W*pow|bil(l)?\W*desk(.*)elect|electricity|(tamilnadu|bangalore|kerala|kota|goa|bikaner|tripura|punjab)\W*(state)?\W*elect|mep"
        self.gas_regex = r"((pavan|kamrup)?\W*industrial|aavantika|adani|amardeep|akshay|green|deep\W*joythi|indraprastha|andhra\W*pradesh|bhagyanagar|star\W*special\W*air|gujarat|a\W*p|haryana\W*city|mahanagar|\W*|gspc)\W*gas(es)?|(hindustan|state|refin(ery)?)\W*(petro)|(amrit|vadilal)\W*(chem)|\bongc\b|ongc\W* vide|dahej\W*sez|vishwa\W*exports|sudha\W*anal|lpg\W*mumbai|ketko\W*san|green\W*power\W*international|aum\W*techno\W*ceramics|eco\W*fuel\W*systems|\bdnp\W*limited|aims\W*indus|wtn\W*enter|hindustan\W*aegis|rohan\W*automotive\W*equ|weatherford\W*oil\W*tool|jetex\W*carbur|bharat\W*oman|merchants\W*chamber|(iwatani|linde|praxair|\bbg|gail)\W*india|dolphin\W*motors|aegis\W*logistics|energy\W*comb|lpg\W*limited|anugraha\W*agen|vida\W*inter|ensci|helios\W*infra|indane|gas\W*bil"
        self.broadband_regex = r"\bbsnl|bsnl\b|bharat\W*sanch(ar)?|bharti\W*air|\bmtnl\b|(\bjio\b|reliance|power|ortel|edge|tata|hughes|verizon|vois|bhiwani|telenor|\bntt\b|videocon|bt\W*global|\bsify\b|telstra|swift\W*ma(il)?)\W*(info|net|tele|india)?\W*comm|(ometa|\bmft\b|readylink|cityzone|ishan|\bindi|space|tamana\W*wi|rajesh\W*patel|singh|sanyog|netmagic|siliguri|ankhnet|touch|gorakhpur|prime|multi|vinayaga(a)?|wish|bhilwara|hcl\W*com|\btata|tikona|kappa|wan\W*and\W*lan|tikona|five|bolindia|state\W*fibre|global|pacific|inative|\bwiwa|\bdish|north\W*east\W*(data(a)?)?)\W*((inter|info|infi|tele)?\W*net)|broadban|at&t|(nextra|japra|united|mahanagar|pulse|sprint|etisalat\W*db|sistema\W*shyam|tulip|tata|quadrant)\W*(tele)|adya\W*tech|airtalk\W*solu|bharat\W*sanchar|bharti\W*airtel|city\W*online|correl\W*it|descon|f\/x\W*wireless|\bgtpl\b|arya\W*omnitalk|ikf\W*tech|(procall|quickcalls|smartalk|shyam\W*spectra|micky\W*online|microscan\W*comp(uters)?)\W*(pvt|private)|railtel\W*corp|sify\W*tech|singtel\W*global|sistemos\W*info|smartx\W*serv|spectrum\W*softech|southern\W*online|symbios\W*creations|vcar\W*call\W*cent|vmobi\W*solu|vodafone\W*idea|orange\W*business|planetcast\W*media|netmagic\W*sol|manipal\W*e\W*comm|ai\W*rtel\W*dist|(cable|landlin(e)?)\W*bil|jio\W*(saavn|fiber|in|mobi|fiber)|(vi(l)?|airtel|jio)\W*(pos|pre|mobi)|\bdth\b|dth\W*dir|dish\W*tv|tata\W*(pla|sk)|hathway|\bd2h\b|vodafo|(pre|pos(t)?)\W*direc|\*\*(dband|a-sky|irect|obile|harge)|(pre|post)\W*pa|tata\W*sky|videocon|borad\W*b|dish\W*(tv|inf)|land\W*line|jioinapp|bsnl\W*land|sun\W*dir|tneb|(dth|d2h)\W*tv|d2heprs|dthd|dthre|suntv|tvnetwo|play\W*direct|docomo"

    def get_sub_category(self, df):
        df['sub_category'] = ""
        df.loc[df['category']=='Investment Income', 'sub_category'] = df.loc[df['category']=='Investment Income', 'narration'].map(self._investment_income)
        df.loc[df['category']=='Investment Expense', 'sub_category'] = df.loc[df['category']=='Investment Expense', 'narration'].map(self._investment_expense)
        df.loc[df['category']=='Bills & Utilities', 'sub_category'] = df.loc[df['category'] == 'Bills & Utilities', 'narration'].map(self._bills_utilities)
        return df

    def _investment_income(self, orig_narr):
        narr_lower = orig_narr.lower()
        narr_preproc = narr_lower.replace(" ", "")

        if 'penalty' in narr_lower:
            return "Others"

        if re.search(self.crypto_regex, narr_preproc):
            return "Crypto Transaction"

        if re.search(self.fd_regex, narr_lower):
            return "Fixed Deposit"

        if re.search(self.share_regex, narr_preproc) or re.search(self.share_regex_caps, orig_narr):
            return "Share Sell"

        if re.search(self.mf_regex, narr_preproc) or re.search(r"\bcams\b", narr_lower):
            return "MF Redemption"

        if re.search(self.small_savings_caps, orig_narr) or re.search(self.small_savings_lower, narr_lower):
            return "Small Savings"

        if re.search(self.dividend_regex, narr_lower):
            return "Dividend"

        return "Others"


    def _investment_expense(self, orig_narr):
        narr_lower = orig_narr.lower()
        narr_preproc = narr_lower.replace(" ", "")

        if 'penalty' in narr_lower:
            return "Others"

        if re.search(self.crypto_regex, narr_preproc):
            return "Crypto Transaction"

        if re.search(self.fd_regex, narr_lower):
            return "Fixed Deposit"

        if re.search(self.share_regex, narr_preproc) or re.search(self.share_regex_caps, orig_narr):
            return "Share Purchase"

        if re.search(self.mf_regex, narr_preproc) or re.search(r"\bcams\b", narr_lower):
            return "MF Purchase"

        if re.search(self.small_savings_caps, orig_narr) or re.search(self.small_savings_lower, narr_lower):
            return "Small Savings"

        return "Others"


    def _bills_utilities(self, orig_narr):
        narr_lower = orig_narr.lower()
        narr_preproc = narr_lower.replace(" ", "")

        if 'penalty' in narr_lower:
            return "Others"

        if re.search(self.electric_regex, narr_preproc):
            return "Electricity bill"
        if re.search(self.gas_regex, narr_preproc):
            return "Gas bill"
        if re.search(self.broadband_regex, narr_lower):
            return "Recharge & Broadband bill"

        return "Others"

