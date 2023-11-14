import pandas as pd
import numpy as np
import re


def loan_insurance_investment_debit_soft_lofic(row):
    try:
        orig_narration, category = row.iloc[0], row.iloc[1]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")

        # print("category", category)

        # to handle some false +ves
        if category == 'homeloan':
            if narration.startswith('pos'):
                return 'shopping&purchase'
            elif narration.startswith("to atm"):
                return "cashwithdrawal"
            elif re.search(r"\bhome\b|\bhouse\b", narration):
                return "transferout"

        if category == 'reversal' and 'loan return' in narration:
            return "loan&emirepayment"

        # icici personal loan format
        if re.search(
                r"^l[a-z]{3,6}xx[0-9]{3,6}(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|personal\W*loan|(abfl|hfcl)\W*personal",
                narration_proc):
            return "personalloan"

        if not (category.startswith('bounce') or category.startswith('charge') or category.startswith(
                'tax') or category.startswith('reversal')):
            if re.search(
                    r"creditwisecapital|wheelsemi|tvscredi|shriramtransport|bajajauto|tatamotorsfi|angelautofin|toyotafin|nissan\W*(?:ren.*)\W*fin",
                    narration_proc):
                return "autoloan"

            if re.search(r"health", narration_proc):
                category = "transferout"

            if (re.search(
                    r"billdesk(pay)?\.lic|paytmlic|bagichealth|lic(of)?india|carehealthins|lifeins|icicipru(dentia|dential)?lif|bhartiaxa|icicil(o)?m|bajaj(al|life)|birla\W*(sun|health)|futuregener(a)?li|swasthasuraksha|coverfoxinsu|(sbi|kotak|hsbc|hdfc)\W*(lf|life|gen)|starhealth|(max|axa)life|naviins|insuinter|hdfcerg|iffcoto|cholamandalammsgen|muthootinsurance|newindiaassurance|sundaramgeneral|godigit|magmahdi|nipponinsu|shriramgen|tata(.*)health|united(india)?ins|religarehealth|pradhanmantri|heroins|tata(aia|aig)|bajajfinservhea|(unique|payu)ins|mediclaim|kotaklifins|pmjjby|debittoins|exidelife|united(ind|india)ins|nationalins|policyba",
                    narration_proc) \
                or re.search(r"\besic\b|\bniacl\b|\buiic\b|\backo\b", narration)) and not re.search("birlasunlifemu",
                                                                                                    narration_proc):
                return "insurance"

            if re.search(
                    r"indinfhoufin|tatacap|lichfl|piramal(c|hfl)|(gic|aspire)(housing|home)fin|homecre|lichousing|icicihomefin|aavasfin|tatacapitalhou|axishome|hindujahous|capriglobalhous|indiabullshous|homeloan",
                    narration_proc) \
                    or re.search(r"\bdhfl\b", narration):
                return "homeloan"

            # add this if too necessary  ->  smallcap|largecap
            if re.search(
                    r"(true|rapid)tra|tradesma|choiceequity|groww|hillviewinvestments|sipdsptaxsaverfund|angel(bro|one|trade|ltd)|(tata|dsp|kotakmahindra|kotak|birla|idfc|sbi|hdfc|mirae)(mf|mut|asset|secu)|nsiceu|nippon|axis(longterm|smallcap|mf)|iciciprud|india(n)?(bulls|midcap|cle|infoline)|etmoney|5paisa|chit(s)?fund|cholamandalaminv|neobillionfin|mofsl|rksvsecu|coinswitch|paytmmoney|mutualf|dreamtrad|nobroker|(asset|wealth)manag|zerodha|(planetretail|maverick)hold|asthacred|indwealth|motilalos|pension|sharekhan|(profitmart|icici)secu|upstox|sbi(longterm|magnum|focused)|blueoceantrading|npstrust|stockoplex",
                    narration_proc) \
                    or re.search(r"\b(N|B)SE\b|\bCAMS\b", orig_narration) or re.search(
                r"\b(n|b)se\W*(limited|ltd)?\b|\bstocks\b|\b(e)?ppf(a)?|\bchit(s)?\b|rd\W*inst", narration):
                # print("inside 1")
                return "investmentexpense"

            if re.search(
                    r"camdento|esloan|naviloan|iiflfin|samastafin|landtfin|whizdm|tcf(p|s)l|fullerton|p2aloan|loanreturn|advancesal|smallborrow|krazybee|dmi(cro)?fin|truecredit|moneyview|bajajfi|adityabirlafin|cholamandalam|icicibankloan|(early|flex)sal|hindujah|liquiloans|drpfin|sundaramfi|apollofinvest|instamoney|dhaniloa|sicreva|loanret|navifin|cap(front|first)|zenlefin|karoloan|olafin|handloan|lazypay|goodskillsec|innofin|clixcap|payufin|bhawanaca|nirafin|adityabirlacapital|manappura|kreditbee|socialworthtech|zestmoney|shriramcity|fairmoney|bhanixfi|ingencofi|loantap|finnovat|loanemi|paisabazaar|spandanasphoorty",
                    narration_proc) or re.search(r"\bemi\b|\bcreditt\b", narration):
                return "loan&emirepayment"

    except:
        return category

    return category


