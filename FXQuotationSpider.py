# -*- coding:utf-8 -*- 
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

from BCHO import BCHO
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

            TLCBInstance = TLCB()
            TLCBInstance.setSleepTime(5)

            with ThreadPoolExecutor(max_workers=8) as TPool:  # 创建一个最大容纳数量为5的线程池

                BCHOFuture = TPool.submit(BCHOInstance.getQuotation)
                NBCBFuture = TPool.submit(NBCBInstance.getQuotation)
                TLCBFuture = TPool.submit(TLCBInstance.getQuotation)

                print('beginning')

                self.QuotationList += BCHOFuture.result()
                self.QuotationList += NBCBFuture.result()
                self.QuotationList += TLCBFuture.result()

                ##QuotationDB.addQuotationtoDB(self.QuotationList)

                while True:
                    self.QuotationList = []

                    BCHOFuture = TPool.submit(BCHOInstance.getQuotation)
                    NBCBFuture = TPool.submit(NBCBInstance.getQuotation)
                    TLCBFuture = TPool.submit(TLCBInstance.getQuotation)

                    self.QuotationList += BCHOFuture.result()
                    self.QuotationList += NBCBFuture.result()
                    self.QuotationList += TLCBFuture.result()

                    BCHO_SE_Bid = 0
                    TLCB_SE_Bid = 0
                    for QuotationDictCell in self.QuotationList:
                        try:
                            if QuotationDictCell.BankName == 'BCHO' and QuotationDictCell.CurrencyCode == 'USD':
                                BCHO_SE_Bid = QuotationDictCell.SE_Bid
                            elif QuotationDictCell.BankName == 'TLCB' and QuotationDictCell.CurrencyCode == 'USD':
                                TLCB_SE_Bid = QuotationDictCell.SE_Bid
                            else:
                                pass
                        except:
                            break
                    spread = round((float(TLCB_SE_Bid) - float(BCHO_SE_Bid)) * 100)
                    print(datetime.datetime.now())
                    print('中国银行美元结汇价格：' + BCHO_SE_Bid + '；泰隆银行美元结汇价格：' + TLCB_SE_Bid + '；泰隆银行价格好：' + str(
                        spread) + 'pips。')

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
