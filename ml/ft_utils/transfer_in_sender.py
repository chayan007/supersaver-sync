import pandas as pd
import re
import logging

logger = logging.getLogger('bank_recat_logger')
var_type = 'Sender_info'


def check_upi_handles(narration):
    try:
        category = ''
        msg = narration  # if sending series to the function
        #     msg = vect          # if sending text/a single msg to the function
        msg = msg.lower() if msg is not None else ''
        upi_regex = r'([a-z0-9.\s]*(@svc|@yespay|@yesbankltd|@yesbank|@yesb|@yes|@ybl|@yb|@yapl|@wasbi|@waicici|@wahdfcbank|@waaxis|@utib|@utbi|@upi|@united|@unionbankofindia|@unionbank|@ujvn|@ucobank|@uboi|@ubin|@ubi|@tjsb|@timecosmos|@tapicici|@syndicate|@synb|@sc|@sbls|@sbin|@sbi|@rmhdfcbank|@rbl|@ratn|@rajgovhdfcbank|@pytm|@punb|@postbank|@pockets|@pnb|@pingpay|@payzapp|@paytm|@pay|@oksbi|@okicici|@okicic|@okici|@okhdfcbank|@okhdfcba|@okhdfcb|@okhd|@okbizaxis|@okaxis|@okaxi|@oka|@ok|@obc|@myicici|@mvalu|@mahb|@lime|@lavb|@kvbl|@kvbank|@kvb|@kotak|@kota|@kmbl|@kmb|@kkbk|@kbl|@kaypay|@karurvysyabank|@jupiteraxis|@jkb|@jiopartner|@jio|@ippb|@iob|@indus|@indu|@indianbank|@indb|@ind|@imobile|@ikwik|@idib|@idfcfirst|@idfcbank|@idfb|@idbibank|@idbi|@icici|@icic|@ibl|@ibkl|@hsbc|@hdfcbankjd|@hdfcbank|@hdfc|@hdf|@freecharge|@fbpe|@fbp|@fbl|@ezeepay|@eazypay|@dbss|@dbs|@cnrb|@cmsidfc|@citibank|@centralbank|@cboi|@cbin|@boi|@bkid|@barodampay|@barb|@bandhan|@axs|@axl|@axisgo|@axisbank|@axisb|@axis|@axi|@axb|@aubank|@apl|@andb|@alla|@airtel|@airp|@abfspay))'
        match = re.findall(upi_regex, msg)
        upi_list = list()
        for upis in match:
            upi_handle = upis[0]
            if re.match(r'\d{1,2}@', upi_handle):
                upi_handle = re.findall(r'[a-z0-9.]* ?-?' + upi_handle, msg)[0]
            if re.match(r'\w@|^@', upi_handle):
                upi_handle = re.findall(r'[a-z0-9.]* ' + upi_handle, msg)[0]
            if re.search(upi_handle + '(?=\d+\.ifsc)', msg):
                pass
            else:
                upi_list.append(re.sub(r'^\W*', '', upi_handle))
        if len(upi_list) > 1:
            upi_handle = upi_list[1]
            category = 'Transfer from ' + upi_handle.upper()

        elif len(upi_list) == 1:
            upi_handle = upi_list[0]
            category = 'Transfer from ' + upi_handle.upper()
    except Exception as e:
        category = 'Transfer in'
    if not category:
        return 'Transfer in'
    else:
        return category


def cleaning_transfer_in(narration):
    custom_words = ['transfer', 'from', 'trans', 'inb', 't', 'upi', 'impsp', 'inwd', 'inet', 'transfer from']
    cleaned_text = ' '.join(
        [re.sub("\d+\w*", "", w) if (w.isalnum() and not w.isalpha() and not w.isdigit()) else w for w in
         narration.split()])
    cleaned_text = ' '.join([a for a in cleaned_text.split(' ') if a not in custom_words])
    cleaned_text = cleaned_text.replace('inwd', '').replace('inet', '').strip()
    return cleaned_text


