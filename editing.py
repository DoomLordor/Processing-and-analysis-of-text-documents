with open("input\\list_of_teachers.txt") as f:
    teachers = f.read().split('\n')

for teacher in teachers:
    teacher = teacher.split(' ')
    with open("input\\{} {} {}.txt".format(*teacher[:3])) as f:
        doc = f.read().split('\n')

    while '' in doc:
        doc.remove('')
    while ' \t' in doc:
        doc.remove(' \t')

    with open("input\\{} {} {}.txt".format(*teacher[:3]), 'w') as f:
        flag = False
        flag1 = False
        for text in doc:
            if text[0].isdigit():
                if flag1:
                    f.write('\n')
                flag1 = True
            f.write(text + '\n')
            if flag:
                f.write('\n')
                flag = False

            if text == 'КЛЮЧЕВЫЕ СЛОВА:' or text == 'АННОТАЦИЯ:':
                flag = True
                flag1 = False