def alcohol_bills_travel_wallet_debit_soft_logic(row):
    try:
        orig_narration, category = row.iloc[0], row.iloc[1]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")

        if re.search(r"cc\W*bill|rtncard", narration_proc):
            return "creditcardpayment"
        if re.search(r"\bcred\b", narration) and re.search(r"\bupi\b", narration) and category == "creditcardpayment":
            return "transferout"

        # add this    nfs\W*cw|^nda|(atm|chs)\W*(wdl|with|wdr|csw)
        if re.search(r"^NDA\b|^NFS|^ISS:|^ATD\b|CHS\W*WDL", orig_narration) or re.search(
                r"\bnfs\b|chs\W*wdl|nfs\W*cw|^nda|(atm|chs)\W*(wdl|with|wdr|csw|withdrawal)", narration):
            return "cashwithdrawal"

        if re.search(r"tatasky|tata\W*play|electri|dish\W*tv|\bd2h\b", narration_proc):
            return "bills&utilities"

        if re.search(r"barand|wine\W*shop|tasmac|wineandb(eer)?|liquor(s)?|alcohol(s)|madhuloka|floff|wines|slnwin",
                     narration_proc) or \
                re.search(r"\bimfl\b|\bwine(s)?\b|\bbeer\b|\bscotch\b|\bspiritz\b|\bbooz(e|ing)\b|\btoit\b|\bwine|wine\b|world\W*wine|wine\W*world", narration):
            return "alcohol"

        if category != 'cashwithdrawal':
            if re.search(
                    r"tour(s)?andtravel|fillingsta|^hpcl|fastag|(irc|ksr|tsr|gsr)tc|ixigo|redbus|aviation|makemytrip|ibibo|ticketbooking|fuel|^igl|^uber|(delhi|hyderabad|hyd|chennai|maharashtra|paytm)metro|metro(inapp|rail)|traintick|indianoil",
                    narration_proc) \
                    or re.search(
                r"\bnhpc\b|\bpetrol(eum)?\b|\bhpcl\b|^hpcl|fastag|\buber(rides)?\b|\bola(online)?\b|\biocl\b|\bhpcl\b|\bbpcl\b",
                narration):
                return "travel"

        narration_wallet = orig_narration.replace(' ', '').replace('-', '').replace('.', '').strip().lower()
        wallet_transfer_regex = re.search(
            r'paytmaddmone|addmoney@paytm|phonepewal|addmoneytowallet|addmoney|paytmwalletloading|paytmwallet|amazonpay@apl|payumoney@',
            narration_wallet)
        if wallet_transfer_regex or ('upi' in narration.lower() and 'wallet' in narration.lower()):
            return 'wallettransfer'
        if re.search(r"paypal", narration_proc):
            return "foreignwallet"

        if re.search(r"\bludo\b|ludo\W*sup|dream\W*1", narration):
            return "gaming"
    except:
        return category

    return category


