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


class ICBC:
    FX = 'GBP,USD'
    sort = 'SE'

    plot = 0
    csv = '~/bocfx_output'
    pt = 0
    op = 0
    bar = 0
    outputmes = ''

    CurrencyName = ['英镑', '欧元', '美元', '日元', '港币', '加拿大元', '澳大利亚元']
    CurrencyCode = ['GBP', 'EUR', 'USD', 'JPY', 'HKD', 'CAD', 'AUD']
    SleepTime = -1

    def __init__(self, n, a, w):

        self.FX = 'GBP,USD'
        self.age = a
        self.__weight = w
        self.outputmes = ''
        self.pt = 0

    def sleeptimeget(sleeptime):
        try:
            sleeptime = input("多久刷新一次(s): ")
            if sleeptime == '':
                sleeptime = 120
                print("已按照默认设置刷新(120s)\n")
            else:
                sleeptime = int(sleeptime)
        except:
            print("输入有误,请重新输入.\n")

    def getQuotation(output, sort, FX_or, erectDate, nothing, FX, i, page, end):
        error_times = 0
        try:
            r = requests.post('https://srh.bankofchina.com/search/whpj/search_cn.jsp',
                              data={'erectDate': erectDate, 'nothing': nothing, 'pjname': str(FX[i]),
                                    'page': str(page)})
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

    def show_prog(all, ifbar=False):
        if ifbar:
            return (tqdm(all))
        else:
            return (all)

    def fxget(self):
        FXC = ['英镑', '欧元', '美元', '加拿大元', '澳大利亚元']
        FX_or = ['GBP', 'EUR', 'USD', 'CAD', 'AUD']
        erectDate = []

        if self.FX != 0:
            FXdict = {'英镑': '英镑', '港币': '港币', '美元': '美元', '瑞士法郎': '瑞士法郎', '德国马克': '德国马克', '法国法郎': '法国法郎',
                      '新加坡元': '新加坡元', '瑞典克朗': '瑞典克朗', '丹麦克朗': '丹麦克朗', '挪威克朗': '挪威克朗', '日元': '日元', '加拿大元': '加拿大元',
                      '澳大利亚元': '澳大利亚元', '欧元': '欧元', '澳门元': '澳门元', '菲律宾比索': '菲律宾比索', '泰国铢': '泰国铢', '新西兰元': '新西兰元',
                      '韩国元': '韩国元', '韩元': '韩国元', '卢布': '卢布', '林吉特': '林吉特', '新台币': '新台币', '西班牙比塞塔': '西班牙比塞塔',
                      '意大利里拉': '意大利里拉', '荷兰盾': '荷兰盾', '比利时法郎': '比利时法郎', '芬兰马克': '芬兰马克', '印度卢比': '印度卢比', '印尼卢比': '印尼卢比',
                      '巴西里亚尔': '巴西里亚尔', '阿联酋迪拉姆': '阿联酋迪拉姆', '南非兰特': '南非兰特', '沙特里亚尔': '沙特里亚尔', '土耳其里拉': '土耳其里拉',
                      'GBP': '英镑', 'HKD': '港币', 'USD': '美元', 'CHF': '瑞士法郎', 'DEM': '德国马克', 'FRF': '法国法郎', 'SGD': '新加坡元',
                      'SEK': '瑞典克朗', 'DKK': '丹麦克朗', 'NOK': '挪威克朗', 'JPY': '日元', 'CAD': '加拿大元', 'AUD': '澳大利亚元',
                      'EUR': '欧元', 'MOP': '澳门元', 'PHP': '菲律宾比索', 'THB': '泰国铢', 'NZD': '新西兰元', 'WON': '韩国元', 'RUB': '卢布',
                      'MYR': '林吉特', 'NTD': '新台币', 'ESP': '西班牙比塞塔', 'ITL': '意大利里拉', 'ANG': '荷兰盾', 'BEF': '比利时法郎',
                      'FIM': '芬兰马克', 'INR': '印度卢比', 'IDR': '印尼卢比', 'BRL': '巴西里亚尔', 'AED': '阿联酋迪拉姆', 'ZAF': '南非兰特',
                      'SAR': '沙特里亚尔', 'TRY': '土耳其里拉', 'UK': '英镑', 'HK': '港币', 'US': '美元', 'FF': '法国法郎', 'JP': '日元',
                      'CA': '加拿大元', 'AU': '澳大利亚元', 'EU': '欧元', 'KIWI': '新西兰元', 'SK': '韩国元', 'RU': '卢布', 'SEN': '林吉特',
                      'TW': '新台币', 'YTL': '土耳其里拉', 'THAI': '泰国铢', 'USA': '美元', 'MO': '澳门元'}

            FXArray = str.upper(self.FX).split(',')
            FX_ed = []

            for i in FXArray:
                try:
                    FX_ed.append(FXdict[i])
                except:
                    print('FX Value error!')
                    exit()

            FX_or = self.FX.copy()
            FXC = FX_ed

        else:
            FXC = ['英镑', '欧元', '美元', '加拿大元', '澳大利亚元']
            FX_or = ['GBP', 'EUR', 'USD', 'CAD', 'AUD']

        if self.sort != 0:
            sort = self.sort.split(',')
            if 'SE' in sort or 'se' in sort or 'Se' in sort:
                if 'BID' in sort or 'bid' in sort or 'Bid' in sort:
                    sort = '(FX_or[i],SE_B,time)'
                    output = [(len(FXC), 'SE_BID', 'Time')]
                elif 'ASK' in sort or 'ask' in sort or 'Ask' in sort:
                    sort = '(FX_or[i],SE_A,time)'
                    output = [(len(FXC), 'SE_ASK', 'Time')]
                else:
                    sort = '(FX_or[i],SE_B,SE_A,time)'
                    output = [(len(FXC), 'SE_BID', 'SE_ASK', 'Time')]
            elif 'BN' in sort or 'bn' in sort or 'Bn' in sort:
                if 'BID' in sort or 'bid' in sort or 'Bid' in sort:
                    sort = '(FX_or[i],BN_B,time)'
                    output = [(len(FXC), 'BN_BID', 'Time')]
                elif 'ASK' in sort or 'ask' in sort or 'Ask' in sort:
                    sort = '(FX_or[i],BN_A,time)'
                    output = [(len(FXC), 'BN_ASK', 'Time')]
                else:
                    sort = '(FX_or[i],BN_B,BN_A,time)'
                    output = [(len(FXC), 'BN_BID', 'BN_ASK', 'Time')]
            elif 'BID' in sort or 'bid' in sort or 'Bid' in sort:
                sort = '(FX_or[i],SE_B,BN_B,time)'
                output = [(len(FXC), 'SE_BID', 'BN_BID', 'Time')]
            elif 'ASK' in sort or 'ask' in sort or 'Ask' in sort:
                sort = '(FX_or[i],SE_A,BN_A,time)'
                output = [(len(FXC), 'SE_ASK', 'BN_ASK', 'Time')]
            else:
                print("Sort Value error!")
                exit()
        else:
            sort = '(FX_or[i],SE_B,BN_B,SE_A,BN_A,time)'
            output = [(len(FXC), 'SE_BID', 'BN_BID', 'SE_ASK', 'BN_ASK', 'Time')]

        if self.time != -1:
            if len(str(self.time)) < 5:
                today_nof = datetime.date.today()
                tegart_nof = today_nof - datetime.timedelta(days=int(self.time))
                erectDate = str(tegart_nof)
                nothing = str(today_nof)
            elif ',' in self.time:
                time = self.time.split(",")
                erectDate = str(time[0])
                nothing = str(time[1])
            elif '-' in self.time:
                today_nof = datetime.date.today()
                erectDate = str(self.time)
                nothing = str(today_nof)
            else:
                print("Incorrect time input!")
                all_task = []
                for i in range(len(FXC)):
                    r = requests.post('https://srh.bankofchina.com/search/whpj/search_cn.jsp',
                                      data={'erectDate': erectDate, 'nothing': nothing, 'pjname': FXC[i], 'page': '1'})
                    r = r.text
                    searchOBJ = re.search(r'var m_nRecordCount = (.*);', r)
                    pages = (int(searchOBJ.group(1)) // 20) + 1

                    ex = ThreadPoolExecutor(max_workers=20)
                    for page in range(1, (pages + 1)):
                        all_task.append(ex.submit(page_get, output, sort, FX_or, erectDate, nothing, FX, i, page, 22))

                [i.result() for i in show_prog(all_task, ifbar=bar)]
                ex.shutdown(wait=True)
                output = list(set(output))
                output.sort(reverse=True, key=lambda ele: ele[-1])
                filename = '[' + '+'.join(FX_or) + ']' + '+'.join(output[0][1:-1]) + '_' + erectDate + '_' + nothing
            else:
            ex = ThreadPoolExecutor(max_workers=20)
            all_task = [ex.submit(page_get, output, sort, FX_or, '', '', FXC, i, '1', 3) for i in range(len(FX))]
            [i.result() for i in show_prog(all_task, ifbar=bar)]
            ex.shutdown(wait=True)

            t = [output[0]]
            for i in range(len(FX_or)):
                for f in range(len(output)):
                    if output[f][0] == FX_or[i]:
                        t.append(output[f])
        output = t
        filename = '[Basic]' + output[1][-1].replace(' ', '_')

        if self.pt != 0:
            from prettytable import PrettyTable

            pt = PrettyTable(output[0])
            for i in output[1:]:
                pt.add_row(i)

            print('\n')
            print(pt)
            print("(SE = Spot Exchange, BN = Banknote)")

        else:
            pass
            # print(output)

        if self.csv != 0:
            op = os.path.expanduser(self.op)
            if not os.path.exists(op):
                os.makedirs(op)
                csvpath = os.path.join(op, filename) + '.csv'

            with open(csvpath, 'w') as f:
                for i in output:
                    f.write(','.join(map(str, i)) + '\n')
            print('\n.csv has already saved to ' + csvpath)

        if self.plot != 0:
            import numpy as np
            import matplotlib.pyplot as plt

            p = np.array(output)
            fl = len(FX_or)
            plt.figure(figsize=(13, 8.5))

            for f in range(fl):
                plt.subplot(fl, 1, f + 1)
                sd = p[np.where(p[:][:, 0] == FX_or[f])]
                x = sd[:, -1][:].astype(np.datetime64)

                for i in range(1, len(output[0]) - 1):
                    plt.plot(x, sd[:, i][:].astype(float),
                             label='[' + FX_or[f] + ']' + str(p[:, i][0]) + ': ' + str(sd[:, i][0]))
                plt.legend(loc=2)
            op = os.path.expanduser(op)
            if not os.path.exists(op):
                os.makedirs(op)
            plotpath = os.path.join(op, filename) + '.png'

            plt.savefig(plotpath, dpi=150)
            print('\nPlot has already saved to ' + plotpath)
            plt.show()

        if len(output[1]) == 3 and time == -1 and self.plot == 0 and self.csv == 0 and pt == 0:
            simple_output = [i[1] for i in output[1:]]
            output = simple_output
        return self.outputmes