def secondary_clean_narration_cr(msg):
    if pd.isnull(msg):
        return ''
    msg = msg.lower()
    reg_remove_digits = r'\W(?:[0-9] ?){8,}\W(?:[0-9] ?){4,}\W|/(?:[0-9] ?){8,}/|~(?:[0-9] ?){8,}~|-\s?(?:[0-9] ?){8,}-|/(?:\d+\*+\d+)/|:(?:[0-9] ?){8,}:|\s?[0-9]{3,}i|-\d{11,}$|/(?:\d+[dc]\W)|\W(?:cms\d+\W)|\W(?:rrn:\d+\w+)|\W?(?:n\d{10,}\s\d{1}-|n\d{10,}\W)|\W?(?:\d{11,12}\w{2}?\W)|\W(?:\d{11,})\W?|\W(?:\d{9})\W'
    remove_date_upi = r'\W(?:[a-z]+)\W\d{2}\.\d{2}\.\d{2,4}\W?'

    reg_imps_p2a = r'\W?(?:imps\Wp2a)\W|(?:imps/-/)'
    reg_remove_time_date = r'(in |\d+ |/)([0-1]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?(/|-|:|$)|/\d{2}-\d{2}-\d{1,}\W\d{5}:\d{2}:\d{2}/|/\d{2}-\d{2}-\d{6}\W\d{2}:\d{2}/|\d{1,2}[.]\s?\d{2}[.]\d{2,4}$'
    reg_mix = r'/(?:[cr] ?){2}/[0-9]+/|(?:rrn) [0-9]+/|/(?:trtr|trrr)|/(?:\d+){12}/|/\W{2}[0-9]+/|/[0-9]{2}/|\Wpayment from .*?\W|(?:rrn) [0-9]+/|(?:rrn\W\w+\W)|(?:rrn\W\d+\W)|\s?\d{1,2}[.-]\d[1,2][.-]\d{2,4}|(?::n\d+/)|(?::\d+dc/)|(?:/p\d+/)'

    remove_cr_spec = r'\W(?:[cr] ?){2}\W|(?:/axiscn/)|/\d{1,3}\s?[\w{1}]\d+$'
    reg_sub_spec_exc = r'/\W{2}[0-9]+/|/[0-9]{2}/'
    reg_neft = r'(?:neft_in\W)|(?:neft\Wcr\W)|(?:neft\W)|(?:neft\W)|(?:\W?neft\W[a-z]{4}0[a-z]{4,}\d{2,})|(?:\Wneft\W)'
    reg_cr_neft = r'(?:neft) ?[a-z]{2}-\w?\d{4,}-|\W(?:neft\s?)'
    p2a_sub = r'\W?(?:upi/p2a)\W?|\W?(?:upi/p2v)\W?|(?:upi from)|(?:upi\s?in)'
    reg_cms_saa = r'(?:/cms[0-9]{10,13})|\W?(?:saa?)[0-9]{9}\W|\W(?:[a-z]+[0-9]){18,}/|\W(?:[a-z]+[0-9]){18,}/|\W(?:[a-z]+[0-9]{18,}\W)|\s[a-z0-9]{11}\W(?:m/s)|(?:[a-z]{6}[0-9]{10})$|\s[a-z0-9]{11}\W(?:m/s)|\W[a-z0-9]{11}\W(?:\W?m/s\s)|/bk0\d+/|/bk+[0-9]+/|/bs+[0-9]+/'

    reg_ref = r'(?:in\d+\w+\d+ )?\W(?:ref\W ?).*$|(?:transaction id\s\W.*)$|(?:a/c.*)$|(?:reference\s?no\s?\W?.*)$|\s?(?:nodal\s?\W?.*)?$|(?:prin2on.*)$'
    reg_mix_num = r'\W?(?:[a-z]{3}[0-9]{8})\W$|(?:/-/)'
    reg_upi_dr = r'/dr-rev/'
    reg_sls = r'\W?(?://|/\s/)\W?'
    reg_ms = r'\W?\s?(?:m/s)\W?\s?|/\w{1}/|/cash/|/me/|/done/|/bill\s?payment/|/hi/|\W(?:hsbcn\d+\s?\d\W)|\W[s]\d{3,}\s?|/(?:sdc\d+)/|/axnp/|/inneft/|/axisc/|\W(?:[a-z]{4,5}\d+)\W|/\w{1}01/|/(?:kbcbm\w+/)|/my\s?ac/|/my/|/tr/'
    reg_by_trns = r'\W(?:amount\sreturn\W)|(?:\W?[in]{2}2[on]{2}\d+\W?)|\W?(?:\d{2,}op\W)|/na/|/\d+\W?/|/2xl/|/\d{1,2}th\s?\w+/|(?:/\d{1,2}\w{2}\s?total\W?\d+/)|/\d{1,2}\w{2}/|\W?\btoday\s?cod\b\W?|\Wifi\W|\btransfer\b|/transfer with id/|\bby\s?transfer\b\W|/utr\s?no\W\s?/|/dr/|(?:\W?ok\sdone\b)|/\bok\b|(?:\sok\sok)|\bfrm\b|\bremarks\b|/phon/|\bfrom\b|/na|/cf/|/collect/'  # change
    reg_alphnum = r'\W?\w{1,}\d{1,}(?:[a-z]+[0-9]+\w+)\W?|\W?\w{1,}\d{1,}\w{1,}-\d\w.*/|(?:cms\d+)$|\W(?:\d{1}\w{1}\d+\s\w{1}\w{2,})'
    reg_sub_upi_cr = r'(upi/|/)\1+'

    if re.search(r'/(?:\d{1,2}-\d{1,2}-?\d{4}?)', msg):
        msg = re.sub(r'/(?:\d{1,2}-\d{1,2}-?\d{4}?)', '/', msg)

    if re.search(reg_remove_digits, msg):
        ext = re.findall(reg_remove_digits, msg)
        for each_prob_num in ext:
            msg = msg.replace(each_prob_num, '/')

    if re.search(p2a_sub, msg):
        ext_p2a = re.findall(p2a_sub, msg)
        for each_p2a in ext_p2a:
            msg = msg.replace(each_p2a, 'upi/')

    if re.search(reg_imps_p2a, msg):
        ext_p2a = re.findall(reg_imps_p2a, msg)
        for each_prob_imps in ext_p2a:
            msg = msg.replace(each_prob_imps, 'imps/')

    if re.search(reg_mix, msg):
        ext = re.findall(reg_mix, msg, re.IGNORECASE)
        for each_cr in ext:
            msg = msg.replace(each_cr, '/')

    if re.search(reg_sub_upi_cr, msg):
        msg = re.sub(re.search(reg_sub_upi_cr, msg).group(), re.findall(reg_sub_upi_cr, msg)[0], msg)

    if re.search(remove_cr_spec, msg):
        extracted_spec = re.findall(remove_cr_spec, msg)
        for each_cr in extracted_spec:
            msg = msg.replace(each_cr, '/')

    if re.search(reg_sub_spec_exc, msg):
        extracted_star = re.findall(reg_sub_spec_exc, msg)
        for each_cr_sp in extracted_star:
            msg = msg.replace(each_cr_sp, '/')

    if re.search(reg_neft, msg):
        ext_neft = re.findall(reg_neft, msg)
        for each_neft in ext_neft:
            msg = msg.replace(each_neft, 'neft/')

    if re.search(reg_cr_neft, msg):
        ext_cr_neft = re.findall(reg_cr_neft, msg)
        for each_cr_neft in ext_cr_neft:
            msg = msg.replace(each_cr_neft, 'neft/')

    if re.search(reg_sls, msg):
        ext_sls = re.findall(reg_sls, msg)
        for each_sls in ext_sls:
            msg = msg.replace(each_sls, '/')

    if re.search(remove_date_upi, msg):
        ext = re.findall(remove_date_upi, msg)
        for i in ext:
            msg = msg.replace(i, '')

    if re.search(r'^.*upiab/|upi-', msg):
        msg = re.sub(r'^.*upiab/|upi-', 'upi/', msg)

    if re.search(reg_remove_time_date, msg):
        msg = re.sub(reg_remove_time_date, '/', msg)

    if re.search(r'(?:imps\Wtransfer/)', msg):
        msg = re.sub(r'(?:imps\Wtransfer/)', 'imps/', msg)
    # additionals....
    if re.search(reg_cms_saa, msg):
        ext = re.findall(reg_cms_saa, msg)
        for each_cms in ext:
            msg = msg.replace(each_cms, '/')

    if re.search(reg_ref, msg):
        ext_ref = re.findall(reg_ref, msg)
        for each_ref in ext_ref:
            msg = msg.replace(each_ref, '')
    if re.search(reg_mix_num, msg):
        ext_reg_mix = re.findall(reg_mix_num, msg)
        for each_ext in ext_reg_mix:
            msg = msg.replace(each_ext, '')

    if re.search(reg_upi_dr, msg):
        ext = re.findall(reg_upi_dr, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '/')

    if re.search(reg_ms, msg):
        ext = re.findall(reg_ms, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '/')

    if re.search(reg_by_trns, msg):
        ext = re.findall(reg_by_trns, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '/')

    if re.search(reg_alphnum, msg):
        ext = re.findall(reg_alphnum, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '')

    if re.search((r'/\s?\w{1}\s?/'), msg):
        msg = re.sub(r'/\s?\w{1}\s?/', '/', msg)

    if re.search(reg_sls, msg):
        ext = re.findall(reg_sls, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '/')

    if re.search(r'(neft/)\1+', msg):
        msg = re.sub(r'(neft/)\1+', 'neft/', msg)

    if re.search(r'(?:imps/\d+)', msg):
        msg = re.sub(r'(?:imps/\d+)', '', msg)

    if re.search(r'\W?(?:[a-z]{4}0.*)$|\W(?:value date.*)$', msg):
        msg = re.sub(r'\W?(?:[a-z]{4}0.*)$|\W(?:value date.*)$', '', msg)

    if re.search(r'\bto\b', msg):
        msg = re.sub(r'\bto\b', '', msg)

    if re.search(r'\W\w{1}\s?$', msg):
        msg = re.sub(r'\W\w{1}\s?$', '', msg)

    if re.search(r'/\d{1}\W|(?:0+/)|(?:fps\d+r/)|/fund/', msg):
        msg = re.sub(r'/\d{1}\W|(?:0+/)|(?:fps\d+r/)|/fund/', '/', msg)

    if re.search(r'/\s?0+$', msg):
        msg = re.sub(r'/\s?0+$', '', msg)

    if re.search(r'\W(?:bw\d+)\W', msg):
        msg = re.sub(r'\W(?:bw\d+)\W', '', msg)

    if re.search(r'\W\d{4}\W?$', msg):
        msg = re.sub(r'\W\d{4}\W?$', '', msg)

    if re.search(r'by\s?\W', msg):
        msg = re.sub(r'by\s?\W', '', msg)

    if re.search(r'(\W?from\W?)\1+|(?:[.]$)', msg):
        msg = re.sub(r'(\W?from\W?)\1+|(?:[.]$)', '', msg)

    if re.search(r'/(?:\d+dc)/', msg):
        msg = re.sub(r'/(?:\d+dc)/', '/', msg)

    if re.search(reg_sub_upi_cr, msg):
        msg = re.sub(re.search(reg_sub_upi_cr, msg).group(), re.findall(reg_sub_upi_cr, msg)[0], msg)

    return msg


