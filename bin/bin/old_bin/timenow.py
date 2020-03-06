#!/usr/bin/python3
import datetime
from time import gmtime, strftime
from pytz import timezone
local_time=timezone('Europe/London')
fmt='%Y-%m-%d %H:%M%z'
loc_dt=local_time.localize(datetime.datetime.now())
formatted_dt=loc_dt.strftime(fmt)
print(formatted_dt)