def minbal_charge_debit_soft_logic(row):
    try:
        orig_narration, category, amount = row.iloc[0], row.iloc[1], row.iloc[2]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")

        narration_min_bal = re.sub(r"[:_/\-]", " ", narration)
        if (re.search(
                r"(\bamb\b|\bmab\b|\bqab\b|min(imum)?( )?avg( )?bal|avg( )?bal|min(imum)?( )?bal|bal( )?min|\bhab\b|avgbal|minavgbal|nmmab|nonmaint|\baqb\b).*(?=chgs|charges|chg|chrg|charge|fee|\bsc\b|\bsb\b)",
                narration_min_bal) \
            or re.search(
                    r"(chgs|charges|chg|chrg|charge|fee|\bsc\b|\bsb\b).*(?=\bamb\b|\bmab\b|\bqab\b|min(imum)?( )?avg( )?bal|avg( )?bal|min(imum)?( )?bal|bal( )?min|\bhab\b|avgbal|minavgbal|nmmab|nonmaint|\baqb\b)",
                    narration_min_bal) \
            or re.search(
                    r"minbal(sc|sb)|recovermab|(monthly|quartly)minavgbal|recover mab|non maintenance ch|mabchgs|min\W*balance",
                    narration_min_bal)) and \
                not ('gst @' in narration or 'gst on' in narration):
            return "belowminbalance"

        if not category.startswith('bounce'):
            if re.search(
                    r"inbcommission|tips/scg|tipssurcharge|^shortfalrec|basic_service_fee|card\W*(fee|amc)|fail.*(charge(s)?|chrg|\bchg\b|chq)",
                    narration):
                return "charges"

        if category == "tax":
            if re.search(r"fee(.*)gst", narration) or re.search(r"\+gst", narration):
                return "charges"

        if category == "cashwithdrawal" and amount > -100:
            return "charges"

    except:
        return category
    return category


def bounce_debit_soft_logic(row):
    try:
        orig_narration, category, amount = row.iloc[0], row.iloc[1], row.iloc[2]
        narration = orig_narration.lower()
        # print(category, orig_narration)

        if re.search(r"dr\W*thru\W*chq", narration):
            return "transferout"

        if (re.search(r"chq paid|ecs.*chq|\batm\b|\bmb\b|paytm", narration) or re.search(r"ATM",
                                                                                         orig_narration) or amount > -100) and category == 'bouncedo/wcheque':
            category = "transferout"

        if re.search(
                r"\bneft\b|\btrf\b|transfer( |-)(by|to)|imps|\binb\b|\bupi\b|\bcms\b|\btpt\b|\bmob\b|\bmapy\b|\bmbk\b|\bpos\b|\binf\b|fund transfer",
                narration.lower()) and category.__contains__('bounce'):
            category = "transferout"
        if re.search(
                r"(i/w|\binw\b|inward|inwd|\biw\b).*(chq|cheque).*(ret|rtn|return|reject)|(i/w|\binw\b|inward|inwd|\biw\b).*(ret|rtn|return|reject).*(chq|cheque)|dishonour\W*ch(e)?q|ch(e)?q\W*dishonour",
                narration):
            # print('inside 1')
            if amount > -1000:
                return "bouncedi/wchequecharges"
            else:
                return "transferout"

        if re.search(
                r"iw_rej_inst|(i/w|\binw\b|inward|inwd|\biw\b).*(reject|retn|rtn|return).*(charge(s)?|chrg|\bchg\b|chq)",
                narration) and not re.search(r"\bach\b|\becs\b", narration):
            # print('inside 2')
            return "bouncedi/wchequecharges"

        # print(1)

        # nach(dr)?( )?(retn|return|rtn)( )?(charge|chrg|chg|chgs)
        if re.search(
                r'^rtn( )?chg|si failure charge|bajajfinserv bounce chrg|ecs inward rejection charge|(nach|ach|ecs)(dr)?(.*)?(retn|return|rtn|ret)(.*)?(charge|chrg|chg|chgs)|cph achdr rtn chg|rtn chg hdbfin|ecs inw chq rej chrgs|ecs nachret insffnd|mandate fail|ach rtn|rtnchg|ecs return|bounce( )?chg|nach\W*fail\W*insuf\W*bal|(ach|ecs)\W*debit\W*insufficient\W*funds',
                narration):
            # print('inside 3')
            if amount < -1500:
                return "transferout"
            if not re.search(r'shortfal|shortfall', orig_narration.lower()):
                # print("inside 4")
                return "bouncedi/wecscharges"

        if re.search(r"(emi|nach|ach).*(rtn|return|ret).*(charge(s)?|chrg|\bchg\b|chgs)", narration):
            # print("inside correct")
            return "bouncedi/wecscharges"

        # print(2)

        if re.search(r"(o/w|outward|\bow\b|\bout\b).*(reject|retn|rtn|return|bounce)", narration) or \
                (re.search(
                    r"imagenotclear|^brnowrtnclg|^owrtn|owrtnclg|owrejinst|(fund).*(?=insuffici)|(insuffici).*(?=fund)",
                    narration.replace(' ', '')) and not re.search(r'\batm\b', narration)) or \
                re.search(r"gefu.*(chq|cheque).*(reject|retn|rtn|return)", narration):
            # print('inside 4')
            if re.search(r"i/w|\binw\b|inward|inwd|\biw\b", narration):
                return "transferout"
            elif amount > -1000:
                return "bouncedo/wchequecharges"
            else:
                return "bouncedo/wcheque"

        # print(3)

        if re.search(
                r"chq dishonour|ow_rej_inst|(o/w|outward|\bow\b|\bout\b).*(rej|reject|ret|rtn|return).*(charges|chrg|\bchg\b|chq)",
                narration) or \
                (re.search(
                    r"(o/w|outward|\bow\b|\bout\b).*(chq|cheque).*(rej|reject|ret|rtn|return)|rtn.*chq.*(charges|chrg|\bchg\b|chq)|out.clg.rtn",
                    narration) and amount > -1000):
            # print('inside 5')
            return "bouncedo/wchequecharges"

        # if re.search(r"nach fail insuf bal", narration):
        #     return "charges"

    except:
        return category
    return category


