from random import (choice,
                    randint, )
from sea_battle.funcs.searching import get_ship_perimeter
from sea_battle.funcs.validation import ship_field_validation


def generate_empty_matrix(n):
    """Генерирует пустую матрицу размерности nxn."""
    empty_matrix = [[0 for i in range(n)] for i in range(n)]
    return empty_matrix


def generate_buttons_names():
    """Генерирует имена для чекбоксов.

    Возвращает матрицу размерностью 10x10, где каждый элемент представлен списком вида [['01', '0']], где
        '01' - имя чекбокса состоящее из номера строки и столбца чекбокса;
        '0' - статус чекбокса (было нажатие или нет).
    """
    length = range(10)
    elem_names = []
    for i in length:
        line = []
        for j in length:
            line.append([f'{i}{j}', '0'])
        elem_names.append(line)
    return elem_names


def generate_rand_ship_field():
    """Генерирует случайное игровое поле.

    Возвращает матрицу, в которой координаты кораблей отмечены единицами.
    Пример: [[0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1], ...].
    """
    ship_matrix = generate_empty_matrix(10)
    for ship_amount in range(1, 5):
        ship_count = 0
        while ship_count != ship_amount:
            flag = None
            # генерация координат нового корабля.
            new_ship = []
            i = randint(0, 4 + ship_amount)
            j = randint(0, 9)
            ship_orientation = choice(('vertical', 'horizontal'))
            for k in range(i, i + 5 - ship_amount):
                option = (k, j)
                if ship_orientation == 'vertical':
                    option = option[::-1]
                new_ship.append((option[0], option[1]))
            # проверка полного совпадения координат нового корабля с существующим.
            ship_size = len(new_ship)
            overlap = 0
            for coordinate in new_ship:
                if ship_matrix[coordinate[0]][coordinate[1]] == 1:
                    overlap += 1
            if overlap == ship_size:
                continue
            # проверка наличия в границах потенциального корабля уже существующего корабля.
            new_ship_perimeter = get_ship_perimeter(new_ship)
            for coordinate in new_ship_perimeter:
                if ship_matrix[coordinate[0]][coordinate[1]] == 1:
                    flag = True
                    break
            # добавление корабля на поле, если пройдены проверки.
            if not flag:
                for coordinate in new_ship:
                    ship_matrix[coordinate[0]][coordinate[1]] = 1
                ship_count += 1
    error = ship_field_validation(ship_matrix)
    if error:
        raise Exception(error)
    return ship_matrix
