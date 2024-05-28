c_list = ['редиска', 'лох']
lst = "Нехороший человек — Мох! редиска!"
for i in c_list:
    for j in lst.split():
        if i in j.lower():
            print(j)
            lst = lst.replace(j[0] + i[1:], j[0] + '*'*(len(i)-1))
print(lst)
print('-'.lower())
