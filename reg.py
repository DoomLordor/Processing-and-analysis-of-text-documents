import tasks
import text_analis
import win32com.client
from itertools import combinations as comb
regular = r'[\d]+\. [А-ЯЁA-Z][А-ЯЁA-Z]{1,2}[\D]+'

keywords, teachers, teachers_keyword = tasks.initialization(TF=False)

Excel = win32com.client.Dispatch('Excel.Application')
wb = Excel.Workbooks.Open(r'E:\test1\Result.xlsx')
sheet = wb.Worksheets('word-word-df')

# new_kwd = {}
#
# for kw in keywords:
#     new_kwd[kw] = []
#     for tkw in teachers_keyword:
#         new_kwd[kw].append(tkw[kw])

# new_kwd = dict(sorted(new_kwd.items(), key=lambda x: (-x[1][3], x[0])))

# for i, word in enumerate(new_kwd):
#     sheet.Cells(i + 2, 1).value = word
#     for j, val in enumerate(new_kwd[word]):
#         sheet.Cells(i + 2, j + 2).value = val

# combination = comb(range(1, len(teachers_keyword)+1), 2)
#
# res_array = [[(i, j), text_analis.length_vector(teachers_keyword[i-1].values(), teachers_keyword[j-1].values())]
#              for i, j in combination]
#
# res_array = sorted(res_array, key=lambda x: x[1])
#
# for k, ((i, j), x) in enumerate(res_array):
#     k += 1
#     sheet.Cells(k, 1).value = i
#     sheet.Cells(k, 2).value = j
#     sheet.Cells(k, 3).value = str(0.25 - x)

# for i, word1 in enumerate(keywords):
#     sheet.Cells(i+2, 1).value = word1
# for i, word1 in enumerate(keywords):
#     sheet.Cells(1, i+2).value = word1

for i, word1 in enumerate(keywords):
    print(i, word1)
    for j, word2 in enumerate(keywords):
        res = 0
        for teacher_words in teachers_keyword:
            if teacher_words[word1] > 0 and teacher_words[word2] > 0:
                res += 1
        sheet.Cells(i+2, j+2).value = res
wb.Save()
wb.Close()
Excel.Quit()
