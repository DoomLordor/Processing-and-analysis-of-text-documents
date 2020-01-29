with open("input\\list_of_teachers.txt") as f:
    teachers = f.read().split('\n')

documents = []

for teacher in teachers:
    teacher = teacher.split(' ')
    with open("input\\{} {} {}.txt".format(*teacher[:3])) as f:
        documents.append(f.read())

str = input('Строка для поиска:   ')

while str:
    for i, text in enumerate(documents):
        if str in text or text in str:
            print(teachers[i].split()[0])
    str = input('Строка для поиска:   ')
