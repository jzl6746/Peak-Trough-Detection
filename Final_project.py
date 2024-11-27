# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:25:46 2024

@author: Letko
"""

import numpy as np
import tensorflow as tf
import keras
import matplotlib
import PyQt5

from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#api key: BBCT3KLZKHATW4RP
Dailyurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=BBCT3KLZKHATW4RP'
Weeklyurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=BBCT3KLZKHATW4RP'
Monthlyurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=BBCT3KLZKHATW4RP'
fiveMinurl = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=BBCT3KLZKHATW4RP'
r = requests.get(url)
data = r.json()

print(data)


