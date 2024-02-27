#check GIT
"""Создание стола
Возвращает пронумерованную матрицу размером size с филлером filler
"""
def create_table(size, filler="-"):
    table = [[filler for _ in range(size + 1)] for _ in range(size + 1)] #Создание таблицы соответсвующего размера заполненого филлером
    for i in range(len(table) - 1): #Создание нумеровки строк и столбцов
        table[0][i + 1] = i
        table[i + 1][0] = i
    table[0][0] = ' ' #Присвоение пустого значения первому элементу таблицы (по условию задачи)
    return table


"""Вывод текущего счета"""
def display_score(score_list):
    return print(f"Текущий счет: X = {score_list[0]}, O = {score_list[1]}.")


"""Обновление стола"""
def refresh_table(table):
    for i in range(1, len(table)):
        for j in range(1, len(table)):
            table[i][j] = '-'
    return table


"""Вывод стола"""
def display_table(table):
    return [print(*row) for row in table]


"""Вывод победителя"""
def display_result(table, score_list):
    """Победа в линию"""
    for row in table:
        check_x = list(map(lambda x: True if x == "x" else False, row[1:]))  # Проверка на строку ххх
        if all(check_x):
            score_list[0] +=1
            return display_table(table), print('Победил X'), display_score(score_list), display_table(refresh_table(table=table))

        check_o = list(map(lambda x: True if x == "o" else False, row[1:]))  # Проверка на стркоу ooo
        if all(check_o):
            score_list[1] +=1
            return display_table(table), print('Победил O'), display_score(score_list), display_table(refresh_table(table=table))

    """Победа в колонку"""
    for i in range(1, len(table)):

        check_list_col = [table[j][i] for j in range(1, len(table))]

        check_x_col = map(lambda x: True if x == "x" else False, check_list_col)  # Проверка колонки ххх
        if all(check_x_col):
            score_list[0] +=1
            return display_table(table), print('Победил X'), display_score(score_list), display_table(refresh_table(table=table))

        check_o_col = map(lambda x: True if x == "o" else False, check_list_col)  # Проверка колонки ooo
        if all(check_o_col):
            score_list[1] +=1
            return display_table(table), print('Победил O'), display_score(score_list), display_table(refresh_table(table=table))

    """Победа по диагонали"""
    check_list_diag_right = [table[i][i] for i in range(1 , len(table))]  # Спадающая диагональ
    check_list_diag_left = [table[i][len(table) - i] for i in range(1 , len(table))]  # Растущая диагональ

    # Проерка диагоналей ххх
    if all(map(lambda x: True if x == "x" else False, check_list_diag_right)) or all(map(lambda x: True if x == "x" else False, check_list_diag_left)):
        score_list[0] +=1
        return display_table(table), print('Победил X'), display_score(score_list), display_table(refresh_table(table=table))

    # Проверка диагоналей ooo
    if all(map(lambda x: True if x == "o" else False, check_list_diag_right)) or all(map(lambda x: True if x == "o" else False, check_list_diag_left)):
        score_list[1] +=1
        return display_table(table), print('Победил O'), display_score(score_list), display_table(refresh_table(table=table))

    """Ничья"""
    ev = [True for row in table[1:] if '-' in row]  # Если есть хоть один '-' (пустая клетка)
    if not ev:
        return display_table(table), print("Ничья"), display_table(refresh_table(table=table))  # Возвращает результат если больше нет свободных клеток

    """Игра продолжается"""
    return display_table(table=table)  # Если пока никто не победил или нет ничьи


"""Функционал игры:
Замена филлера (по умолчанию "-") на x/o
Формат хода: XY S. Где X - номер строки, Y - номер столбца, S - знак x/o.
K примеру ввод следующей сроки "22 x" в поле 3x3 разместит 'x' в ряд 2 колонку 2.
"""
def play(table, command="start", score_list=[0,0]):
    if command == "start":
        return display_table(table)

    if command == "reset":
        return display_table(refresh_table(table=table))

    if command == "score":
        return display_score(score_list), display_table(table)

    # Проверка на неправельный диапозон хода
    pos = [int(i) + 1 for i in command.split()[0]]  # Определение клетки хода
    if pos[0] > len(table) - 1 or pos[1] > len(table) - 1:
        alarm_msg = f"Вы ввели значение хода больше допустимого! Максимально допустимое значение: {len(table) - 2}"
        return print(alarm_msg)

    # Проверка на занятость клетки
    if table[pos[0]][pos[1]] != '-':
        alarm_msg = "Эта клетка уже занята, выберите лубую свободную!"
        return print(alarm_msg)

    sgn = command.split()[1]  # Определение знака хода
    # Проверка на корректность вводимого знака
    if sgn != 'x' and sgn !="o":
        alarm_msg = f"Вы ввели некорректный символ хода! Допустимые символы хода: x или o."
        return print(alarm_msg)

    # Если все хорошо, делает ход и возвращает доску
    table[pos[0]][pos[1]] = sgn
    return display_result(table, score_list)

"""Запуск игры"""

command = 'start'  # Инициализация игры
table_size = int(input())  # Ввод размера доски
table = create_table(table_size)  # Создание доски соответствующего размера

while command != 'exit':
    play(table, command)
    command = input()

print("Вы вышли из игры!")
