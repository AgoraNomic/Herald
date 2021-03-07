from sys import argv
from csv import reader
from datetime import datetime, timezone 

isTest = "-t" in argv

if isTest:
    print("Running test generation.")

def scroll_center(string):
    #TODO: fix the scroll alignment so I don't have to add an extra 2
    return int((72 / 2) - (len(string) / 2) + 2)

notices_str = "Cuddlebeam has officially been awarded a win for Economic Takeover. \n \n The \"Champions\" portion of this report is now automatically generated. Feedback appreciated."
notices = " " * scroll_center(notices_str) + notices_str

# Determine timestamp

now = datetime.now(timezone.utc)

isTest = True

if isTest:
    report_name = "test"
else:
    report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)

time_str = now.strftime('%B %d, %Y')

fancy_time = " " * scroll_center(time_str) + time_str

# import and process wins
wins_lists = {}
with open('Data/champions.csv', 'r') as infile:
    in_wins = reader(infile, delimiter=',', quotechar="\"")
    next(in_wins) #skip header line
    for row in in_wins:
        times = 1
        if row[5] != "":
            times = int(row[5])
        if not(row[0] in wins_lists):
            wins_lists[row[0]] = {}
        if not(row[1] in wins_lists[row[0]]):
            wins_lists[row[0]][row[1]] = times
        else:
            wins_lists[row[0]][row[1]] += times

max_title_len = 20

champions = ""
for key in wins_lists:
    champions_line = " " * (max_title_len - len(key)) + key + ": "
    cur_len = len(champions)
    for winner in wins_lists[key]:
        this_winner = winner
        if wins_lists[key][winner] > 1:
            this_winner += " (x" + str(wins_lists[key][winner]) + ")"
        this_winner += ", "
        if (len(champions_line) + len(this_winner)) > 72:
            champions += champions_line[0:72] + "\n"
            champions_line = " " * (max_title_len + 2) + champions_line[72:]
        champions_line += this_winner
    champions += champions_line[:-2] + "\n"

# Apply map and output report

with open('template.txt', 'r') as infile:
    template = infile.read()

mapping = {'notices': notices, 'fancy_time': fancy_time, 'champions': champions}

with open('Reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))

if not isTest:
    with open('scroll.txt', 'w') as ofile:
        ofile.write(template.format_map(mapping))
