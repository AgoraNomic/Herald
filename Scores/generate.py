from sys import argv
from csv import reader,writer
from datetime import datetime, timezone 

isReport = "-r" in argv

# Determine timestamp
now = datetime.now(timezone.utc)

class Player:
    def __init__(self, n, sn, os, c):
        self.name = n
        self.short_name = sn.upper()
        self.old_score = int(os)
        self.change = int(c)
        self.score = self.old_score + self.change

players = []
max_score_len = 0

csv_file = 'scores.csv'

edited = []

with open(csv_file, 'r') as infile:
    score_file = reader(infile, delimiter=',', quotechar="\"")
    edited.append(next(score_file)) #skip header line
    
    for row in score_file:
        players.append(Player(row[0],row[1],row[2],row[3]))
        edited.append([players[-1].name,players[-1].short_name,players[-1].score,0])

key = "KEY\n"
key+= "---\n"
for pl in players:
    key+= pl.name + " = " + pl.short_name + "; "

players.sort(key=lambda x:x.score, reverse=True) #sort by new score, desc

# define the ordinal numbers
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

place = 1
ties = -1 # starts at -1 because the first loop will iterate it
previous_score = players[0].score
out = ""

max_col_1 = len(ordinal(len(players)+1))

def formatter(place, pl):
    place_ord = ordinal(place)
    out = place_ord
    out += " " * (8-len(place_ord))
    out += pl.short_name
    out += " " * (7 - len(pl.short_name))
    str_score = "0" * (5 - len(str(pl.score))) + str(pl.score)
    out += str_score
    out += " " * 3
    if pl.change < 0:
        out += str(pl.change)
    elif pl.change > 0:
        out += "+" + str(pl.change)
    out += "\n"
    return(out)

output = "Scores as of " + now.strftime('%B %d, %Y') + "\n\n"
output+= "PLACE   " + "NAME" + "   SCORE   " + "CHANGE" + "\n"
output+= "-----   " + "----" + "   -----   " + "------" + "\n"

for pl in players:
    if pl.score == previous_score:
        ties+=1
    else:
        place+=ties+1
        ties=0
    previous_score = pl.score
    output += formatter(place, pl)

output+= "\n"
output+= key
output+= "\n\n"
output+= "If you'd like to change your three letter name, please let the Herald know."

if not isReport:
    print(output)
else:
    report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    
    # Edit the csv to incorporate changes
    with open(csv_file, 'w') as outfile:
        editor = writer(outfile, delimiter=',', quotechar="\"")
        
        for row in edited:
            editor.writerow(row)
    
    with open('reports/' + report_name + '.txt', 'w') as ofile:
        ofile.write(output)
        
    with open('scores.txt', 'w') as ofile:
        ofile.write(output)
