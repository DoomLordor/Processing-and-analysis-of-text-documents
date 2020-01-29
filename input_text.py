name_file = input("Название файла  ")
i = int(input("Номер позиции  "))
file = open(name_file, 'a')
word = input()
while word != 'Всё':
    if word == '':
        word = input()
    if word[0] == '\t':
        word = word[1:-1]
    file.write("{}. {}\n".format(i, word))
    i += 1
    word = input()
    if word == "КЛЮЧЕВЫЕ СЛОВА:":
        file.write("{}\n".format(word))
        word = input()
        word = input()
        file.write("{}\n\n".format(word))
        word = input()
    if word == 'АННОТАЦИЯ:':
        file.write("{}\n".format(word))
        word = input()
        word = input()
        word = input()
        while word != '/':
            file.write("{}\n\n".format(word))
            word = input()
    word = input()
file.close()
