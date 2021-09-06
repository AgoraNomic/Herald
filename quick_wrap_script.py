messages = ["Aris has awarded Trigon the title Popular Polygon"]

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