def loan_investment_insurance_credit_soft_logic(row):
    try:
        orig_narration, category = row.iloc[0], row.iloc[1]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")

        if not (category.startswith('bounce') or category == 'salary' or category == 'reversal'):
            if re.search(r"health", narration_proc):
                category = "transferin"

            if re.search(r"reliancenipponlife|maxlife|lifeinsu|licofind|aicofind|(sbi|kotak|hsbc|hdfc)\W*(lf|life|gen)",
                         narration_proc) or re.search(r'\bAIC\b', orig_narration):
                return "insurance"

            if re.search(
                    r"(true|rapid)tra|tradesma|(tata|dsp|kotakmahindra|kotak|birla|idfc|sbi|hdfc|mirae)(mf|mut|asset|secu)|angel(bro|one|trade|ltd)|clearingcorp|sharekhan|findiv|sharesandholding|redemption|dividend|sharemarket|maturityclaim|paragparikh|rksvsecu|sweep(from|dep)|pension|kuberinvest|axismut|nippon|rdcrea|zerodha|nextbil|visagehold|absolutefin|fortunecap|fdpremat|mutualfu|choiceequity|(rd|fd)clo|(fixed|flexi)dep|revsweep|arnoldhol|coimbatorecap|epfpens|alicebluefin|cholamandalaminvest|finvasiasecur|finaldiv|paytmmoney|indmoney|hdfcsecu|miraeasset|icicipru|5paisa|subsidy|bypen|infoline|asthacred",
                    narration_proc) \
                    or re.search(r"\b(N|B)SE\b|\bCAMS\b|\bEPF(O)?\b", orig_narration) or re.search(
                r"\bstocks\b|\b(e)?ppf(a)?|\bchit(s)?\b|\bf&o\b|\bFD\b|\bRD\b|brn-flexi|int\W*div|divdnd|dividend|fnldiv|int\W*spl\W*div|(div2|fnl|final)[0-9]", narration):
                return "investmentincome"

            if re.search(
                    r"camdento|myloancare|kavachfin|personalloan|esloan|samastafin|naviloan|landtfin|ucafin|tatacap|piramalc|mahindrarural|advancesal|trillionloan|fullerto|shikshafin|northernarccap|bssmicrofi|homeloan|loan(re)?pay|creditwisecapital|lichousing|wheelsemi|tvscredi|shriramtransport|bajajauto|tatamotorsfi|angelautofin|tcf(p|s)l|fullerton|p2aloan|smallborrow|krazybee|beekredit|dmi(cor)?fin|truecre|money(view|tap)|bajaj(fin|hou)|adityabirlafi|cholamandalam|icicibankloan|(early|flex)sal|hindujah|liquiloans|sundaramfin|drpfin|apollofin|instamoney|dhaniloa|sicreva|loanret|navifin|cap(front|first)|zenlefin|karoloan|olafin|handloan|lazypay|goodskillsec|innofin|clixca|payufin|bhawanaca|nirafin|adityabirlacapital|manappura|kreditbe|socialworthtech|zestmoney|shriramcity|fairmoney|bhanixfi|ingencofi|loantap|finnovat|loanemi|paisabazaar|mpokket|muthoot(micro|gold)|muthootf|kissht|aavasfin|bussanautofi|finnabl|capitaltru|paymeind|earlysal|mfinance|akaraca|pocketly|vivifi|tatacapit|goldlinefin",
                    narration_proc) \
                    or re.search(
                r"\bloan(s)?\b|\bemi(s)?\b|\bdhfl\b|\bincred\b|\bcreditt\b|\blend(ing)?(s)?\b|\biifl\b|\bstpl\b",
                narration):
                return "loandisbursed"

            if orig_narration.startswith("NACH") and category != 'loandisbursed':
                return "investmentincome"
    except:
        return category

    return category


