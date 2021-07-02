messages = ["===============================", "THE SCROLL OF AGORA", "===============================", "Herald's Monthly Report", "-------------------", "NEWS", "-------------------", "Some of the scroll has been properly centered on 72 width. More to come", "Jason has won by Renaissance.","Aris has seen it wise to grant the titles Popular, Popular Philanthropist, Very Popular, and Most Popular to some players. These are listed in \"And More\".","Alphabet re-alphabetized.", "CHAMPION by", "ORDER OF THE HERO OF AGORA NOMIC", "--------------------------------", "GRAND HERO OF AGORA NOMIC","Peter Suber, Chuck Carroll, Douglas Hofstadter, Michael Norrish", "HERO OF AGORA NOMIC", "Murphy, G., omd"]

for item in messages:
    word_salad = item.split()
    output = ""
    chunks = []
    cur_chunk = ""
    for word in word_salad:
        if len(cur_chunk + " " + word) <= 72 - 6:
            if len(cur_chunk) > 0:
                cur_chunk += " "
            cur_chunk += word
        else:
            chunks.append(cur_chunk)
            cur_chunk = word
    chunks.append(cur_chunk)
    
    output = ""
    for chunk in chunks:
        l_pad = int((72 - len(chunk)) / 2)
        output += " " * l_pad + chunk + "\n"
    
    print(output)