def initial_clean_narration_cr(msg):
    ifsc_list = ['firn', 'adcc', 'barc', 'kaij', 'asbl', 'tsab', 'bcey', 'indb', 'prth', 'urbn', 'ibko', 'ntbl', 'psib',
                 'zsbl', 'utbi', 'jpcb', 'ibbk', 'nvnm', 'susb', 'ncub', 'adcb', 'soge', 'yesb', 'punb', 'sibl', 'nucb',
                 'sidc', 'gbcb', 'abna', 'bkid', 'ksbk', 'tssb', 'icic', 'kace', 'upcb', 'rssb', 'ujvn', 'ajhc', 'jsfb',
                 'mahb', 'deob', 'sahe', 'apmc', 'alla', 'bara', 'nnsb', 'aucb', 'msbl', 'stcb', 'ipos', 'vasj', 'nicb',
                 'andb', 'jasb', 'idib', 'ibkl', 'itbl', 'csbk', 'crub', 'aubl',
                 'gdcb', 'fino', 'vijb', 'qnba', 'kang', 'karb', 'sdcb', 'nosc', 'rnsb', 'sksb', 'kvgb', 'iduk', 'botm',
                 'hvbk', 'dohb', 'mslm', 'bkdn', 'airp', 'lavb', 'mdcb', 'svcb', 'tdcb', 'cosb', 'mcbl', 'tbsb', 'icbk',
                 'zcbl', 'amcb', 'mshq', 'sjsb', 'durg', 'kvbl', 'jiop', 'kgrb', 'sabr', 'clbl', 'ebil', 'oiba', 'krth',
                 'fdrl', 'koex', 'rscb', 'kdcb', 'kcbl', 'nspb', 'vara', 'harc', 'ubin', 'hcbl', 'pjsb', 'pmec', 'bcbm',
                 'utib', 'akjb', 'mhcb', 'ratn', 'nmcb', 'rmgb', 'nata', 'dnsb',
                 'njbk', 'jjsb', 'cnrb', 'hsbc', 'nkgs', 'rbih', 'bdbl', 'mdbk', 'barb', 'sutb', 'smcb', 'ctcb', 'ngsb',
                 'rrbp', 'synb', 'wbsc', 'bofa', 'abhy', 'citi', 'sbin', 'nmgb', 'tjsb', 'uovb', 'spcb', 'msci', 'msnu',
                 'dlsc', 'kucb', 'rsbl', 'amdn', 'orcb', 'kjsb', 'hpsc', 'gscb', 'sunb', 'dmkj', 'nbrd', 'vcob', 'eibi',
                 'tgmb', 'mvcb', 'thrs', 'kolh', 'sury', 'pucb', 'apbl', 'tmbl', 'pytm', 'rabo', 'esfb', 'bnpa', 'ttcb',
                 'vsbl', 'dicg', 'dlxb', 'mahg', 'jaka', 'klgb', 'kscb', 'hdfc',
                 'idfb', 'scbl', 'orbc', 'jsbl', 'apgb', 'kccb', 'bnsb', 'utks', 'smbc', 'pusd', 'snbk', 'sidb', 'dcbl',
                 'abpb', 'nesf', 'crly', 'sbls', 'csbx', 'fsfb', 'ioba', 'jsbp', 'corp', 'vvsb', 'bacb', 'knsb', 'nbad',
                 'mkpb', 'ctba', 'svbl', 'ccbl', 'srcb', 'ggbk', 'deut', 'wpac', 'kkbk', 'bbkm', 'pkgb', 'sant', 'mubl',
                 'cres', 'shbk', 'esmf', 'kbkb', 'dbss', 'chas', 'uucb', 'pmcb', 'ciub', 'anzb', 'apgv', 'tnsc', 'jana',
                 'svsh', 'sdce', 'cbin', 'ajar', 'rbis', 'ucba']

    if pd.isnull(msg):
        return ''
    msg = msg.lower()
    msg = msg.replace('~', '/')
    reg_sub_double_slash = r'/\s{0,}?/'

    reg_special = r'(?:[a-z]{4}0[a-z]{6}\W[a-z]{5}[0-9]+\W)|\W(?:[a-z]{4}[0-9]+\W?)\W(?:cms\d+\W)\W?|\W[0-9]{5,8}\W?$|\W?(?:normal\d{13,}/)|-[a-z]+[0-9]{14,}-|/[a-z0-9]{19,}/|/[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{11}/|[a-z0-9]{13,}\s[a-z0-9]{10,}/|[a-z0-9]{8}\s\w{4}\s[a-z0-9]{8}/|/[a-z0-9]{8}\s[a-z0-9]{4}\s\d{4}\s[a-z0-9]{4}/|/[a-z0-9]{12,}-w/\W?|/[a-z0-9]{6,}\s?[a-z0-9]{13,}$|(?:na\sq\d{8,}\s?.*)$|\Wm\d+\w{1}\d+\W|\W(?:fbbt\d+)\W|-(?:\d+dc-)|\W?(?:barb\W)|(?:barb\w+\d+\s?\w\W)|^\w{1}/|\W(?:sbin\d{2,}\W)|/(?:out\s?of\s?\d+/)'
    salution_reg = r'(?:ms|mrs|mr|miss|master|mast)(.|. | . |.- |./ |.\) )?(?:\b)'
    reg_remove_ifsc = r'/\s?(?:[a-z] ?){4}/|-(?:[a-z] ?){4}-'
    reg_remove_space_upi2 = r'\s?(?:\d+-)\d+@|\s+@|\s+\d+@|\s+\W\d+|\W?\w?\d+@\s?'
    if re.search(reg_remove_ifsc, msg):
        extracted_ifsc_list = re.findall(reg_remove_ifsc, msg)
        for each_prob_ifsc in extracted_ifsc_list:
            if re.findall(r'\w+', re.sub(r'\s+', '', each_prob_ifsc))[0] in ifsc_list:
                msg = msg.replace(each_prob_ifsc, '/')

    if re.search(reg_special, msg):
        ext = re.findall(reg_special, msg)
        for each_ext in ext:
            msg = msg.replace(each_ext, '/')

    if re.search(salution_reg, msg):
        msg = re.sub(salution_reg, '', msg)

    if re.search(r'\W[a-z]{4}0[a-z]{2}\d{4}\W', msg):
        msg = re.sub(r'\W[a-z]{4}0[a-z]{2}\d{4}\W', '/', msg)

    if re.search(r'/;/', msg):
        msg = re.sub(r'/;/', ',', msg)

    if re.search(r'(?:ift/\w{2,4}\d+\W\w{3}.*/)', msg):
        msg = re.sub(r'(?:ift/\w{2,4}\d+\W\w{3}.*/)', 'ift/', msg)

    if re.search(r'(?:upi from)', msg):
        msg = re.sub(r'(?:upi from)', 'upi/', msg)

    if re.search(r'/\W?(?:\d{1,2}\W\d{1,2}/\d{4}\s\d{1,2}:\d{1,2}:\d{1,2})|/e01/', msg):
        msg = re.sub(r'/\W?(?:\d{1,2}\W\d{1,2}/\d{4}\s\d{1,2}:\d{1,2}:\d{1,2})|/e01/', '', msg)

    if re.search(reg_sub_double_slash, msg):
        msg = re.sub(re.search(reg_sub_double_slash, msg).group(), '/', msg)

    if re.search(reg_remove_space_upi2, msg):
        extracted_space_list = re.findall(reg_remove_space_upi2, msg)
        for each_prob_space in extracted_space_list:
            msg = msg.replace(each_prob_space, each_prob_space.strip())

    return msg


