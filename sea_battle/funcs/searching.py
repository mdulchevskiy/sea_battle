from copy import deepcopy


def get_ship_perimeter(ship):
    """Определяет координаты периметра корабля.

    Возвращает список координат периметра корабля.
    """
    x_axis = []
    y_axis = []
    for x, y in ship:
        x_axis.append(x)
        y_axis.append(y)
    # условие сценария поиска координат в зависимости от ориентации корабля.
    if all(ind == y_axis[0] for ind in y_axis):
        option = (0, 1)
    elif all(ind == x_axis[0] for ind in x_axis):
        option = (1, 0)
    ship_perimeter = []
    ship_size = len(ship)
    for num, coordinate in enumerate(ship):
        # нахождение периметра крайних граней или единичного корабля.
        if not num or num == ship_size - 1 or ship_size == 1:
            repeat = 2 if ship_size == 1 else 1
            for mark in range(repeat):
                j = -1 if not num else 1
                if mark:
                    j = -j
                for i in range(3):
                    a = coordinate[option[0]] + j
                    b = coordinate[option[1]] - 1 + i
                    offset = (a, b)
                    if option[0]:
                        offset = offset[::-1]
                    if 10 > a >= 0 and 10 > b >= 0:
                        ship_perimeter.append([offset[0], offset[1]])
        # нахождение периметра боковых граней.
        sub_option = (1, -1)
        for i in sub_option:
            a = coordinate[option[0]]
            b = coordinate[option[1]] + i
            offset = (a, b)
            if option[0]:
                offset = offset[::-1]
            if 10 > b >= 0:
                ship_perimeter.append([offset[0], offset[1]])
    return ship_perimeter


def find_ships(matrix, level=1):
    """Поиск кораблей.

    Параметр level отвечает за поиск кораблей по определенному флагу:
        1 - флаг корабля,
        2 - флаг промаха,
        3 - флаг попадания,
        4 - флаг затонувшего корабля;
    Возвращает список со списками координат всех кораблей.
    """
    length = len(matrix)
    ships = []
    # поиск больших кораблей (от 2-х клеток).
    for big_ship in find_ships_in_column(matrix, level):
        ships.append(big_ship)
    for big_ship in find_ships_in_row(matrix, level):
        ships.append(big_ship)
    # обнуление координат больших кораблей и поиск маленьких (1 клетка).
    small_ship_matrix = deepcopy(matrix)
    for big_ship in ships:
        for coordinate in big_ship:
            small_ship_matrix[coordinate[0]][coordinate[1]] = 0
    for i in range(length):
        for j in range(length):
            if small_ship_matrix[i][j] == level:
                ships.append([[i, j]])
    return ships


