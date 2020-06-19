import socket
from sea_battle.funcs.searching import (find_ships,
                                        get_ship_perimeter, )


def check_connection():
    """Проверка соединения с интернетом."""
    try:
        socket.gethostbyname('www.google.com')
    except socket.gaierror:
        return False
    return True


def ship_field_validation(matrix):
    """Комплексная проверка игрового поля.

    Возвращает False, если поле валидно, иначе - сообщение об ошибке.
    """
    check_list = [
        check_1,
        check_2,
        check_3,
    ]
    for check in check_list:
        message = check(matrix)
        if message:
            return message
    return False


def check_1(matrix):
    """Проверка на нужное количество закрашенных клеток.

    Площадь кораблей должна покрывать 20 клеток.
    Возвращает False, если поле валидно, иначе - сообщение об ошибке.
    """
    marked_cells = 0
    for line in matrix:
        marked_cells += sum(line)
    if marked_cells != 20:
        message = 'Cells marked incorrectly.'
        return message
    return False


def check_2(matrix):
    """Проверка на необходимое количество кораблей определенных типов.

    Требования к кораблям:
        1 четырехпалубный корабль,
        2 трехпалубных корабля,
        3 двухпалубных корабля,
        4 однопалубных корабля.
    Возвращает False, если поле валидно, иначе - сообщение об ошибке.
    """
    ships_requirement = {4: 1, 3: 2, 2: 3, 1: 4}
    ships_amount = {4: 0, 3: 0, 2: 0, 1: 0}
    for ship in find_ships(matrix):
        ship_size = len(ship)
        ship_amount = ships_amount.get(ship_size)
        if ship_amount is not None:
            ships_amount[ship_size] = ship_amount + 1
    if ships_amount != ships_requirement:
        message = 'Incorrect number of ships.'
        return message
    return False


def check_3(matrix):
    """Проверка на соприкосаемость.

    Проверка наличия в границах одного корабля другого корабля.
    Возвращает False, если поле валидно, иначе - сообщение об ошибке.
    """
    for ship in find_ships(matrix):
        ship_perimeter = get_ship_perimeter(ship)
        for coordinate in ship_perimeter:
            if matrix[coordinate[0]][coordinate[1]]:
                message = 'Ships cannot be placed near each other.'
                return message
    return False
