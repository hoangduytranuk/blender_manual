#!/usr/bin/env python3
from datetime import datetime
import pytz

class ReportCurrentTime:
    def run(self):
        tz_london = pytz.timezone('Europe/London')
        datetime_london = datetime.now(tz_london)
        current_time = datetime_london.strftime("%Y-%m-%d %H:%M%z")
        print(current_time)

x = ReportCurrentTime()
x.run()