# -*- coding:utf-8 -*- 
# 
# 
# 

import getopt
import sys
import time as tm
import os
import requests

from scrapy.selector import Selector
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import datetime
import re
from BCHO import BCHO

sd = BCHO()
sd.setSleepTime(5)
example01 = sd.getQuotation()

print(example01)
all_task = []

ex = ThreadPoolExecutor(max_workers=20)
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
