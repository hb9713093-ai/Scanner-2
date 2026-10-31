#!/usr/bin/env python3
"""
Nifty 500 daily trend-flip scanner.

Trend colour logic (replicated from the SSL Hybrid baseline in Ricky's indicator):
  baseline = EMA(close, 30)
  channel  = baseline +/- 0.2 * EMA(TrueRange, 30)
  Blue  = close above upper channel
  Red   = close below lower channel
  Grey  = close inside channel
A "flip" is any day whose colour differs from the previous day.

Outputs:
  index.html          the website (table + click-TV popup chart)
  data/<SYMBOL>.json  last ~6 months of candles + channel for each stock (popup chart)

Usage:
  python scanner.py                   full run
  python scanner.py --check AXISBANK  prints recent colours + last flips for one stock
  python scanner.py --limit 40        quick test on first 40 stocks
"""
import argparse
import io
import json
import os
import re
import sys
import time
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote

import numpy as np
import pandas as pd
import requests
import yfinance as yf

# ----------------------------- settings -----------------------------
MA_LEN = 30
KELT_MULT = 0.2
HISTORY = "5y"
BATCH_SIZE = 50
CHART_BARS = 130                # ~6 months of daily candles in the popup chart