def reversal_cashdeposit_rewards_tax_credit_soft_logic(row):
    try:
        orig_narration, category = row.iloc[0], row.iloc[1]
        narration = orig_narration.lower()
        narration_proc = narration.replace(" ", "")

        if re.search(r"gstadjtran|(tax|gst|tds).*(?=refund|rfnd|return)", narration_proc) or re.search(
                r"AY2022(-| )?23|AY2021(-| )?22|AY2023(-| )?24|\bTDS\b", orig_narration):
            return "tax"

        if re.search(r"instantpay|bundltech", narration_proc):
            return "transferin"

        if (re.search(r"refun|failed|retur|\brev\b|revers|\brvsl\b|\bret\b|\brevr\b", narration) and re.search(
                r"\bpos\b|charge|\bupi\b|^atd|^atm|^upi|\becom\b|\bimps\b|\bvisa\b|\bneft\b", narration)) or \
                (re.search(
                    r"\bpos ref\b|\brev_insta\b|^ref\b|\biconn ref\b|\bips ref\b|\brev( )?merv\b|upiret|visa ref|upi_ret|credit\,tips surcharge|\btrrr\b|^ref\b|^rev\b|tipssurc|atm-cwrr|upi/rvsl",
                    narration)):
            return "reversal"
        if category == 'reversal' and re.search(r"upi/rev", narration_proc) and not re.search(
                r"upi/rev\b|upi/rvsl|upi/reversal", narration_proc):
            return "transferin"

        # some of the narrations with cash / deposit in them are coming as cashdeposit, so removing upi|neft|nft txns to handle these false +ves
        if re.search(r"\bUPI\b|\bRTGS\b|\bIMPS\b|\bNEFT\b|\b(I)?NFT\b|\bCLG\b|\bCHQ\b|\bCHEQUE\b|\bINB\b",
                     orig_narration) and category == 'cashdeposit':
            return "transferin"
        if (re.search(r"^NFS|\bCDM\b|^([- ])*(CDM|CDS)|^ATM\b|^BNA\b|^CASH DEP|CHS\W*DEP|CARDLESS\W*DEP",
                      orig_narration) or re.search(r'cashdep',
                                                   narration_proc)) and category != 'reversal' and not re.search(
                r"\bUPI\b|\bRTGS\b|\bIMPS\b|\bNEFT\b|\b(I)?NFT\b|\bCLG\b|\bCHQ\b|\bCHEQUE\b", orig_narration):
            return "cashdeposit"

        if re.search(r"interest|intere|intrest|intcoll|exgratia", narration_proc):
            return "interest"

        if category != 'salary' and (
                re.search(r"reward|reimb|remmitance|expclaim|incentive|allowanc|cashback|reimburs|expens",
                          narration_proc) or re.search(r"\breim(b)?(s)?\b|\bbonus\b", narration)):
            return "rewards&allowances"

        if category == 'bouncedi/wecs' and re.search(r"^UPI\b|^NEFT\b|^RTG\b|^IMPS\b", orig_narration):
            return "transferin"

    except:
        return category

    return category


