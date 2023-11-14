import pandas as pd
import re
import logging
logger = logging.getLogger('bank_recat_logger')
var_type = 'Receiver_info'

def check_upi_handles(narration):
    try:
        category = ''
        msg = narration  # if sending series to the function
        #     msg = vect          # if sending text/a single msg to the function
        msg = msg.lower() if msg is not None else ''
        upi_regex = r'([a-z0-9.]*(@svc|@yespay|@yesbankltd|@yesbank|@yesb|@yes|@ybl|@yb|@yapl|@wasbi|@waicici|@wahdfcbank|@waaxis|@utib|@utbi|@upi|@united|@unionbankofindia|@unionbank|@ujvn|@ucobank|@uboi|@ubin|@ubi|@tjsb|@timecosmos|@tapicici|@syndicate|@synb|@sc|@sbls|@sbin|@sbi|@rmhdfcbank|@rbl|@ratn|@rajgovhdfcbank|@pytm|@punb|@postbank|@pockets|@pnb|@pingpay|@payzapp|@paytm|@pay|@oksbi|@okicici|@okicic|@okici|@okhdfcbank|@okhdfcba|@okhdfcb|@okhd|@okbizaxis|@okaxis|@okaxi|@oka|@ok|@obc|@myicici|@mvalu|@mahb|@lime|@lavb|@kvbl|@kvbank|@kvb|@kotak|@kota|@kmbl|@kmb|@kkbk|@kbl|@kaypay|@karurvysyabank|@jupiteraxis|@jkb|@jiopartner|@jio|@ippb|@iob|@indus|@indu|@indianbank|@indb|@ind|@imobile|@ikwik|@idib|@idfcfirst|@idfcbank|@idfb|@idbibank|@idbi|@icici|@icic|@ibl|@ibkl|@hsbc|@hdfcbankjd|@hdfcbank|@hdfc|@hdf|@freecharge|@fbpe|@fbp|@fbl|@ezeepay|@eazypay|@dbss|@dbs|@cnrb|@cmsidfc|@citibank|@centralbank|@cboi|@cbin|@boi|@bkid|@barodampay|@barb|@bandhan|@axs|@axl|@axisgo|@axisbank|@axisb|@axis|@axi|@axb|@aubank|@apl|@andb|@alla|@airtel|@airp|@abfspay))'
        match = re.findall(upi_regex, msg)
        upi_list = list()
        for upis in match:
            upi_handle = upis[0]
            if re.match(r'\d{1,2}@', upi_handle):
                upi_handle = re.findall(r'[a-z0-9.]* ?-?' + upi_handle, msg)[0]
            if re.match(r'\w@|^@', upi_handle):
                upi_handle = re.findall(r'[a-z0-9.]* ' + upi_handle, msg)[0]
            if re.search(upi_handle + '(?=\d+\.ifsc)', msg):
                if 'imps' in narration and 'ifsc' in narration:
                    upi_handle = re.findall(upi_handle + '\d+\.ifsc\.[a-zA-Z]*', msg)
                    if upi_handle:
                        upi_list.append(upi_handle[0])
                else:
                    pass
            else:
                upi_list.append(re.sub(r'^\W*', '', upi_handle))
        if len(upi_list) > 1:
            upi_handle = upi_list[1]
            category = 'Transfer to ' + upi_handle.upper()

        elif len(upi_list) == 1:
            upi_handle = upi_list[0]
            category = 'Transfer to ' + upi_handle.upper()
    except Exception as e:
        category = 'Transfer out'
    if not category:
        return 'Transfer out'
    else:
        return category


def cleaning_transfer_in(narration):
    custom_words = ['transfer', 'to', 'trans', 'inb', 't', 'upi', 'impsp', 'inwd', 'inet']
    cleaned_text = ' '.join([re.sub("\d+\w*", "", w) if (w.isalnum() and not w.isalpha() and not w.isdigit()) else w for w in narration.split()])
    cleaned_text = ' '.join([a for a in cleaned_text.split(' ') if a not in custom_words])
    cleaned_text = cleaned_text.replace('inwd', '').replace('inet', '').strip()
    return cleaned_text


