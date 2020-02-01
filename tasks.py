import os
import re
import win32com.client
from typing import List
from text_analis import *
from itertools import repeat
from functools import partial
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from multiprocessing import Pool
from itertools import combinations as comb


regular = r'[\d]+\. [А-ЯЁA-Z][А-ЯЁA-Z]{1,2}[\D]+'


def initialization(TF=True, IDF=False):
    with open("input\\stop_word.txt") as f:
        dictionary_of_stop_words = f.read().upper().split('\n')

    with open("input\\list_of_teachers.txt") as f:
        teachers = f.read().split('\n')

    for i, teacher in enumerate(teachers):
        teachers[i] = teacher.split(' ')
        with open("input\\{} {} {}.txt".format(teachers[i][0], teachers[i][1], teachers[i][2])) as f:
            teachers[i].append(f.read().split('\n'))
            teachers[i][4] = removing_special_characters(teachers[i][4])

    for i, teacher in enumerate(teachers):
        teachers[i][4] = partition2(teacher[4])

    for i, teacher in enumerate(teachers):
        teachers[i][4] = delete_english_word(teacher[4])

    for i, teacher in enumerate(teachers):
        teachers[i][4] = delete_numbers(teacher[4])

    for i, teacher in enumerate(teachers):
        teachers[i][4] = delete_stop_word(teacher[4], dictionary_of_stop_words)

    del dictionary_of_stop_words

    teachers_keyword = reception_keywords(teachers)

    keywords = sum_dict(teachers_keyword.copy())

    keywords = sort_val(keywords)

    keywords = delete_one_frequency_keyword(keywords)

    teachers_keyword = reception_keywords(teachers)

    teachers_keyword = profile(keywords, teachers_keyword)

    if TF:
        if IDF:
            teachers_keyword = tfidf(teachers_keyword)
        else:
            teachers_keyword = tf(teachers_keyword)

        keywords = sum_dict(teachers_keyword)

        keywords = sort_val(keywords)

        teachers_keyword = profile(keywords, teachers_keyword)

    teachers = set_keywords(teachers, teachers_keyword)

    return keywords, teachers, teachers_keyword


def var_cos(keywords, teachers):
    cos_array: List[List[float]] = []
    threshold_value = float(input('Введите пороговое значение: ').replace(',', '.'))

    for i, teacher1 in enumerate(teachers):
        cos_array.append([])
        for teacher2 in teachers:
            cos_array[i].append(vec_cos(teacher1[4].values(), teacher2[4].values()))

    position = []

    for i, value1 in enumerate(cos_array):
        for j, value2 in enumerate(value1):
            if (value2 >= threshold_value) & (1 > value2) & (i < j):
                position.append([i, j])

    with open("output\\output_all_cos.txt", 'w') as f:
        f.write('   ')
        for i, teacher in enumerate(teachers):
            f.write("{}.{}.{}.  ".format(teacher[0][0], teacher[1][0], teacher[2][0]))
        for i, list_val in enumerate(cos_array):
            f.write('\n{}'.format(i + 1).ljust(4, ' '))
            for val in list_val:
                f.write('{:.4f}  '.format(val))
        f.write('\n')
        for i, j in position:
            f.write("\n{0} {1}.{2}. -".format(teachers[i][0], teachers[i][1][0], teachers[i][2][0]))
            f.write("\t{0} {1}.{2}. \t- ".format(teachers[j][0], teachers[j][1][0], teachers[j][2][0]))
            f.write('{}'.format(cos_array[i][j]))

    flag = input('Построить облака слов: Да/Нет?')
    if flag == 'Да' or flag == 'Д':
        wc = WordCloud(background_color="white", height=500, width=1000)

        wc.generate_from_frequencies(keywords)

        plt.subplots(num=None, figsize=(16, 9), dpi=80)

        plt.imshow(wc, interpolation='bilinear')

        plt.gcf().canvas.set_window_title('Профиль_кафедры')

        plt.axis("off")

        plt.savefig('cloud/Профиль_кафедры.png')

        for i, j in position:
            name_fig = teachers[i][0] + '-' + teachers[j][0]
            buf = sum_values(teachers[i][4], teachers[j][4])
            buf = {k: v for k, v in buf.items() if v > 0}
            wc.generate_from_frequencies(buf)
            plt.subplots(num=None, figsize=(16, 9), dpi=100)
            plt.gcf().canvas.set_window_title(name_fig)
            plt.imshow(wc, interpolation='bilinear')
            plt.axis("off")
            plt.savefig('cloud/' + name_fig + '.png')
        plt.show()