def bounce_credit_soft_logic(row):
    try:
        narration, category, amount, balance = row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3]
        # narration = orig_narration.lower()
        # narration_proc = narration.replace(" ", "")

        # handling bounced i/w ecs  false +ves
        if re.search(r"\bach\b", narration, flags=re.I) and not re.search(r"^ach d", narration, flags=re.I) \
            and not re.search(r"reject|retn|\brtn\b|\bret\b|return|bounce|inward|\binw\b|i/w", narration.lower()) and category=="bouncedi/wecs":
            category = "transferin"
            category = loan_investment_insurance_credit_soft_logic(pd.Series({'narration':narration, 'category':category}))
            if category=="loandisbursed" and amount<500:
                category = "investmentincome"

        # handling bounced i/w cheque  false +ves
        if category=="bouncedi/wcheque" and balance>amount and not re.search(r"reject|retn|\brtn\b|\bret\b|return|bounce|inward|\binw\b|i/w|chq\W*ret|\brej\b|signature|emi.*[0-9]*chq|over\W*due\W*loan", narration.lower()):
            category = "transferin"

        # handling bounced  false  +ves
        if re.search(
                r"\bneft\b|\btrf\b|transfer( |-)(by|to)|imps|\binb\b|\bupi\b|\bcms\b|\btpt\b|\bmob\b|\bmapy\b|\bmbk\b|\bpos\b|\binf\b|fund transfer",
                narration.lower()) and category.__contains__('bounce'):
            category = "transferin"

        if re.search(r"CHQ DEP", narration) and category.__contains__('bounce'):
            return "transferin"


        if re.search(r"IMPS REJECT", narration):
            category = "bouncedi/wpayment"

        if re.search(r"\bNEFT\b|\bUPI|UPI\b|\bIMPS\b", narration) and category.startswith('bounce'):
            if re.search('reject|return|\brtn\b', narration.lower()) and not re.search(r"retail", narration.lower()):
                category = "bouncedi/wpayment"
            else:
                return "transferin"

        if re.search("no(?:.*)funds(?:.*)available|dr(?:.*)not(?:.*)allowed", narration, flags=re.I) and re.search(r"\becs\b|\bnach\b|\bach\b", narration.lower()):
            return "bouncedi/wecs"
        if re.search(r"^ACH\W*D", narration):
            return "bouncedi/wecs"
        if narration.startswith('CC') and re.findall(r'CC\d+', narration.replace(' ', '')):
            return "bouncedi/wecs"
        if re.findall(r'BAJAJFINEMIBF\d+', narration.replace(' ', '').replace('-', '')):
            return "bouncedi/wecs"
        if narration.startswith('HDB') and narration.__contains__('EMI'):
            return "bouncedi/wecs"
        if (narration.__contains__('CHEQUE') and re.findall(r'RETURN', narration)) or (
                narration.__contains__('I/W') and narration.__contains__('CHEQUE') and narration.__contains__('RET')):
            return "bouncedi/wcheque"
        if re.findall(r'EMI\d+CHEQUE', narration.replace(' ', '')) and narration.startswith('EMI'):
            return "bouncedi/wcheque"

        if narration.startswith('I/W CHEQUE RTN'):
            return "bouncedi/wcheque"
        if narration.startswith('RETURNED') and narration.__contains__('INSUFFICIENT'):
            return "bouncedi/wcheque"

        if narration.replace(' ', '').__contains__('BYCLG(REJ)'):
            return "bouncedi/wcheque"
        if narration.replace(' ', '').__contains__('I/WCHEQUERET'):
            return "bouncedi/wcheque"
        if narration.__contains__('CLG') and narration.__contains__('REJ'):
            return "bouncedi/wcheque"
        if narration.replace(' ', '').__contains__('ECSDRRTN') or narration.replace(' ', '').__contains__(
                'ACHLDRRTN') or narration.replace(' ', '').__contains__('ACH DR RTN'):
            return "bouncedi/wecs"

        if narration.__contains__('I/W') and narration.__contains__('CHEQUE') and narration.__contains__('RETURN'):
            return "bouncedi/wcheque"
        if (narration.replace(' ', '').__contains__('TOCLG(REJ)')) or (
                narration.replace(' ', '').__contains__('CLEARING(REJ)')):
            return "bouncedi/wcheque"
        if narration.startswith("BY RET") and narration.__contains__("DIFFE"):
            return "bouncedi/wcheque"

        if narration.replace(' ', '').replace('.', '').__contains__('ECSRET') or narration.replace(' ', '').replace('.',
                                                                                                                    '').__contains__(
                'ECSRTN'):
            return "bouncedi/wecs"
        if narration.replace('.', '').__contains__('CHEQUE') and narration.__contains__('RETURN'):
            return "bouncedi/wcheque"
        if narration.replace('.', '').__contains__('CHEQUE') and narration.__contains__('RTN'):
            return "bouncedi/wcheque"

        if narration.startswith('RETURNED') and re.findall(r'RETURNED:\d+:', narration) or (
                narration.__contains__('RETURNED') and (
                narration.__contains__('INSUFFICIENT') or narration.__contains__('SIGNATURE'))):
            return "bouncedi/wcheque"

        if narration.startswith('RETURNED') and re.findall(r'RETURNED:\d+:', narration) or (
                narration.__contains__('RETURNED') and (
                narration.__contains__('INSUFFICIENT') or narration.__contains__('SIGNATURE'))):
            return "bouncedi/wcheque"

        if narration.replace(' ', '').replace('(', '').replace(')', '').__contains__('CLGREJ'):
            return "bouncedi/wcheque"
        if narration.__contains__('CHEQUE') and narration.__contains__('RETURN'):
            return "bouncedi/wcheque"

        # print('here1')

        if narration.replace(' ', '').replace('/', '').__contains__('NACHDRIW'):
            return "bouncedi/wecs"
        if narration.__contains__('INWARD') and narration.__contains__('CHEQUE') and (
                narration.__contains__('RETURN') or narration.__contains__('RTN') or narration.__contains__('RETN')):
            return "bouncedi/wcheque"
        if narration.__contains__('CHEQUE') and narration.__contains__('RTN'):
            return "bouncedi/wcheque"
        if narration.__contains__('TFCQ') and narration.__contains__('RTN'):
            return "bouncedi/wcheque"

        if narration.__contains__('CHEQUE') and narration.__contains__('RETURN'):
            return "bouncedi/wcheque"
        if narration.replace(' ', '').replace('/', '').__contains__('IWCHEQUERTN'):
            return "bouncedi/wcheque"
        if narration.__contains__('ECS') and narration.__contains__('RETURN') and not narration.replace(' ',
                                                                                                        '').__contains__(
                'REVOFECSRETURNCHGS'):
            return "bouncedi/wecs"

        # print('here2')

        if narration.replace(' ', '').__contains__('CHEQUEISSUEDBOUNCE'):
            return "bouncedi/wcheque"

        if narration.startswith('RETURNED') and re.findall(r'RETURNED:\d+:', narration.replace(' ', '')):
            return "bouncedi/wcheque"

        if narration.replace(' ', '').__contains__('ECSCLG(REJ)') or narration.replace(' ', '').__contains__(
                'CLG(REJ):ECS'):
            return "bouncedi/wecs"
        if re.findall(r'ECSBFL:\d+', narration):
            return "bouncedi/wecs"
        if narration.replace(' ', '').__contains__('CLG(REJ)') or narration.replace(' ', '').__contains__(
                'CLEARING(REJ)'):
            return "bouncedi/wcheque"

        if narration.replace(' ', '').__contains__('INWARDCHEQUECLGRTRN'):
            return "bouncedi/wcheque"

        if narration.__contains__('ACH DR'):
            return "bouncedi/wecs"

        # print('here3')

        if narration.replace(' ', '').__contains__('IWCHEQUERETURN') or re.findall(r'RETURNED:\d+:', narration):
            return "bouncedi/wcheque"

        if re.search(r"cln.*ecs.*bounce.*pmt", narration.lower()):
            return "bouncedi/wecs"

        if category == "bouncedi/wpayment":
            category = 'reversal'

    except:
        return category

    return category


