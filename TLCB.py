# -*- coding:utf-8 -*- 
# 
# 
# 

import datetime
import json
import time
import time as tm

import requests
from scrapy.selector import Selector

from QuotationDict import QuotationDict


class TLCB:
    CurrencyNameList = ['826', '978', '840', '392', '344']
    CurrencyCodeList = ['GBP', 'EUR', 'USD', 'JPY', 'HKD']

    SleepTime = -1
    EndRow = 64

    def __init__(self):
        self.SleepTime = -1

    def setSleepTime(self, sleeptime):
        if sleeptime != '':
            self.SleepTime = sleeptime
            print("已按照默认设置刷新(120s)\n")
        else:
            self.SleepTime = -1

    def QuotationFlow(self, QuotationList):
        while True:
            a = self.getQuotation()
            QuotationList += a

            print(self.SleepTime)
            time.sleep(self.SleepTime)

    def getQuotation(self):
        error_times = 0
        try:
            r = requests.post('https://ebank.zjtlcb.com/perbank/PB0000_currencyRate.do',
                              data={'trxCode': 'PB0000', 'tranFlag': '1', 'format': 'JSON', 'srcChannel': 'WEB'})
            r.encoding = "utf-8"
        except:
            print("Internet Error, waiting 2s.\n")
            error_times += 1
            tm.sleep(2)
            while error_times <= 3:
                r = requests.post('https://ebank.zjtlcb.com/perbank/PB0000_currencyRate.do',
                                  data={'trxCode': 'PB0000', 'tranFlag': '1', 'format': 'JSON', 'srcChannel': 'WEB'})
            else:
                print("Retry 3 times, break!")
                exit()

        html = r.text
        text = json.loads(html)

        QuotationList = []

        for row in text['cd']['exchangeRateList']:
            try:
                if 'currencyType' in row and 'buyPrice' in row and 'selPrice' in row and 'midPrice' in row \
                        and 'cashBuyPrice' in row and 'cashSellPrice' in row and 'disRate' in row and 'valDate' in row \
                        and 'valTime' in row:

                    # QuotationDict = {'BankName', 'CurrencyName', 'TimeStamp', 'SE_Bid', 'SE_Ask', 'BN_Bid', 'BN_Ask'}
                    QuotationDictTmp = QuotationDict()
                    QuotationDictTmp.BankName = 'TLCB'
                    QuotationDictTmp.CurrencyCode = self.CurrencyCodeList[
                        self.CurrencyNameList.index(row['currencyType'])]
                    QuotationDictTmp.TimeStamp = datetime.datetime.strptime(
                        row['valDate'] + '_' + row['valTime'], "%Y-%m-%d_%H:%M:%S")
                    QuotationDictTmp.SE_Bid = row['buyPrice']
                    QuotationDictTmp.SE_Ask = row['selPrice']
                    QuotationDictTmp.BN_Bid = row['cashBuyPrice']
                    QuotationDictTmp.BN_Ask = row['cashSellPrice']
                    QuotationDictTmp.CurrencyUnit = 100

                    QuotationList.append(QuotationDictTmp)
                else:
                    print('table fault')
                    exit()

            except IndexError:

                break
        print('TLCB Spider RownNum_' + str(len(text['cd']['exchangeRateList'])) + ' is endness.')
        return QuotationList