def secondary_clean_narration(msg):
    if pd.isnull(msg):
        return ''
    msg = msg.lower()
    reg_remove_digits = r'\W(?:[0-9] ?){8,}\W(?:[0-9] ?){4,}\W|/(?:[0-9] ?){8,}/|~(?:[0-9] ?){8,}~|-\s?(?:[0-9] ?){8,}-|/(?:\d+\*+\d+)/|:(?:[0-9] ?){8,}:'
    reg_remove_dr = r'/(?:[drnaft] ?){2}/|~(?:[drnaft] ?){2}~|-(?:[drnaft] ?){2}-|\Wpayment from .*?\W|\Wverified merch.*?\W|\Wpay to .*?/|(?:rrn) [0-9]+/|/mob\W'
    reg_sub_upi = r'(upi/|/)\1+'
    reg_wdl_imps_sub = r'wdl-imps'
    reg_remove_time = r'(in |\d+ |/)([0-9]?[0-9]|2[0-9]):[0-9][0-9](:[0-9][0-9])?(/|-|:|$)'
    reg_remove_seq_txn = r'(?:txn |tx )(?:seq no.*id\s\w+)'

    if re.search(reg_remove_digits, msg):
        ext = re.findall(reg_remove_digits, msg)
        for each_prob_char in ext:
            msg = msg.replace(each_prob_char, '/')
    if re.search(reg_remove_time, msg):
        msg = re.sub(reg_remove_time, '/', msg)
    if re.search(reg_remove_dr, msg):
        ext = re.findall(reg_remove_dr, msg)
        for each_dr in ext:
            msg = msg.replace(each_dr, '/')
    if re.search(r'\d{2}([/\-])\d{2}([/\-])\d{4}', msg):
        msg = re.sub(r'\d{2}([/\-])\d{2}([/\-])\d{4}', '', msg)
    if re.search(reg_sub_upi, msg):
        msg = re.sub(re.search(reg_sub_upi, msg).group(), re.findall(reg_sub_upi, msg)[0], msg)
    if re.search(reg_wdl_imps_sub, msg):
        msg = re.sub(re.search(reg_wdl_imps_sub, msg).group(), 'wdl/imps', msg)
    if re.search(r'^.*impscub\d+:', msg):
        msg = re.sub(r'^.*impscub\d+:', 'imps/', msg)
    if re.search(r'\s?/\s?', msg):
        msg = re.sub(r'\s?/\s?', '/', msg)
    if re.search(r'^(?:neft|neft_out)(?:\Wdr|\Wmb)?(?:\W?\w+\d+\W)(?:(?:neft|neft_out)(?:\Wdr|\Wmb)?(?:\W?\w+\d+\W))?', msg):
        msg = re.sub(r'^(?:neft|neft_out)(?:\Wdr|\Wmb)?(?:\W?\w+\d+\W)(?:(?:neft|neft_out)(?:\Wdr|\Wmb)?(?:\W?\w+\d+\W))?', 'neft/', msg)
    if re.search(r'^(?:inf/inft/)', msg):
        msg = re.sub(r'^(?:inf/inft/)', 'inf/', msg)
    if re.search(reg_remove_seq_txn, msg):
        msg = re.sub(reg_remove_seq_txn, '', msg)
    if re.search(r'\W(?:oid\d+$)',msg):
        msg = re.sub(r'\W(?:oid\d+$)','/',msg)

    return msg


