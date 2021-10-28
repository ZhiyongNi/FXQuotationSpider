﻿# -*- coding:utf-8 -*- 
# 
# 
# 

import getopt
import sys
import time
import time as tm
import os
import requests

from scrapy.selector import Selector
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tqdm import tqdm
import datetime
import re

from ABCI import ABCI
from BCHO import BCHO
from CCBH import CCBH
from ICBC import ICBC
from NBCB import NBCB
from QuotationDB import QuotationDB
from TLCB import TLCB


class FXQuotationSpider:
    QuotationList = []

    # QuotationList.extend(BCHOInstance.getQuotation())
    # QuotationList.extend(NBCBInstance.getQuotation())
    def QuotationSpiderCommand(self, command):
        if command == 'start':
            BCHOInstance = BCHO()
            BCHOInstance.setSleepTime(5)

            NBCBInstance = NBCB()
            NBCBInstance.setSleepTime(5)

            ICBCInstance = ICBC()
            ICBCInstance.setSleepTime(5)

            CCBHInstance = CCBH()
            CCBHInstance.setSleepTime(5)

            ABCIInstance = ABCI()
            ABCIInstance.setSleepTime(5)

            TLCBInstance = TLCB()
            TLCBInstance.setSleepTime(5)

            with ThreadPoolExecutor(max_workers=8) as TPool:  # 创建一个最大容纳数量为5的线程池
                print('FXQuotationSpider beginning.')

                while True:
                    self.QuotationList = []

                    BCHOFuture = TPool.submit(BCHOInstance.getQuotation)
                    ICBCFuture = TPool.submit(ICBCInstance.getQuotation)
                    ABCIFuture = TPool.submit(ABCIInstance.getQuotation)
                    CCBHFuture = TPool.submit(CCBHInstance.getQuotation)
                    NBCBFuture = TPool.submit(NBCBInstance.getQuotation)
                    TLCBFuture = TPool.submit(TLCBInstance.getQuotation)

                    self.QuotationList += BCHOFuture.result()
                    self.QuotationList += ICBCFuture.result()
                    self.QuotationList += ABCIFuture.result()
                    self.QuotationList += CCBHFuture.result()
                    self.QuotationList += NBCBFuture.result()
                    self.QuotationList += TLCBFuture.result()

                    QuotationDB.addQuotationtoDB(self.QuotationList)

                    SE_BidDict = {}
                    CurrencyUnit = {}
                    spread = {}
                    for QuotationDictCell in self.QuotationList:
                        try:
                            if QuotationDictCell.CurrencyCode == 'USD':
                                SE_BidDict[QuotationDictCell.BankName] = QuotationDictCell.SE_Bid
                                CurrencyUnit[QuotationDictCell.BankName] = QuotationDictCell.CurrencyUnit
                            else:
                                pass
                        except:
                            break

                    print(datetime.datetime.now())
                    print('中国银行美元结汇价格：' + SE_BidDict.get('BCHO') + '；')
                    spread['BCHO'] = round(float(SE_BidDict.get('TLCB')) * 100 - float(SE_BidDict.get('BCHO')) * 100)
                    print('中国工商银行美元结汇价格：' + SE_BidDict.get('ICBC') + '；')
                    spread['ICBC'] = round(float(SE_BidDict.get('TLCB')) * 100 - float(SE_BidDict.get('ICBC')) * 100)
                    print('中国建设银行美元结汇价格：' + SE_BidDict.get('CCBH') + '；')
                    spread['CCBH'] = round(float(SE_BidDict.get('TLCB')) * 10000 / CurrencyUnit['TLCB'] - float(
                        SE_BidDict.get('CCBH')) * 10000 / CurrencyUnit['CCBH'])
                    print('中国农业银行美元结汇价格：' + SE_BidDict.get('ABCI') + '；')
                    spread['ABCI'] = round(float(SE_BidDict.get('TLCB')) * 10000 / CurrencyUnit['TLCB'] - float(
                        SE_BidDict.get('ABCI')) * 10000 / CurrencyUnit['ABCI'])
                    print('宁波银行美元结汇价格：' + SE_BidDict.get('NBCB') + '；')
                    spread['NBCB'] = round(float(SE_BidDict.get('TLCB')) * 100 - float(SE_BidDict.get('NBCB')) * 100)
                    print('泰隆银行美元结汇价格：' + SE_BidDict.get('TLCB') + '；泰隆银行价格比中国银行好：' + str(
                        spread['BCHO']) + 'pips；泰隆银行价格比中国工商银行好：' + str(
                        spread['ICBC']) + 'pips；泰隆银行价格比中国建设银行好：' + str(
                        spread['CCBH']) + 'pips；泰隆银行价格比中国农业银行好：' + str(
                        spread['ABCI']) + 'pips；泰隆银行价格比宁波银行好：' + str(
                        spread['NBCB']) + 'pips。')

                    time.sleep(30)

                    ##print('BCHO added')
                    ##print(self.QuotationList)
                    ##self.QuotationList += NBCBFuture.result()
                    ##print('NBCB added')
                    ##print(self.QuotationList)

                    # for future in futures:

                    # print('start')

                    # print(BCHOTask.result())

                    # print(f"task1: {BCHOTask.done()}")  # 通过done来判断线程是否完成

                    # NBCBTask = ex.submit(NBCBInstance.getQuotation())  # 通过submit提交执行的函数到线程池中

                    # print(f"task2: {BCHOTask.done()}")

                    ##BCHOInstance.setSleepTime(15)
                    ##print(BCHOInstance.getQuotation())

                    ##for element in BCHOInstance.getQuotation():

                    # time.sleep(5)

                    # for page in range(1, (pages + 1)):
                    #    all_task.append(ex.submit(page_get, output, sort, FX_or, erectDate, nothing, FX, i, page, 22))

                    # [i.result() for i in show_prog(all_task, ifbar=bar)]
                    # ex.shutdown(wait=True)
                    # output = list(set(output))
                    # output.sort(reverse=True, key=lambda ele: ele[-1])
                    # filename = '[' + '+'.join(FX_or) + ']' + '+'.join(output[0][1:-1]) + '_' + erectDate + '_' + nothing
                    # else:
                    # ex = ThreadPoolExecutor(max_workers=20)
                    # all_task = [ex.submit(page_get, output, sort, FX_or, '', '', FXC, i, '1', 3) for i in range(len(FX))]
                    # [i.result() for i in show_prog(all_task, ifbar=bar)]
                    # ex.shutdown(wait=True)

                    # def bocfxnew(FX=0, sort=0, time=-1, plot=0, csv=0, pt=0, op='~/bocfx_output', bar=0):
