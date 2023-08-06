# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 05:22:37 2019

@author: tommy
"""

import os
import time
from datetime import timedelta

def beg():
    beg_tm = time.perf_counter()
    os.environ['the_logger_time'] =  str(beg_tm)

def end():
    end_tm = time.perf_counter()
    beg_tm = float(os.environ['the_logger_time'])
    sec_delta = end_tm - beg_tm
    sec_delta = round(sec_delta, 3)
    exec_tm = str(timedelta(seconds = sec_delta)).rstrip('0')
    print(f"Elapsed Time: {exec_tm}")
    