def initial_clean_narration(msg):
    ifsc_list = ['firn', 'adcc', 'barc', 'kaij', 'asbl', 'tsab', 'bcey', 'indb', 'prth', 'urbn', 'ibko', 'ntbl', 'psib', 'zsbl', 'utbi', 'jpcb', 'ibbk', 'nvnm', 'susb', 'ncub', 'adcb', 'soge', 'yesb', 'punb', 'sibl', 'nucb', 'sidc', 'gbcb', 'abna', 'bkid', 'ksbk', 'tssb', 'icic', 'kace', 'upcb', 'rssb', 'ujvn', 'ajhc', 'jsfb', 'mahb', 'deob', 'sahe', 'apmc', 'alla', 'bara', 'nnsb', 'aucb', 'msbl', 'stcb', 'ipos', 'vasj', 'nicb', 'andb', 'jasb', 'idib', 'ibkl', 'itbl', 'csbk', 'crub', 'aubl',
                 'gdcb', 'fino', 'vijb', 'qnba', 'kang', 'karb', 'sdcb', 'nosc', 'rnsb', 'sksb', 'kvgb', 'iduk', 'botm', 'hvbk', 'dohb', 'mslm', 'bkdn', 'airp', 'lavb', 'mdcb', 'svcb', 'tdcb', 'cosb', 'mcbl', 'tbsb', 'icbk', 'zcbl', 'amcb', 'mshq', 'sjsb', 'durg', 'kvbl', 'jiop', 'kgrb', 'sabr', 'clbl', 'ebil', 'oiba', 'krth', 'fdrl', 'koex', 'rscb', 'kdcb', 'kcbl', 'nspb', 'vara', 'harc', 'ubin', 'hcbl', 'pjsb', 'pmec', 'bcbm', 'utib', 'akjb', 'mhcb', 'ratn', 'nmcb', 'rmgb', 'nata', 'dnsb',
                 'njbk', 'jjsb', 'cnrb', 'hsbc', 'nkgs', 'rbih', 'bdbl', 'mdbk', 'barb', 'sutb', 'smcb', 'ctcb', 'ngsb', 'rrbp', 'synb', 'wbsc', 'bofa', 'abhy', 'citi', 'sbin', 'nmgb', 'tjsb', 'uovb', 'spcb', 'msci', 'msnu', 'dlsc', 'kucb', 'rsbl', 'amdn', 'orcb', 'kjsb', 'hpsc', 'gscb', 'sunb', 'dmkj', 'nbrd', 'vcob', 'eibi', 'tgmb', 'mvcb', 'thrs', 'kolh', 'sury', 'pucb', 'apbl', 'tmbl', 'pytm', 'rabo', 'esfb', 'bnpa', 'ttcb', 'vsbl', 'dicg', 'dlxb', 'mahg', 'jaka', 'klgb', 'kscb', 'hdfc',
                 'idfb', 'scbl', 'orbc', 'jsbl', 'apgb', 'kccb', 'bnsb', 'utks', 'smbc', 'pusd', 'snbk', 'sidb', 'dcbl', 'abpb', 'nesf', 'crly', 'sbls', 'csbx', 'fsfb', 'ioba', 'jsbp', 'corp', 'vvsb', 'bacb', 'knsb', 'nbad', 'mkpb', 'ctba', 'svbl', 'ccbl', 'srcb', 'ggbk', 'deut', 'wpac', 'kkbk', 'bbkm', 'pkgb', 'sant', 'mubl', 'cres', 'shbk', 'esmf', 'kbkb', 'dbss', 'chas', 'uucb', 'pmcb', 'ciub', 'anzb', 'apgv', 'tnsc', 'jana', 'svsh', 'sdce', 'cbin', 'ajar', 'rbis', 'ucba', 'trtr']
    if pd.isnull(msg):
        return ''
    msg = msg.lower()
    msg = msg.replace('~', '/')
    msg = msg.replace('|', '/')
    msg = re.sub(r'\s?\\\s?', '/', msg)
    reg_sub_double_slash = r'/\s+?/'
    reg_remove_ifsc = r'/(?:[a-z] ?){4}/|-(?:[a-z] ?){4}-'
    reg_remove_space_upi = r'@(?: ?[a-z] ?)+'  # remove spaces between UPI handles

    if re.search(reg_remove_ifsc, msg):
        extracted_ifsc_list = re.findall(reg_remove_ifsc, msg)
        for each_prob_ifsc in extracted_ifsc_list:
            if re.findall(r'\w+', re.sub(r'\s+', '', each_prob_ifsc))[0] in ifsc_list:
                msg = msg.replace(each_prob_ifsc, '-') if re.match(r'^-', each_prob_ifsc) else msg.replace(each_prob_ifsc, '/')


    if re.search(reg_remove_space_upi, msg):
        extracted_upi_list = re.findall(reg_remove_space_upi, msg)
        for each_prob_upi in extracted_upi_list:
            msg_split = msg.split(each_prob_upi)
            each_prob_upi = re.sub(r'\s+', '', each_prob_upi)
            msg = each_prob_upi.join(e for e in msg_split)
    if re.search(reg_sub_double_slash, msg):
        msg = re.sub(re.search(reg_sub_double_slash, msg).group(), '/', msg)
    return msg