def get_sender(narration):
    if pd.isnull(narration):
        return 'Transfer in'
    narration = narration.lower()
    sender = 'Transfer in'
    if 'upi' in narration:
        if '@' in narration:
            sender = check_upi_handles(narration)
            if ('/p2a/|/p2m/' in narration) and '/' in narration:
                text_sub_cat = [a for a in narration.split('/')]
                if len(text_sub_cat) <= 3:
                    sender = 'Transfer in'
                elif re.match(r'^\d+$', text_sub_cat[3]) and len(text_sub_cat) > 3:
                    sender = 'Transfer from ' + text_sub_cat[4].upper().strip()
                else:
                    sender = 'Transfer from ' + text_sub_cat[3].upper().strip()

        elif '/' not in narration and '~' not in narration and '-' not in narration:
            text = cleaning_transfer_in(narration)
            if text:
                extraction = re.findall(r'upi\d+(.*)', text)
                if extraction:
                    sender = 'Transfer from ' + extraction[0]

    elif 'imps' in narration:
        if 'imps-' in narration and 'imps-cr' not in narration and 'money transfer' in narration:
            if len(narration.split('-')) >= 3:
                sender = 'Transfer from ' + narration.split('-')[3].strip().upper()
        elif 'imps-cr' in narration:
            sender = 'Transfer from ' + narration.split('/')[2].strip().upper()

        elif 'imps inward' in narration and 'upi' in narration:
            sender = 'Transfer from ' + narration.split('upi')[-1].strip().upper()

    if sender == 'Transfer from ':
        sender = 'Transfer in'
    sender = sender.replace('/', '').strip()
    if sender == 'Transfer in':
        secondary_text_cleaning = secondary_clean_narration_cr(narration)
        secondary_sender = extract_secondary_sender(secondary_text_cleaning)
        sender = 'Transfer from ' + secondary_sender if secondary_sender != '' else 'Transfer in'  # + ' ' + secondary_text_cleaning

    if '(ref' in sender.lower():
        sender = sender.lower().split('(ref')[0].strip().upper()

    if re.search(r'p2a|imps|\brev\b|reversal|\binb\b|\bme\b', sender):
        sender = 'Transfer in'

    if re.search(r'(?:bulk\s?posting\W?)\W?[a-z]{3,4}\W?', narration):
        sender = 'Transfer in'

    if re.search(r'(?:upi\Wrem\Wfailed\b)|\bsalary\s?payment\b|(?:/transfer\s?with\s?id\s?\d+\s?cf/)', narration):
        sender = "Transfer in"

    if 'transfer from ' in narration and narration.split('transfer from')[-1].strip().isdigit():
        sender = 'Transfer in'

    if re.search(
            r'\W?\s?(?:bundl\stechnologies)|\W?\s?(?:m/s\s?bundl\s?technologi\s?)|(?:/scbl\s?bundl\s?technologi\W?)|(?:bundl\s?tech)',
            narration):
        sender = 'Transfer from bundl technologies private limited'

    if re.search(r'\s?\W?(?:zomato\s?limited\s?\W?|\Wzomato\s?lim\W?|\bzomato\b)', narration):
        sender = 'Transfer from zomato limited'

    if re.search(
            r'\W?(?:branch\W.*)$|\W(?:account\W?validat|acc valida|a c valida|ac validat)\W|\W?refunded\W?|\btest\b|\bself\b|\bown\s?account\b|\breversed\b|\baccverifyk\b|\bbirthday\b|\bfunds transfer\b|\bfunds\b|\bverification\b|\bwithdrawal\b|\bauthentication\b|\bensure kyc aml\b|/(?:mb\W)|\bw2b\b|\bdefault\b|\breversal\b|\brvsl\b|acc validation by me|\brefund\b|\btrf\b|\W(?:thank)\W?|/accvalid/|/accvalidationby/',
            narration):
        sender = 'Transfer in'

    if re.search(r'(?:\\)', narration):
        sender = 'Transfer in'
    if re.search(r'transfer fund|transfer\s?cash|transfer\d{1,3}|\W(?:add\W?mone)\W?|\W?(?:whatsapp\s?payments)',
                 narration):
        sender = 'Transfer in'
    if re.search(r't-wallet', narration):
        sender = 'Transfer from T-Wallet'

    if re.search(r'(?:Transfer\sfrom\s?[x]+$\W?|[x]+>|[x]+!)|(?:page\s?\w{1,2})|\bpage\b|\bsheet\b|\bcomplete\b',
                 sender):
        sender = 'Transfer in'
    if re.search(r'rbi|rbis', narration):
        sender = 'Transfer from rbis'

    if re.search(r'(?:Transfer\sfrom\s?[x]+$\W?|[x]+>|[x]+!)', sender):
        sender = 'Transfer in'

    return sender


