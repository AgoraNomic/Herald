from sys import argv
from csv import reader
from datetime import datetime, timezone 

def scroll_center(string):
    return int((72 / 2) - (len(string) / 2) + 2)

notices_str = "No news since the previous report."
notices = " " * scroll_center(notices_str) + notices_str

# Determine timestamp

now = datetime.now(timezone.utc)

isTest = True

if isTest:
    report_name = "test"
else:
    report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

time_str = now.strftime('%B') + " " + str(now.day).zfill(2) + ", " + str(now.year)
#TODO: convert month to actual month name

# the extra 2 is there because the entire scroll is slightly off-center

fancy_time = " " * scroll_center(time_str) + time_str

# Apply map and output report

with open('template.txt', 'r') as infile:
    template = infile.read()

mapping = {'notices': notices, 'fancy_time': fancy_time}

with open('Reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))