def var_k_means(teachers, teachers_keyword):
    flag = input('Вариант задания:\n1 - ручной \n2 - автоматический\n')

    if flag == '1':
        while True:
            number_of_clusters = input('номера начала класстеров ').split(' ')
            if '' in number_of_clusters:
                number_of_clusters.remove('')

            input_provisions = []
            for i in number_of_clusters:
                input_provisions.append(teachers_keyword[int(i) - 1].copy())

            error, provisions_of_clusters = k_means(teachers_keyword, input_provisions, error_end=True)

            cluster = []
            for teacher in teachers:
                pos = belonging_of_cluster(teacher[4], provisions_of_clusters)
                cluster.append([teacher[0],
                                pos + 1,
                                length_vector(teacher[4].values(),
                                              provisions_of_clusters[pos].values())])

            cluster = sorted(cluster, key=lambda value: value[1])
            for val in cluster:
                print('{} {} {}'.format(*val))

            question = input("\nПовторить? Да/Нет  ")

            if not (question[0].upper() == 'Д' or question[0].upper() == 'Y'):
                break

    else:
        min_number_clusters = int(input('Минимальное колисество кластеров:  '))
        max_number_clusters = int(input('Максимальное колисество кластеров:  '))

        excel = win32com.client.Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(os.getcwd() + r'\Results\Clusters.xlsx')
        sheet = wb.Worksheets(3)

        for i, j in enumerate(range(min_number_clusters, max_number_clusters + 1)):
            error_all = []
            combination = list(comb(range(1, len(teachers) + 1), j))

            for x in combination:
                print(('{} ' * j).format(*x))

                input_provisions = []

                for val in x:
                    input_provisions.append(teachers_keyword[val - 1].copy())
                error, provisions_of_clusters = k_means(teachers_keyword, input_provisions, error_end=True)
                error_all.append(error)

            min_errors = list_items(error_all, min(error_all))
            sheet.Cells(1, j).value = u'{} кластеров'.format(j)
            sheet.Cells(2, j).value = min(error_all)
            for l, k in enumerate(min_errors):
                sheet.Cells(l + 3, j).value = ('{} ' * j).format(*(combination[k]))

            wb.Save()

        wb.Close()
        excel.Quit()

    return 0


def word_word(only_kwords=False):
    with open("input\\stop_word.txt") as f:
        dictionary_of_stop_words = f.read().upper().split('\n')

    with open("input\\list_of_teachers.txt") as f:
        teachers = f.read().split('\n')

    documents = []

    for teacher in teachers:
        teacher = teacher.split(' ')
        with open("input\\{} {} {}.txt".format(*teacher[:3])) as f:
            if only_kwords:
                documents += f.read().split('\n')
            else:
                documents += re.findall(regular, f.read())
    if only_kwords:
        k_words_pos = list_items(documents, 'КЛЮЧЕВЫЕ СЛОВА:')

        doc = documents.copy()

        documents.clear()
        for i in k_words_pos:
            documents.append(doc[i+1])

    documents = removing_special_characters(documents)

    documents = partition2(documents, True)

    for i, doc in enumerate(documents):
        documents[i] = delete_english_word(doc)

    for i, doc in enumerate(documents):
        documents[i] = delete_numbers(doc)

    for i, doc in enumerate(documents):
        documents[i] = delete_stop_word(doc, dictionary_of_stop_words)

    del dictionary_of_stop_words

    all_documents = sum_dict(documents.copy())

    all_documents = sort_val(all_documents)

    all_documents = delete_frequency_keyword(all_documents, 1, False)

    for i, doc in enumerate(documents):
        for word in doc.copy():
            if all_documents.get(word) is None:
                documents[i].pop(word)

    Excel = win32com.client.Dispatch('Excel.Application')
    wb = Excel.Workbooks.Open(os.getcwd() + r'\Results\Result.xlsx')
    sheet = wb.Worksheets('word-word')

    for i, word1 in enumerate(all_documents):
        print(i, word1)
        sheet.Cells(i + 2, 1).value = word1
        sheet.Cells(1, i + 2).value = word1
        for j, word2 in enumerate(all_documents):
            res = 0
            for doc in documents:
                if doc.get(word1) is not None and doc.get(word2) is not None and word1 != word2:
                    res += 1
            if res > 0:
                sheet.Cells(i + 2, j + 2).value = res
    wb.Save()
    wb.Close()
    Excel.Quit()


