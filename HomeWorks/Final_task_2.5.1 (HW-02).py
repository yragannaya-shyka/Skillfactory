from random import randint

# Классы исключений
# Базовый класс исключений, если придется добавлять что-то общее всем исключением
class BoardException(Exception):
    pass

#  Если ход игрока выходит за пределы доски
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете за доску. Выберите другую клетку"


#  Если выстрел осуществляется в уже стрелянную точку
class BoardShootenDotException(BoardException):
    def __str__(self):
        return "Вы уже сюда стреляли. Выберите другую клетку"

#  Если выстрел осуществляется в контур корабля
class BoardShootenCounterException(BoardException):
    def __str__(self):
        return "Вы не можете сюда стрелять. Это контур корабля. Выберите другую клетку"

# Если корабль расположен неправильно
class BoardWrongShipException(BoardException):
    pass


# Класс создания точки на поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Упрощение сравнения точек
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y




class Ship:
    def __init__(self, bow, length, ornt):
        self.bow = bow  # Точка носа корабля, начало отсчета.
        self.length = length  # Длина коробля.
        self.ornt = ornt  # Ориентация коробля, 0 - гор., 1 - верт.
        self.lives = length  # Кол-во жизней корабля; Логично прировнять к длине коробля.

    # Создание массива точек корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            crnt_x = self.bow.x
            crnt_y = self.bow.y

            if self.ornt == 0:
                crnt_x += i

            elif self.ornt == 1:
                crnt_y += i

            ship_dots.append(Dot(crnt_x, crnt_y))

        return ship_dots

    # Проверка "попадания". Есть ли точка выстрела в массиве точек корабля или нет
    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size  # Размер доски (для возможной масштабизации)
        self.field = [ ["О"]*size for _ in range(size) ]  # Двумерный списк, в котором хранятся состояния каждой из клеток.
        self.ships = []  # Список кораблей.
        self.hid = hid  # информация о том, нужно ли скрывать корабли на доске (для вывода доски врага), или нет (для своей доски).
        self.dead_ship_count = 0  # Количество живых кораблей
        self.used_dots = []  # Список занятых точек (кораблем или мимо)


    # Переписанный медот str, который выводит доску в консоль в зависимости от параметра hid
    def __str__(self):
        board = ""
        board += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            board += f"\n{i+1} | " + " | ".join(row) + " |"

        if self.hid:  # Если True - прятать доску (ее значения)
            board = board.replace("■", "O")
        return board

    # Метод, который для точки (объекта класса Dot ) возвращает True , если точка выходит за пределы поля, и False , если не выходит.
    def out(self, dot):
        return not((0<= dot.x < self.size) and (0<= dot.y < self.size))

    # Метод, который ставит корабль на доску (если ставить не получается, выбрасываем исключения).
    def add_ship(self, ship):

        # Проверка выхода точки за край доски
        for dot in ship.dots:
            if self.out(dot) or dot in self.used_dots:
                raise BoardWrongShipException()
        for dot in ship.dots:
            self.field[dot.x][dot.y] = "■"
            self.used_dots.append(dot)

        self.ships.append(ship)
        self.contour(ship)
    # Метод, который обводит корабль по контуру. Помечает соседние точки, где корабля по правилам быть не может.
    def contour(self, ship, verb = False):
        around = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in around:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not(self.out(cur)) and cur not in self.used_dots:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.used_dots.append(cur)

    # Метод, который делает выстрел по доске (если есть попытка выстрелить за пределы и в использованную точку, выбрасывает исключение)
    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()

        if dot in self.used_dots:
            raise BoardShootenDotException()

        self.used_dots.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.field[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.dead_ship_count += 1
                    self.contour(ship, verb = True)
                    print("Убит!")
                    return False
                else:
                    print("Ранен!")
                    return True

        self.field[dot.x][dot.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.used_dots = []

# Класс родитель для пользователя и компьютера
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    # Метод, который "спрашивает" игрока, в какую клетку он делает выстрел.
    def ask(self):
        raise NotImplementedError()

    # Метод, который делает ход в игре
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):

    # Выбирает случайную точку на доске
    def ask(self):
        dot = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {dot.x+1} {dot.y+1}")
        return dot

class User(Player):

    # Запрашивает координаты точки дял выстрела
    def ask(self):
        while True:
            dot = input("Ваш ход: ").split()

            # Проверки на корректность параметров точки
            if len(dot) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = dot

            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        user_board = self.random_board() #  Доска пользователя
        ai_board = self.random_board()  # Доска компьютера
        ai_board.hid = True  # Спрятать отображение кораблей компьютера

        self.user = User(user_board, ai_board)  # Игрок-пользователь
        self.ai = AI(ai_board, user_board)  # Игрок-компьютер

    # Метод генерирует случайную доску
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    # Метод расставляет корабли слцчайным образом от большого к маленькому
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]  # Список размеров кораблей
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 5000: #  Делает много попыток, если неудачно, генерирует исключение
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    # Метод, который в консоли приветствует пользователя и рассказывает о формате ввода
    def greet(self):
        print("-----------------------")
        print("Начало игры морской бой")
        print(" формат ввода хода: x y")
        print("   x - номер строки    ")
        print("   y - номер столбца   ")

    # Метод с самим игровым циклом
    def loop(self):
        player_step = 0  # Помогает определить чья очередь ходить
        while True:
            print("-"*27)
            print("Доска пользователя:")
            print(self.user.board)
            print("-"*27)
            print("Доска компьютера:")
            print(self.ai.board)
            if player_step % 2 == 0:
                print("-"*27)
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("-"*27)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                player_step -= 1

            if self.ai.board.dead_ship_count == 7:
                print("-"*27)
                print("Пользователь выиграл!")
                break

            if self.user.board.dead_ship_count == 7:
                print("-"*27)
                print("Компьютер выиграл!")
                break
            player_step += 1
    # Запуск игры
    def start(self):
        self.greet()
        self.loop()

# Старт игры
game = Game()
game.start()
