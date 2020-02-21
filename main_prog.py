import tasks

if __name__ == '__main__' :
    options = ['Косинусное сходство', 'Метод К-средних', 'Построение профиля', 'Кластеризация статей']
    res_string = 'Вариант задания:\n'

    for i in range(len(options)):
        res_string += '{} - '.format(i + 1) + '{}\n'

    flag = input(res_string.format(*options))

    if flag == '1':
        keywords, teachers, teachers_keyword = tasks.initialization(TF=False)
        tasks.var_cos(keywords, teachers)
    elif flag == '2':
        keywords, teachers, teachers_keyword = tasks.initialization()
        tasks.var_k_means(teachers, teachers_keyword)
    elif flag == '3':
        keywords, name_documets, all_keywords = tasks.doc_initialization()
        tasks.word_word(True)
    elif flag == '4':
        keywords, name_documets, all_keywords = tasks.doc_initialization(annotation=False)
        tasks.text_clustering(keywords, name_documets)