def find_ships_in_row(matrix, level=1):
    """Поиск горизонтальных кораблей.

    Параметр level отвечает за поиск кораблей по определенному флагу:
        1 - флаг корабля,
        2 - флаг промаха,
        3 - флаг попадания,
        4 - флаг затонувшего корабля;
    Возвращает список со списками координат вертикальных кораблей.
    """
    # поиск по строкам всех закрашенных клеток.
    length = len(matrix)
    marked_matrix = []
    for i in range(length):
        marked_line = []
        for j in range(length):
            if matrix[i][j] == level:
                marked_line.append([i, j])
        marked_matrix.append(marked_line)
    # поиск кораблей в строке закрашенных клеток.
    ship_matrix = []
    for marked_line in marked_matrix:
        ship_line = []
        length = len(marked_line)
        for i in range(1, length):
            if marked_line[i - 1][1] == marked_line[i][1] - 1:
                ship_line.append(marked_line[i - 1])
            elif i >= 2:
                if marked_line[i - 1][1] == marked_line[i - 2][1] + 1:
                    ship_line.append(marked_line[i - 1])
            if i == length - 1:
                if marked_line[length - 2][1] == marked_line[length - 1][1] - 1:
                    ship_line.append(marked_line[length - 1])
        if ship_line:
            ship_matrix.append(ship_line)
    # деление строки кораблей на отдельные корабли.
    delimiters = []
    for ship_line in ship_matrix:
        length = len(ship_line)
        delimiter_line = []
        for i in range(1, length):
            if ship_line[i - 1][1] < ship_line[i][1] - 1:
                delimiter_line.append(i)
        delimiters.append(delimiter_line)
    flag = None
    for delimiter in delimiters:
        if delimiter:
            flag = True
    if flag:
        ships_in_rows = []
        for ship_line, delimiters_line in enumerate(delimiters):
            if delimiters_line:
                delimiters_amount = len(delimiters_line)
                for i in range(delimiters_amount + 1):
                    if not i:
                        delimiter = delimiters_line[0]
                        ships_in_rows.append(ship_matrix[ship_line][:delimiter])
                    elif i == delimiters_amount:
                        delimiter = delimiters_line[i - 1]
                        ships_in_rows.append(ship_matrix[ship_line][delimiter:])
                    else:
                        delimiter = delimiters_line[i]
                        pr_delimiter = delimiters_line[i - 1]
                        ships_in_rows.append(ship_matrix[ship_line][pr_delimiter:delimiter])
            else:
                ships_in_rows.append(ship_matrix[ship_line])
        return ships_in_rows
    else:
        return ship_matrix


def find_ships_in_column(matrix, level=1):
    """Поиск вертикальных кораблей.

    Параметр level отвечает за поиск кораблей по определенному флагу:
        1 - флаг корабля,
        2 - флаг промаха,
        3 - флаг попадания,
        4 - флаг затонувшего корабля;
    Возвращает список со списками координат вертикальных кораблей.
    """
    # поиск по столбцам всех закрашенных клеток.
    length = len(matrix)
    marked_matrix = []
    for i in range(length):
        marked_column = []
        for j in range(length):
            if matrix[j][i] == level:
                marked_column.append([j, i])
        marked_matrix.append(marked_column)
    # поиск кораблей в строке закрашенных клеток.
    ship_matrix = []
    for marked_line in marked_matrix:
        ship_line = []
        length = len(marked_line)
        for i in range(1, length):
            if marked_line[i - 1][0] == marked_line[i][0] - 1:
                ship_line.append(marked_line[i - 1])
            elif i >= 2:
                if marked_line[i - 1][0] == marked_line[i - 2][0] + 1:
                    ship_line.append(marked_line[i - 1])
            if i == length - 1:
                if marked_line[length - 2][0] == marked_line[length - 1][0] - 1:
                    ship_line.append(marked_line[length - 1])
        if ship_line:
            ship_matrix.append(ship_line)
    # деление строки кораблей на отдельные корабли.
    delimiters = []
    for ship_line in ship_matrix:
        length = len(ship_line)
        delimiter_line = []
        for i in range(1, length):
            if ship_line[i - 1][0] < ship_line[i][0] - 1:
                delimiter_line.append(i)
        delimiters.append(delimiter_line)
    flag = None
    for delimiter in delimiters:
        if delimiter:
            flag = True
    if flag:
        ships_in_columns = []
        for ship_line, delimiters_line in enumerate(delimiters):
            if delimiters_line:
                delimiters = len(delimiters_line)
                for i in range(delimiters + 1):
                    if not i:
                        delimiter = delimiters_line[0]
                        ships_in_columns.append(ship_matrix[ship_line][:delimiter])
                    elif i == delimiters:
                        delimiter = delimiters_line[i - 1]
                        ships_in_columns.append(ship_matrix[ship_line][delimiter:])
                    else:
                        delimiter = delimiters_line[i]
                        pr_delimiter = delimiters_line[i - 1]
                        ships_in_columns.append(ship_matrix[ship_line][pr_delimiter:delimiter])
            else:
                ships_in_columns.append(ship_matrix[ship_line])
        return ships_in_columns
    else:
        return ship_matrix