def extract_secondary_sender(msg):
    extracted_field = ''
    upi_ptr = r'(?:\bupi-)([\w\s]+)|(?:\bupi/)([\w\s.@-]+)|(?:upi/)([\w\s.@-]+)|(?:upi/p2a/)|(?:upi/cr/)([\w\s]+)'

    extracted_field_tuple = re.findall(upi_ptr, msg, re.IGNORECASE)
    if extracted_field_tuple:
        extracted_field_list = list(extracted_field_tuple[0])

        extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)

    elif re.search(r'upi:/|mmt/|imcredit/|upi/p2a/|/mob#|mob|ift', msg):
        msg_split = msg.split('/')
        extracted_field = msg_split[2] if len(msg_split) > 2 else ''
    elif re.search(r'imps/', msg):
        msg_split = msg.split('/')
        msg_split = [i for i in msg_split if i]
        if msg_split and len(msg_split) > 1 and re.search(r'([\w\s.@-]+)', msg_split[1]):
            extracted_field = re.search(r'([\w\s.@-]+)', msg_split[1]).group() if len(msg_split) > 1 else ''
    elif re.search(r'imps by ', msg) and re.search(r'(?:imps by )([\w\s]+)', msg):
        extracted_field = re.search(r'(?:imps by )([\w\s]+)', msg).group(1) if len(msg) > 1 else ''

    elif re.search(r'imps/p2a|/imps/p2a/', msg) and re.search(r'(?:transfer from)(\W[a-z0-9]+)', msg):
        extracted_field = re.search(r'(?:transfer from)(\W[a-z0-9]+)', msg).group(1) if len(msg) > 1 else ''

    elif re.search(r'neft/', msg) and re.search(r'(?:neft\W)([\w\s]+)', msg):
        extracted_field = re.search(r'(?:neft\W)([\w\s]+)', msg).group(1) if len(msg) > 1 else ''

    if re.search(r'neft/', msg):
        msg_split = msg.split('/')
        msg_split = [i for i in msg_split if i]
        if msg_split and len(msg_split) > 1 and re.search(r'([\w\s.@]+)', msg_split[1]):
            extracted_field = re.search(r'([\w\s.@]+)', msg_split[1]).group() if len(msg_split) > 1 else ''

    elif re.search(r'received from', msg) and re.search(r'(?:received\sfrom)(\s.*)', msg):
        extracted_field = re.search(r'(?:received\sfrom)(\s.*)', msg).group(1) if len(msg) > 1 else ''

    elif re.search(r'upi fund transfer from(.*)with ref', msg):
        extracted_field_tuple = re.findall(r'upi fund transfer to(.*)with ref', msg, re.IGNORECASE)
        if extracted_field_tuple:
            extracted_field_list = list(extracted_field_tuple[0])
            extracted_field = ",".join(string for string in extracted_field_list if len(string) > 0)

    return re.sub(r'^_|\bin(\s\d+)?$|\s\d+$|^\d+\s|date', '', extracted_field.strip())


def sender_info(vec):
    narration = vec[0]
    category = vec[1]
    try:
        if category == 'Transfer in':
            cleaned_narration = initial_clean_narration_cr(narration)
            category = get_sender(cleaned_narration)
        return category
    except Exception as e:
        logger.error("Exception occured at func: sender_info",
                     extra={'var': var_type, 'type': 'EXCEPTION', 'exception': e})
        return category