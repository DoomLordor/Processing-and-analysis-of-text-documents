from re import findall

regular = r'[\d]+\. [А-ЯЁA-Z][А-ЯЁA-Z]{1,2}[\D]+'

with open("input\\list_of_teachers.txt") as f:
    teachers = f.read().split('\n')

for teacher in teachers:
    teacher = teacher.split(' ')
    with open("input\\{} {} {}.txt".format(*teacher[:3])) as f:
        documents = findall(regular, f.read())

    with open("input\\{} {} {}.txt".format(*teacher[:3]), 'w') as f:
        for doc in documents:
            text = doc.split('\n')

            while ' \t' in text:
                text.remove(' \t')

            f.write(text[0] + '\n')
            if 'КЛЮЧЕВЫЕ СЛОВА:' not in text:
                f.write('КЛЮЧЕВЫЕ СЛОВА:\n\n')
            else:
                f.write(text[1] + '\n' + text[2] + '\n\n')
            if 'АННОТАЦИЯ:'not in text:
                f.write('АННОТАЦИЯ:\n\n')
            else:
                f.write(text[-2] + '\n' + text[-1] + '\n\n')