def get_receiver(narration):
    if pd.isnull(narration):
        return 'Transfer out'
    narration = narration.lower()
    receiver = 'Transfer out'
    if 'upi' in narration:
        if '@' in narration:
            receiver = check_upi_handles(narration)
        elif ('/p2a/' in narration or '/p2m/' in narration) and '/' in narration:
            text_sub_cat = [a for a in narration.split('/')]
            receiver = 'Transfer to ' + text_sub_cat[3].upper().strip()
        elif '/' not in narration and '~' not in narration and '-' not in narration:
            text = cleaning_transfer_in(narration)
            if text:
                extraction = re.findall(r'(upi\d+)(.*)', text)
                if extraction:
                    receiver = 'Transfer to ' + str(extraction[0]).replace('(','')

    elif 'imps' in narration:
        if 'imps-' in narration and 'imps-dr' not in narration and 'money transfer' in narration:
            if len(narration.split('-')) >= 3:
                receiver = 'Transfer to ' + narration.split('-')[2].strip().upper()
        elif 'mb sent to' in narration:
            receiver = 'Transfer to ' + narration.split(' ')[3].strip().upper()
        elif 'imps to' in narration:
            receiver = 'Transfer to ' + narration.split('imps to')[-1].strip().upper()
        elif 'imps-rib/fund trf' in narration:
            if narration.split('/')[3] != 'na':
                receiver = 'Transfer to ' + narration.split('/')[3].strip().upper()
        elif 'imps outward' in narration and 'upi' in narration:
            receiver = 'Transfer to ' + narration.split('upi')[-1].strip().upper()
    if receiver == 'Transfer to ':
        receiver = 'Transfer out'
    receiver = receiver.replace('/', '').strip()
    if receiver == 'Transfer out':
        secondary_text_cleaning = secondary_clean_narration(narration)
        secondary_receiver = extract_secondary_receiver(secondary_text_cleaning)
        receiver = 'Transfer to ' + secondary_receiver if secondary_receiver != '' else 'Transfer out'  # + ' ' + secondary_text_cleaning
    if '(ref' in receiver.lower():
        receiver = receiver.lower().split('(ref')[0].strip().upper()
        receiver = re.sub(r"^TRANSFER TO ", "Transfer to ", receiver)
    if re.search(r'transfer to (p2a|imps|pay(ment)?|upi(intent| transaction)?|remarks|\d+|[a-z]{1,2})$', receiver, re.IGNORECASE):
        receiver = 'Transfer out'
    if re.search(r'payment from\s?phonepe',receiver):
        receiver = 'Transfer out'

    return receiver


