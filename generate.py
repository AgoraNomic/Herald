from sys import argv
from csv import reader
from datetime import datetime, timezone 

isTest = "-t" in argv

if isTest:
    print("Running test generation.")

def scroll_center(string):
    #TODO: fix the scroll alignment so I don't have to add an extra 2
    #TODO: maybe expand this function's usages? or get rid of it.
    return int((72 / 2) - (len(string) / 2) + 2)

# Determine timestamp
now = datetime.now(timezone.utc)

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
        # If there's an entry in the "times" column, use it. Otherwise,
        # assume it was just once.
        times = 1
        if row[5] != "":
            times = int(row[5])
        # If this title isn't in the dict yet, add it.
        if not(row[0] in wins_lists):
            wins_lists[row[0]] = {}
        # If this person isn't in the title's dict yet, add em.
        if not(row[1] in wins_lists[row[0]]):
            wins_lists[row[0]][row[1]] = times
        # If e already is, add the times to the current tally.
        else:
            wins_lists[row[0]][row[1]] += times

# format wins for the report
max_title_len = 20

champions = ""
for title in wins_lists:
    # pad each title to a length of 20, right-aligned
    champions_line = " " * (max_title_len - len(title)) + title + ": "
    # add each winner and a ", " but first check if it would be too long
    # and start a new line if so
    for winner in wins_lists[title]:
        this_winner = winner
        if wins_lists[title][winner] > 1:
            this_winner += " (x" + str(wins_lists[title][winner]) + ")"
        this_winner += ", "
        if (len(champions_line) + len(this_winner)) > 72:
            champions += champions_line[0:72] + "\n"
            champions_line = " " * (max_title_len + 2) + champions_line[72:]
        champions_line += this_winner
    # remove the last ", " and add a new line for the next title
    champions += champions_line[:-2] + "\n"


# TODO: sort values here so I don't need a silly column in the csv
# import and process service awards
service_lists = {}
with open('Data/service.csv', 'r') as infile:
    in_service = reader(infile, delimiter=',', quotechar="\"")
    next(in_service) #skip header line
    for row in in_service:
        # If this title isn't in the dict yet, add it.
        if not(row[1] in service_lists):
            service_lists[row[1]] = []
        # If this person isn't in the title's list yet, add em.
        if not(row[2] in service_lists[row[1]]):
            service_lists[row[1]].append(row[2])

service_titles = ""
for title in service_lists:
    # pad to a length of 20, right-aligned
    title_line = " " * (max_title_len - len(title)) + title + ": "
    # add each holder and a ", " but first check if it would be too long
    # and start a new line if so
    for holder in service_lists[title]:
        this_holder = holder + ", "
        if (len(title_line) + len(this_winner)) > 72:
            service_titles += title_line[0:72] + "\n"
            title_line = " " * (max_title_len + 2)
        title_line += this_holder
    # remove the last ", " and add a new line for the next title
    service_titles += title_line[:-2] + "\n"

print(service_lists)

# Apply map and output report
with open('template.txt', 'r') as infile:
    template = infile.read()

mapping = {'fancy_time': fancy_time, 'champions': champions, 'service_titles': service_titles}

with open('Reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))

if not isTest:
    with open('scroll.txt', 'w') as ofile:
        ofile.write(template.format_map(mapping))
