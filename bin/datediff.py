#!/usr/bin/env python3
#cython: language_level=3

from datetime import datetime
from dateutil import relativedelta

today = datetime.today()
past_date = datetime(2014, 2, 8)

diff = relativedelta.relativedelta(today, past_date)
nyear = diff.years
nmonth = diff.months
ndays = diff.days
msg = f'{nyear}, {nmonth}, {ndays}'
print(diff)
print(msg)