def salary_credit_soft_logic(row):
    try:
        orig_narration, category, amount = row.iloc[0], row.iloc[1], row.iloc[2]
        narration = orig_narration.lower()
        narration_proc = re.sub(r'\d+', ' ', narration.lower())
        is_salary = False

        if (re.search(r"reward|reimb|remmitance|expclaim|incentive|allowanc|cashback|reimburs|expens|rebate|indemni|compens|commision|conveyan", narration_proc) \
                or re.search(r"\breim(b)?(s)?\b|\bbonus|bonus\b", narration)):
            return "rewards&allowances"

        if re.search(r"\bupi\b|\bupi|upi\b|\bsalam\b|\bsaleesm\b|\bsalim\b|\bfaisal\b",
                     narration_proc) and category.lower() == 'salary':
            return "transferin"
        if re.search(r"flexsal|earlysal", narration_proc):
            return "loandisbursed"
        if re.search(
                r"\becs\b|fiduciary|incentive|early|\brev\b|reversal|salarpur|cash dep|return|\bemi\b|\bstock\b|flexsalary",
                narration_proc) or re.search(r'earlysal', narration_proc.replace(' ', '')):
            return category

        if (amount > 3000) and (not re.search(r"\bupi\b|\bupi|upi\b", narration_proc)):
            if re.search(r'\bslc\b|\bslry\b|wage(s)?\b|\bsal_|pay( )?rol|\bemplid', narration_proc) \
                    or re.search(r's(a)?al(l)?(a|e)?(i)?r(y|ie)|netsal|saltrf|_sal_|stipend',
                                 narration_proc.replace(' ', '')) \
                    or re.search(
                r'([_]?(s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?)[_ ]?)(\W*)(of|for|from|given|paid|to)?(\W*)(?=jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)',
                narration_proc) \
                    or re.search(
                r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)(\W*)(of|for|from|given|paid|to)?(\W*)(?=[ _]?(s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?)[_]?)',
                narration_proc) \
                    or re.search(
                r'(january|february|march|april|may|june|july|august|september|october|november|december)(.*)(?=[ _]?(s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?)[_]?)',
                narration_proc) \
                    or re.search(
                r'([ _]?(s(a)?al(l)?(a|e)?(i)?(r)?(y|ie)?)[_]?)(.*)(?=january|february|march|april|may|june|july|august|september|october|november|december)',
                narration_proc) \
                    or re.search(r'2020 net pay|2019 net pay|2021 net pay|2022 net pay', narration):  # \
                # or re.search(r"sal\b", narration_proc) and re.search('bulkpost', narration_proc.replace(' ', '')):
                is_salary = "salary"

            # sal_month = re.findall(r"(?:\bjanuary|\bjan|\bfebruary|\bfeb|\bmarch|\bmar|\bapril|\bmay|\bjune|\bjuly|\baugust|\bseptember|\bsep|\boctober|\boct|\bnovember|\bnov|\bdecember|\bdec)( )?(\d{2,4})\b",narration.lower())
            # if sal_month:
            #     is_salary = True
    except:
        return category

    return 'salary' if is_salary else category