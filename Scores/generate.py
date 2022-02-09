from csv import reader

class Player:
    def __init__(self, n, sn, os, c):
        self.name = n
        self.short_name = sn.upper()
        self.old_score = int(os)
        self.change = int(c)
        self.score = self.old_score + self.change

players = []
max_score_len = 0

with open('scores.csv', 'r') as infile:
    score_file = reader(infile, delimiter=',', quotechar="\"")
    next(score_file) #skip header line
    
    for row in score_file:
        players.append(Player(row[0],row[1],row[2],row[3]))

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
    out += " " * (max_col_1-len(place_ord)+1)
    out += pl.short_name
    out += " " * 4
    out += str(pl.score)
    print(out)

for pl in players:
    if pl.score == previous_score:
        ties+=1
    else:
        place+=ties+1
        ties=0
    previous_score = pl.score
    formatter(place, pl)