def text_clustering(n=30, TF=True, IDF=False, kwords=True, annotation=True):

    with open("input\\list_of_teachers.txt") as f:
        teachers = f.read().split('\n')

    documents = []

    for teacher in teachers:
        teacher = teacher.split(' ')
        with open("input\\{} {} {}.txt".format(*teacher[:3])) as f:
            documents += re.findall(regular, f.read())

    del teachers

    documents = kwords_annotation(documents, kwords, annotation)

    name_documents = []
    for doc in documents:
        name = doc.split('\n')[0]
        while True:
            if not name[0].isalpha():
                name = name[1:]
            else:
                break
        name_documents.append(name)

    documents = removing_special_characters(documents)

    keywords = partition2(documents, not_common=True)

    del documents

    for i, keyword in enumerate(keywords):
        keywords[i] = delete_english_word(keyword)

    for i, keyword in enumerate(keywords):
        keywords[i] = delete_numbers(keyword)

    with open("input\\stop_word.txt") as f:
        dictionary_of_stop_words = f.read().upper().split('\n')

    for i, keyword in enumerate(keywords):
        keywords[i] = delete_stop_word(keyword, dictionary_of_stop_words)

    del dictionary_of_stop_words

    while {} in keywords:
        pos_object = keywords.index({})
        del keywords[pos_object], name_documents[pos_object]

    all_keywords = sum_dict(keywords.copy())

    all_keywords = sort_val(all_keywords)

    all_keywords = delete_one_frequency_keyword(all_keywords)

    keywords = profile(all_keywords, keywords)

    keywords = delete_elements_certain_length(keywords, 2)

    if TF:
        if IDF:
            keywords = tfidf(keywords)
        else:
            keywords = tf(keywords)

    number_of_clusters = int(input('Количество кластеров: '))

    pool = Pool(processes=5)
    print('hello0')
    args = list(zip([number_of_clusters] * n, [keywords] * n, range(n)))

    input_provisions = pool.starmap(k_means_plus_plus, args)
    print('hello1')
    args = list(zip(repeat(keywords, n), input_provisions))

    dec = partial(k_means, error_end=True)

    output = pool.starmap(dec, args)
    print('hello2')
    error, cluster = list(zip(*output))

    cluster = cluster[error.index(min(error))]

    del error, pool, args

    cluster_output = []

    for i, keyword in enumerate(keywords):
        pos = belonging_of_cluster(keyword, cluster)
        cluster_output.append([name_documents[i], pos + 1])

    cluster_output = sorted(cluster_output, key=lambda value: value[1])

    for val in cluster_output:
        print('{} {}'.format(*val))

    sheet_name = 'Doc-clasters'

    if TF:
        if IDF:
            sheet_name += '-TF-IDF'
        else:
            sheet_name += '-TF'

    Excel = win32com.client.Dispatch('Excel.Application')
    wb = Excel.Workbooks.Open(os.getcwd() + '\\Results\\Res-{}.xlsx'.format(number_of_clusters))
    sheet = wb.Worksheets(sheet_name)

    k = 0
    i = 2
    for c_out in cluster_output:
        if c_out[1] != k:
            k += 1
            sheet.Cells(1, k).value = '{} кслатер'.format(k)
            i = 2
        sheet.Cells(i, c_out[1]).value = c_out[0]
        i += 1
    sheet = wb.Worksheets(sheet_name + '-info')

    for i, c_out in enumerate(cluster):
        sheet.Cells(1, 2*i + 1).value = '{} кслатер'.format(i + 1)
        c_out = delete_frequency_keyword(c_out, 0)
        c_out = sort_val(c_out)
        for j, word in enumerate(c_out):
            sheet.Cells(j + 2, 2 * i + 1).value = word
            sheet.Cells(j + 2, 2 * i + 2).value = c_out[word]
    wb.Save()
    wb.Close()
    Excel.Quit()

    return 0