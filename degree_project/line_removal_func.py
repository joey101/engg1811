def line_removal(file_name, word):
    word_removed = word

    with open(file_name, 'r') as data:
        read_file = data.readlines()
    with open('/home/bladerunner/Documents/degree_project/copy.txt', 'w') as data:
        for line in read_file:
            if word_removed in line.strip("\n"):
                continue
            data.write(line)
        
   


