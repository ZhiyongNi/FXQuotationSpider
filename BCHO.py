# -*- coding:utf-8 -*- 
# 
# 
# 

import datetime
import os
import re
import time as tm
from concurrent.futures import ThreadPoolExecutor

import requests
from bocfx import show_prog, page_get
from scrapy.selector import Selector
from tqdm import tqdm


class BCHO:
    outputmes = ''

    CurrencyName = ['英镑', '欧元', '美元', '日元', '港币', '加拿大元', '澳大利亚元']
    CurrencyCode = ['GBP', 'EUR', 'USD', 'JPY', 'HKD', 'CAD', 'AUD']
    SleepTime = -1

    def __init__(self):

        self.outputmes = ''

    def setSleepTime(sleeptime):
        try:
            sleeptime = input("多久刷新一次(s): ")
            if sleeptime == '':
                sleeptime = 120
                print("已按照默认设置刷新(120s)\n")
            else:
                sleeptime = int(sleeptime)
        except:
            print("输入有误,请重新输入.\n")

    def getQuotation(self):
        error_times = 0
        try:
            r = requests.get('https://www.boc.cn/sourcedb/whpj/')
            r.encoding = "utf-8"
            print(r.text)
        except:
            print("Internet Error, waiting 2s.\n")
            error_times += 1
            tm.sleep(2)
            while error_times <= 3:
                r = requests.post('https://srh.bankofchina.com/search/whpj/search_cn.jsp',
                                  data={'erectDate': erectDate, 'nothing': nothing, 'pjname': str(FX[i]),
                                        'page': str(page)})
            else:
                print("Retry 3 times, break!")
                exit()

        html = r.text

        for row in range(2, end):
            try:
                SE_B = Selector(text=html).xpath('//tr[%i]/td[2]/text()' % (row)).extract()[0]
                BN_B = Selector(text=html).xpath('//tr[%i]/td[3]/text()' % (row)).extract()[0]
                SE_A = Selector(text=html).xpath('//tr[%i]/td[4]/text()' % (row)).extract()[0]
                BN_A = Selector(text=html).xpath('//tr[%i]/td[5]/text()' % (row)).extract()[0]
                time = Selector(text=html).xpath('//tr[%i]/td[7]/text()' % (row)).extract()[0].replace('.', '-')
                output.append(eval(sort))

            except IndexError:
                break
        return self.outputmes
