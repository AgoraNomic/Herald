from sys import argv
from csv import reader
from datetime import datetime, timezone 

isTest = "-t" in argv

if isTest:
    print("Running test generation.")

def scroll_center(string):
    #TODO: fix the scroll alignment so I don't have to add an extra 2
    #TODO: maybe expand this function's usages? or get rid of it.
    return int((72 / 2) - (len(string) / 2))

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
service_lists = {}
with open('Data/titles.csv', 'r') as infile:
    in_titles = reader(infile, delimiter=',', quotechar="\"")
    next(in_titles) #skip header line
    
    # add the titles for service manually, so they're sorted
    service_lists["Three Months"] = []
    service_lists["Six Months"] = []
    service_lists["Nine Months"] = []
    service_lists["Twelve Months"] = []
    
    for row in in_titles:
        if row[0] == "Champion":
            # If there's an entry in the "times" column, use it. Otherwise,
            # assume it was just once.
            times = 1
            if row[6] != "":
                times = int(row[6])
            # If this title isn't in the dict yet, add it.
            if not(row[1] in wins_lists):
                wins_lists[row[1]] = {}
            # If this person isn't in the title's dict yet, add em.
            if not(row[2] in wins_lists[row[1]]):
                wins_lists[row[1]][row[2]] = times
            # If e already is, add the times to the current tally.
            else:
                wins_lists[row[1]][row[2]] += times
        elif row[0] == "Service Award":
            if not(row[2] in service_lists[row[1]]):
                service_lists[row[1]].append(row[2])

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

service_titles = ""
for title in service_lists:
    # pad to a length of 20, right-aligned
    title_line = " " * (max_title_len - len(title)) + title + ": "
    # add each holder and a ", " but first check if it would be too long
    # and start a new line if so
    for holder in service_lists[title]:
        this_holder = holder + ", "
        if (len(title_line) + len(this_holder)) > 72:
            service_titles += title_line[0:72] + "\n"
            title_line = " " * (max_title_len + 2)
        title_line += this_holder
    # remove the last ", " and add a new line for the next title
    service_titles += title_line[:-2] + "\n"

# Apply map and output report
with open('template.txt', 'r') as infile:
    template = infile.read()

mapping = {'fancy_time': fancy_time, 'champions': champions, 'service_titles': service_titles}

with open('Reports/' + report_name + '.txt', 'w') as ofile:
    ofile.write(template.format_map(mapping))

if not isTest:
    with open('scroll.txt', 'w') as ofile:
        ofile.write(template.format_map(mapping))
