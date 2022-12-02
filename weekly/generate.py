from sys import argv
from csv import reader, writer
from datetime import datetime, timezone

isReport = "-r" in argv

headers = "Event,Name,Change,Reason,Date\n"

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
        
    def set_score(self, c):
        ns = int(c)
        self.change+= ns-self.score
        self.score = ns
        
    def quarterly(self):
        self.change+= 0-self.score//2
        self.score= self.score//2
    
    def scorestr(self):
        digits = len(str(self.score))
        return " " + "0" * (3-digits) + str(self.score)
    
    def changestr(self):
        if self.change == 0:
            return ""
        else:
            if self.change > 0:
                sign = "+"
            else:
                sign = ""
            
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
        if row[0] == "ADJ":
            players[row[1]].change_score(row[2])
        elif row[0] == "SET":
            players[row[1]].set_score(row[2])
        elif row[0] == "QRT":
            for pl in players:
                players[pl].quarterly()
        elif row[0] == "REG":
            players[row[1]] = Player(row[1], row[2], 0)
        elif row[0] == "DRG":
            players.pop(row[1])
        elif row[0] == "WIN":
            for pl in players:
                if pl != row[1]:
                    players[pl].quarterly()
                else:
                    players[pl].set_score(0)
        
        changes+=[row]
        
        # If it's a report, put all of this in the history file now that we're done with it
        if isReport:
            historic_file = 'history.csv'
            with open(historic_file, 'a') as outfile:
                outfile.write(','.join(row)+"\n")

if isReport:
    with open(recent_file, 'w') as outfile:
        outfile.write(headers)

# Grab all the player names, then sort them by score
pl_keys = list(players.keys())
pl_keys.sort(key=lambda x:players[x].score, reverse=True) #sort by new score, desc

# define the ordinal numbers
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

place = 1
ties = -1 # starts at -1 because the first loop will iterate it
previous_score = players[pl_keys[0]].score
out = ""

report_scores = ""
html_scores = ""

def report_formatter(place, pl):
    out = ""
    out+= ordinal(place) + " " * (7 - len(ordinal(place)))
    out+= pl.short_name + " " * 6
    out+= pl.scorestr() + " " * 4
    out+= pl.changestr()
    out+= "\n"
    return(out)

def html_formatter(place, pl):
    out = "<tr>"
    out+= "<td>" + ordinal(place) + "</td>"
    out+= "<td>" + pl.short_name + "</td>"
    out+= "<td>" + pl.scorestr() + "</td>"
    out+= "<td>" + pl.changestr() + "</td>"
    out+= "</tr>"
    return(out)

for player in pl_keys:
    pl = players[player]

    if pl.score == previous_score:
        ties+=1
    else:
        place+=ties+1
        ties=0
    previous_score = pl.score
    report_scores += report_formatter(place, pl)
    html_scores += html_formatter(place, pl)

pl_keys.sort(key=lambda x : players[x].name, reverse=False) #sort by name

# Generate key
key_list = ""
for player in pl_keys:
    key_list+= players[player].name + " = " + players[player].short_name + "; "

key_list = key_list[:-2]

history=""

#TODO: Make this more readable by turning the ints into descriptive vars?

for i in changes:
    history += i[4] + ": "
    if i[0] == "ADJ":
        if int(i[2]) >= 0:
            history += i[1] + " gains " + i[2] + " (" + i[3] + ")"
        else:
            history += i[1] + " loses " + i[2] + " (" + i[3] + ")"
    elif i[0] == "SET":
        history += i[1] + " score set to " + i[2] + " (" + i[3] + ")"
    elif i[0] == "QRT":
        history += "All players' scores halved for new quarter."
    elif i[0] == "REG":
        history += i[1] + " registers."
    elif i[0] == "DRG":
        history += i[1] + " is deregistered."
    elif i[0] == "WIN":
        history += i[1] + " wins via High Score. Eir score is set to 0. Other scores are halved."
    history+= "\n"

# Apply map and output report
with open('report.template', 'r') as infile:
    template = infile.read()

report_mapping = {'date': now.strftime('%d %b %Y'), 'history': history, 'scores': report_scores, 'key': key_list}

report = template.format_map(report_mapping)

# Apply map and output html
with open('report.html.template', 'r') as infile:
    template = infile.read()

html_mapping = {'date': now.strftime('%d %b %Y'), 'history': history, 'scores': html_scores, 'key': key_list}

html = template.format_map(html_mapping)

if not isReport:
    print(report)
    print(html)
else:
    report_name = now.strftime('%Y-%m-%d')

    with open(score_file, 'w') as outfile:
        outfile.write(headers)
        for player in pl_keys:
            outfile.write(players[player].name+","+players[player].short_name+","+str(players[player].score)+"\n")

    with open("report.html", "w") as ofile:
        ofile.write(html)

    with open('reports/' + report_name + '.txt', 'w') as ofile:
        ofile.write(report)

    with open('report.txt', 'w') as ofile:
        ofile.write(report)
