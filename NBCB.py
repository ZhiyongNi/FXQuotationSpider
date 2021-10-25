# -*- coding:utf-8 -*- 
# 
# 
# 

import datetime
import os
import re
import time
import time as tm
from concurrent.futures import ThreadPoolExecutor

import requests
from bocfx import show_prog, page_get
from scrapy.selector import Selector
from tqdm import tqdm

from QuotationDict import QuotationDict


class NBCB:
    CurrencyNameList = ['英镑', '欧元', '美元', '日元', '港币', '加拿大元', '澳大利亚元']
    CurrencyCodeList = ['GBP', 'EUR', 'USD', 'JPY', 'HKD', 'CAD', 'AUD']

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
            r = requests.get('https://mybank.nbcb.com.cn/doorbank/cms_exchangeRate.do')
            r.encoding = "utf-8"
        except:
            print("Internet Error, waiting 2s.\n")
            error_times += 1
            tm.sleep(2)
            while error_times <= 3:
                r = requests.get('https://mybank.nbcb.com.cn/doorbank/cms_exchangeRate.do')
            else:
                print("Retry 3 times, break!")
                exit()

        html = r.text
        QuotationList = []

        DateTmp = Selector(text=html).xpath('//input[@id="queryDate"]/@value').extract()[0]
        TimeTmp = Selector(text=html).xpath('//input[@id="queryTimeText"]/@value').extract()[0]
        for row in range(1, self.EndRow):
            try:
                if row == 1 and Selector(text=html).xpath('//tr[%i]/th[1]/text()' % (row)).extract()[0] != '交易币' and \
                        Selector(text=html).xpath('//tr[%i]/th[2]/text()' % (row)).extract()[0] != '交易币单位' and \
                        Selector(text=html).xpath('//tr[%i]/th[3]/text()' % (row)).extract()[0] != '基本币' and \
                        Selector(text=html).xpath('//tr[%i]/th[4]/text()' % (row)).extract()[0] != '中间价' and \
                        Selector(text=html).xpath('//tr[%i]/th[5]/text()' % (row)).extract()[0] != '卖出价' and \
                        Selector(text=html).xpath('//tr[%i]/th[6]/text()' % (row)).extract()[0] != '现汇买入价' and \
                        Selector(text=html).xpath('//tr[%i]/th[7]/text()' % (row)).extract()[0] != '现钞买入价':
                    print('table fault')
                    exit()
                elif Selector(text=html).xpath('//tr[%i]/td[1]/text()' % (row)).extract()[0] in self.CurrencyNameList \
                        and Selector(text=html).xpath('//tr[%i]/td[3]/text()' % (row)).extract()[0] == '人民币':
                    CurrencyName = Selector(text=html).xpath('//tr[%i]/td[1]/text()' % (row)).extract()[0]
                    CurrencyUnit = Selector(text=html).xpath('//tr[%i]/td[2]/text()' % (row)).extract()[0]
                    SE_Ask = Selector(text=html).xpath('//tr[%i]/td[5]/text()' % (row)).extract()[0]
                    BN_Ask = Selector(text=html).xpath('//tr[%i]/td[5]/text()' % (row)).extract()[0]
                    SE_Bid = Selector(text=html).xpath('//tr[%i]/td[6]/text()' % (row)).extract()[0]
                    BN_Bid = Selector(text=html).xpath('//tr[%i]/td[7]/text()' % (row)).extract()[0]
                    TimeStamp = datetime.datetime.strptime(DateTmp + '_' + TimeTmp, "%Y%m%d_%H%M%S")

                    # QuotationDict = {'BankName', 'CurrencyName', 'TimeStamp', 'SE_Bid', 'SE_Ask', 'BN_Bid', 'BN_Ask'}
                    QuotationDictTmp = QuotationDict()
                    QuotationDictTmp.BankName = 'NBCB'
                    QuotationDictTmp.CurrencyCode = self.CurrencyCodeList[self.CurrencyNameList.index(CurrencyName)]
                    QuotationDictTmp.TimeStamp = TimeStamp
                    QuotationDictTmp.SE_Bid = SE_Bid
                    QuotationDictTmp.SE_Ask = SE_Ask
                    QuotationDictTmp.BN_Bid = BN_Bid
                    QuotationDictTmp.BN_Ask = BN_Ask
                    QuotationDictTmp.CurrencyUnit = CurrencyUnit

                    QuotationList.append(QuotationDictTmp)
                else:
                    CurrencyName = Selector(text=html).xpath('//tr[%i]/td[1]/text()' % (row)).extract()[0]

            except IndexError:
                print('NBCB Spider RownNum_' + str(row) + ' is endness.')
                break
        return QuotationList
