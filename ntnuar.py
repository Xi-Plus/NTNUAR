import argparse
import datetime
import calendar
import random
from config import *

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, default=datetime.date.today().year)
parser.add_argument('--month', type=int, default=datetime.date.today().month)
parser.add_argument('--holiday', type=int, action='append', default=[])
args = parser.parse_args()
print(args)

YEAR = args.year
MONTH = args.month
HOLIDAY = args.holiday

remain_hours = all_hours
result = {}
for date in range(1, calendar.monthrange(YEAR, MONTH)[1] + 1):
    result[date] = []

for avail in available_time:
    day = avail[0]
    start = avail[1]
    end = avail[2]
    for week in calendar.monthcalendar(YEAR, MONTH):
        date = week[day - 1]
        if date != 0 and date not in HOLIDAY:
            if remain_hours >= end - start:
                result[date].append([start, end])
                remain_hours -= (end - start)
            else:
                result[date].append([start, start + remain_hours])
                remain_hours = 0
        if remain_hours <= 0:
            break
    if remain_hours <= 0:
        break

print('remain_hours', remain_hours)

with open('out.txt', 'w') as f:
    for date in range(1, calendar.monthrange(YEAR, MONTH)[1] + 1):
        f.write('{}\t'.format(date))
        if len(result[date]) == 0:
            f.write('off day')
        else:
            result[date].sort()
            for work in result[date]:
                start_min = random.randint(0, 3)
                end_min = random.randint(start_min + 1, 4)
                f.write('{}:{:02d}-{}:{:02d}\t'.format(
                    work[0], start_min,
                    work[1], end_min,
                ))
        f.write('\n')
