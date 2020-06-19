from random import choice
from string import ascii_uppercase as ltr
from sea_battle.funcs.searching import (find_ships,
                                        get_ship_perimeter, )


def is_move_possible(move, possible_moves):
    """Проверка возможности хода."""
    for row in possible_moves:
        for possible_move in row:
            if move == possible_move:
                return True


def enemy_attack(request, player_ship_field, player_ships, message, title, user_mark):
    """Функция генерирующая ход противника.

    Возвращает:
        поле игрока вида [[0, 2, 0, 1, 0, 3, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0, 1, 0, 1], ...], где
            '1' - координата корабля,
            '2' - координата промаха,
            '3' - координата попадания,
            '4' - координата затонувшего корабля;
        список сообщений вида [['A10 - Miss!', '1'], ['H9 - Miss!', '0'], ...], где
            'A10 - Miss!' - координтаы и статус выстрела,
            '0' - код хода противника;
        флаг промаха/попадания противника.
    """
    updated_message = message[:]
    # генерация матрицы возможных ходов.
    possible_moves = [[[row, col] for col in range(10)] for row in range(10)]
    # поиск уже совершенных ходов и исключение их из матрицы возможных ходов.
    used_moves = []
    for i, row in enumerate(player_ship_field):
        for j, elem in enumerate(row):
            if elem == 2 or elem == 3 or elem == 4:
                used_moves.append([i, j])
    for used_move in used_moves:
        possible_moves[used_move[0]][used_move[1]] = None
    # поиск раненого корабля.
    hit_ship = find_ships(player_ship_field, 3)
    # если на поле есть раненый корабль, следующий ход будет нацелен на раненый корабль.
    if hit_ship:
        hit_ship = hit_ship[0]
        hits_amount = len(hit_ship)
        if hits_amount == 1:
            # если у корабля одно ранение, то координата следующего хода выбирается случайным образом по
            # горизонтальной и вертикальной оси относительно попадания. Происходит проверка, что координата
            # не вышла за пределы ОДЗ.
            tag = False
            while not tag:
                i = choice([1, 0, -1])
                j = 0 if i else choice([1, 0, -1])
                move = [hit_ship[0][0] + i, hit_ship[0][1] + j]
                if 0 <= move[0] <= 9 and 0 <= move[1] <= 9:
                    tag = is_move_possible(move, possible_moves)
        # если у корабля несколько ранений, то определяется ориентация корабля путем сравнения соседних
        # координат ранений, на основе которой находятся координаты следующего хода.
        else:
            tag = False
            while not tag:
                # горизонтальная ориентация.
                if hit_ship[0][0] == hit_ship[1][0]:
                    # определение крайних индексов относительно ранений.
                    left = hit_ship[0][1] - 1
                    right = hit_ship[-1][1] + 1
                    # определение индексов координаты следующего хода.
                    if 0 <= left <= 9:
                        j = choice([left, right]) if 0 <= right <= 9 else left
                    else:
                        j = right
                    i = hit_ship[0][0]
                # вертикальная ориентация.
                else:
                    # определение крайних индексов относительно ранений.
                    top = hit_ship[0][0]-1
                    bottom = hit_ship[-1][0]+1
                    # определение индексов координаты следующего хода.
                    if 0 <= top <= 9:
                        i = choice([top, bottom]) if 0 <= bottom <= 9 else top
                    else:
                        i = bottom
                    j = hit_ship[0][1]
                # координата следующего хода.
                move = [i, j]
                tag = is_move_possible(move, possible_moves)
    # если на поле нет раненых кораблей, следующий ход будет выбран случайным образом из матрицы возможных ходов.
    else:
        while True:
            move = choice(choice(possible_moves))
            if move:
                break
    # проверка попадания. При попадании противник ходит еще раз пока не промажет.
    for i, ship_info in enumerate(player_ships):
        ship = ship_info[0]
        # если было попадание.
        if move in ship:
            player_ship_field[move[0]][move[1]] = 3
            hit_count = player_ships[i][1][0] + 1
            ship_size = player_ships[i][1][1]
            # проверка потопления корабля после попадания.
            if hit_count == ship_size:
                # если корабль потоплен, то он отмечается соответствующим образом, а также исключается его
                # периметр из возможных ходов.
                for coordinate in ship:
                    player_ship_field[coordinate[0]][coordinate[1]] = 4
                ship_perimeter = get_ship_perimeter(ship)
                for coordinate in ship_perimeter:
                    player_ship_field[coordinate[0]][coordinate[1]] = 2
                updated_message.append([f'{ltr[move[1]]}{title[move[0]]} - Sunk!', '0'])
            else:
                # корабль ранен, но не потоплен
                updated_message.append([f'{ltr[move[1]]}{title[move[0]]} - Hit!', '0'])
            player_ships[i][1][0] = hit_count
            request.session[f'player_ships_{user_mark}'] = player_ships
            miss_flag = True
            break
    # если не было попадания (цикл не прерван), то ход отмечается соответствующим образом, а также на этом ход
    # противника заканчивается (реализовано через miss_flag).
    else:
        player_ship_field[move[0]][move[1]] = 2
        updated_message.append([f'{ltr[move[1]]}{title[move[0]]} - Miss!', '0'])
        miss_flag = False
    possible_moves[move[0]][move[1]] = None
    return player_ship_field, updated_message, miss_flag
