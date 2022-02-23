from sys import argv
from csv import reader,writer
from datetime import datetime, timezone 

isReport = "-r" in argv

# Determine timestamp
now = datetime.now(timezone.utc)

# Player class
class Player:
    def __init__(self, n, sn, sc):
        self.name = n
        self.short_name = sn.upper()
        self.score = int(sc)
        self.change = 0
    
    def change_score(self, c):
        self.change+= int(c)
        self.score+= int(c)
    
    def scorestr(self):
        digits = len(str(self.score))
        return "0" * (5-digits) + str(self.score)
    
    def changestr(self):
        if self.change == 0:
            return ""
        else:
            if self.change > 0:
                sign = "+"
            else:
                sign = "-"
            
            digits = len(sign + str(self.change))
            
            return " " * (6-digits) + sign + str(self.change)

players = {}
max_score_len = 0

edited = []

# Open the existing scores csv
score_file = 'scores.csv'
with open(score_file, 'r') as infile:
    scores_in = reader(infile, delimiter=',', quotechar="\"")
    next(scores_in)
    
    for row in scores_in:
        players[row[0]] = Player(row[0],row[1],row[2])

recent_file = 'recent.csv'
changes = []
with open(recent_file, 'r') as infile:
    recent_in = reader(infile, delimiter=',', quotechar="\"")
    next(recent_in)
    
    for row in recent_in:
        players[row[0]].change_score(row[1])
        
        changes+=[row]
        
        # If it's a report, put all of this in the history file now that we're done with it
        if isReport:
            historic_file = 'history.csv'
            with open(historic_file, 'a') as outfile:
                outfile.write(','.join(row)+"\n")

if isReport:
    with open(recent_file, 'w') as outfile:
        outfile.write("Name,Change,Reason\n")

# Grab all the player names, then sort them by score
pl_keys = list(players.keys())
pl_keys.sort(key=lambda x:players[x].score, reverse=True) #sort by new score, desc

# define the ordinal numbers
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

place = 1
ties = -1 # starts at -1 because the first loop will iterate it
previous_score = players[pl_keys[0]].score
out = ""

#Final output
output = "Scores as of " + now.strftime('%B %d, %Y') + "\n\n"
output+= "PLACE\t" + "NAME\t" + "SCORE\t" + "CHANGE" + "\n"
output+= "-----\t" + "----\t" + "-----\t" + "------" + "\n"

def formatter(place, pl):
    out = []
    out.append(ordinal(place))
    out.append(pl.short_name)
    out.append(pl.scorestr())
    out.append(pl.changestr())
    return('\t'.join(out)+"\n")

for player in pl_keys:
    pl = players[player]
    
    if pl.score == previous_score:
        ties+=1
    else:
        place+=ties+1
        ties=0
    previous_score = pl.score
    output += formatter(place, pl)

def dechunker(chunked, mlen):
    out = ""
    line = ""
    for chunk in chunked:
        if (len(line) + len(chunk)) > mlen:
            out+= line + "\n"
            line = ""
        line += chunk + " "
    out += line
    return out

pl_keys.sort(key=lambda x:players[x].name, reverse=False) #sort by name

# Generate key
key_list = []
for player in pl_keys:
    key_list.append(players[player].name + " = " + players[player].short_name + "; ")

output+= "\n"
output+= dechunker(key_list,73)
output+= "\n"

output+= "\n"
output+= dechunker("If you'd like to change your three letter name, please let the Herald know.".split(" "),73)
output+= "\n"

output+= "\n"
output+= "List of Recent Changes\n"
output+= "----------------------\n"

for i in changes:
    output+= ", ".join(i) + "\n"

if not isReport:
    print(output)
else:
    report_name = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    
    with open(score_file, 'w') as outfile:
        outfile.write("Name,Short,Score\n")
        for player in pl_keys:
            outfile.write(players[player].name+","+players[player].short_name+","+str(players[player].score)+"\n")
    
    with open('reports/' + report_name + '.txt', 'w') as ofile:
        ofile.write(output)
        
    with open('scores.txt', 'w') as ofile:
        ofile.write(output)
