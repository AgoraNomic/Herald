from sys import argv
from csv import reader
from datetime import datetime, timezone

# Set arguments, first arg is previous score, second arg is changes
prev_rad_file = argv[1]
recent_changes_file = argv[2]

# set values for certain changes
cfj_amount = 3
author_amount = 4
coauthor_amount = 1

# Determine timestamp
now = datetime.now(timezone.utc)

# Player class
class Player:
    def __init__(self, n, sn, rd):
        self.name = n
        self.short_name = sn.upper()
        self.init_radiance = int(rd)
        self.radiance = self.init_radiance
    
    def change_score(self, c):
        self.radiance+= int(c)
        
    def set_score(self, c):
        ns = int(c)
        self.radiance = ns
        
    def quarterly(self):
        self.radiance= self.radiance//2
    
    def scorestr(self):
        digits = len(str(self.radiance))
        return "0" * (3-digits) + str(self.radiance)
        return str(self.radiance)
    
    def changestr(self):
        change = self.radiance - self.init_radiance
        if change == 0:
            return ""
        else:
            if change > 0:
                sign = "+"
            else:
                sign = ""
            return sign + str(change)

players = {}

# Open the previous radiance csv
with open(prev_rad_file, 'r') as infile:
    rads_in = reader(infile, delimiter=',', quotechar="\"")
    next(rads_in)
    
    for row in rads_in:
        players[row[0]] = Player(row[0],row[1],row[2])

# Read in and apply recent changes
history = ""

with open(recent_changes_file, 'r') as infile:
    recent_in = reader(infile, delimiter=',', quotechar="\"")
    next(recent_in) # skip headers
    
    for row in recent_in:
        date, name, event = row[0], row[1], row[2]
        if len(row) > 3:
            reason = row[3]
        if len(row) > 4:
            amount = row[4]
        history += f"{date}: "
        match event:
            case "SET":
                players[name].set_score(amount)
                history += f"{name} radiance set to {amount} ({reason})"
            case "ADJ":
                players[name].change_score(amount)
                if int(amount) >= 0:
                    history += f"{name} gains {amount} ({reason})"
                else:
                    history += f"{name} loses {amount} ({reason})"
            case "QRT":
                history += "New quarter, all radiances halved"
                for pl in players:
                    players[pl].quarterly()
            case "WIN":
                history += f"{name} wins by High Score. Eir score is set to 0. Other scores are halved."
                for pl in players:
                    if pl != name:
                        players[pl].quarterly()
                    else:
                        players[pl].set_score(0)
            case "CFJ":
                amount = cfj_amount
                players[name].change_score(amount)
                history += f"{name} gains {amount} (judgment of CFJ{reason})"
            case "AUT":
                amount = author_amount
                players[name].change_score(amount)
                history += f"{name} gains {amount} (author of P{reason})"
            case "COA":
                amount = coauthor_amount
                players[name].change_score(amount)
                history += f"{name} gains {amount} (coauthor of P{reason})"
            case "BDY":
                players[name].change_score(amount)
                history += f"{name} gains {amount} (birthday!)"
                
        history += "\n"

# This section makes the html and txt outputs

# Grab all the player names, then sort them by score
pl_keys = list(players.keys())
pl_keys.sort(key=lambda x:players[x].radiance, reverse=True) #sort by new score, desc

# define the ordinal numbers
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

place = 1
ties = -1 # starts at -1 because the first loop will iterate it
previous_score = players[pl_keys[0]].radiance
out = ""

report_scores = ""
html_scores = ""

def report_formatter(place, pl):
    out = ""
    out+= ordinal(place) + " " * (7 - len(ordinal(place)))
    out+= pl.short_name + " " * 7
    out+= pl.scorestr()
    if pl.changestr():
        out += f" ({pl.changestr()})"
    out+= "\n"
    return(out)

def html_formatter(place, pl):
    out = "<tr>"
    out+= f"<td>{ordinal(place)}</td>"
    out+= f"<td>{pl.short_name}</td>"
    if pl.changestr():
        out+= f"<td>{pl.scorestr()} ({pl.changestr()})</td>"
    else:
        out+= f"<td>{pl.changestr()}</td>"
    out+= "</tr>"
    return(out)

for player in pl_keys:
    pl = players[player]

    if pl.radiance == previous_score:
        ties+=1
    else:
        place+=ties+1
        ties=0
    previous_score = pl.radiance
    report_scores += report_formatter(place, pl)
    html_scores += html_formatter(place, pl)

# Generate key
key_list = ""
for player in pl_keys:
    key_list+= f"{players[player].name} = {players[player].short_name}; "

key_list = key_list[:-2]

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

print(report_scores)

with open("report.html", "w") as ofile:
    ofile.write(html)

with open('report.txt', 'w') as ofile:
    ofile.write(report)
    
with open('scores/' + now.strftime('%Y-%m-%d') + '.csv', 'w') as ofile:
    ofile.write("Name,Short_name,Radiance\n")
    for k in players.keys():
        pl = players[k]
        ofile.write(f"{pl.name},{pl.short_name},{pl.radiance}\n")