def extract_secondary_receiver(msg):
    extracted_field = ''
    upi_ptr = r'(?:\bupi-dr/)([\w\s.@]+)|(?:\bupi-)([\w\s]+)|(?:\bupi/)([\w\s.@]+)|(?:upiout/)([\w\s.@-]+)|(?:vps/)([\w\s.@]+)'
    reg_debit_card = r'(?:debit card\W)(?:.*pos|.*pg)(?:\s?[a-z]+\d+)([\w\s]+)|(?:debit card\W)(?:.*pos|.*pg)(?:\s?\d+\s?(?:payu\W|raz\W|msw\W))([\w\s]+)|(?:debit card\W)(?:.*pos|.*pg)(?:\s?\d+)([\w\s]+)'
    reg_withdrawal_transfer = r'(?:withdrawal transfer)(?:.*to \d+)([\w\s]+)$|(?:chq withdrawal)(?: \d+)([\w\s.]+)$'
    reg_neft = r'(?:neft out )(?:.*/)([\w\s]+)$|(?:neft(?:/| to))([\w\s]+)'
    reg_mixed_mode = r'to transfer\W(?:to|inb)?([\w\s.@a/c]+)|purchase\W([\w\s.@*]+)|transfer to \d+([\w\s.@*]+)|trfr to\W([\w\s.@*]+)|money transfer dr\W([\w\s.@*]+)|(?:ecom\W)(?:pur\W|rupay\W?|\d+)?([\w\s.@*]+)|(?:(?:prcr from pos)|(?:prcr\W))((?:e-)?[\w\s.@*]+)|(?:mb:sent (?:money )?(?:to)?)(?:neft)?([\w\s.]+)|(?:pca/)([\w\s]+)|(?:pcd/\w+/)([\w\s*]+)|(?:ift\W)([\w\s.]+)|(?:tpt\W)([\w\s.]+)'
    reg_to_receiver = r'(?:to\W)([\w\s]+)'
    reg_pos_cleaning = r'(?:pos/e-pos\W?|pos\W\d+(?:x+\d+)?\W?|pos prch/?\s?pos\W?|pos-visa\W?|pos wdl\W?\d+|rupaypos\W?|pos txn at|pos\W?)'

    extracted_field_tuple = re.findall(upi_ptr, msg, re.IGNORECASE)
    if extracted_field_tuple:
        extracted_field_list = list(extracted_field_tuple[0])
        extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
    elif re.search(r'upiar/|mmt/|imdebit/|mob/|wdl/', msg):
        msg_split = msg.split('/')
        extracted_field = msg_split[2] if len(msg_split) > 2 else ''
    elif re.search(r'imps/|impsmb/|medr/|inf/', msg):
        msg_split = msg.split('/')
        msg_split = [i for i in msg_split if i]
        if msg_split:
            extracted_field = re.search(r'([\w\s.@]+)', msg_split[1]).group() if len(msg_split) > 1 else ''
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(r'payee(.*)na|upi fund transfer to(.*)with ref', msg):
        extracted_field_tuple = re.findall(r'payee(.*)na|upi fund transfer to(.*)with ref', msg, re.IGNORECASE)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
    elif re.search(reg_mixed_mode, msg):
        extracted_field_tuple = re.findall(reg_mixed_mode, msg)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(reg_debit_card, msg):
        extracted_field_tuple = re.findall(reg_debit_card, msg)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(reg_withdrawal_transfer, msg):
        extracted_field_tuple = re.findall(reg_withdrawal_transfer, msg)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(reg_neft, msg):
        extracted_field_tuple = re.findall(reg_neft, msg)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(reg_pos_cleaning, msg):
        msg = re.sub(reg_pos_cleaning, 'pos/', msg)
        extracted_field_list = re.findall(r'(?:pos/)(?:\W+)?((?:\w-)?[\w\s*]+)', msg)
        if extracted_field_list:
            extracted_field = extracted_field_list[0]
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif re.search(reg_to_receiver, msg):
        extracted_field_list = re.findall(reg_to_receiver, msg)
        if extracted_field_list:
            extracted_field = extracted_field_list[0]
            extracted_field = re.sub(r'\bin(\s\d+)?$|\b\d+$|^\d+', '', extracted_field.strip())
    elif not re.search(r'[_()/\|}{~:]', msg):
        extracted_field = msg
    elif re.search(r'^\d+', msg):
        extracted_field = 'A/c ' + re.match(r'^\d+', msg).group()
    return re.sub(r'^_|\bin(\s\d+)?$|\s\d+$|^\d+\s$|date', '', extracted_field.strip())


def receiver_info(vec):
    narration = vec[0]
    category = vec[1]
    try:
        if category == 'Transfer out':
            cleaned_narration = initial_clean_narration(narration)
            category = get_receiver(cleaned_narration)
        return category
    except Exception as e:
        logger.error("Exception occured at func: receiver_info",extra={'var': var_type, 'type': 'EXCEPTION', 'exception': e})
        return category