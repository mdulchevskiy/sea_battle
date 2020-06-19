import re
from django.conf import settings
from sea_battle.funcs.classes import WinGame
from sea_battle.funcs.generation import (generate_buttons_names,
                                         generate_empty_matrix, )
from sea_battle.funcs.searching import find_ships


def get_leaderboard(win_games):
    """Формирует таблицу лидеров.

    Получает на вход выборку из всех победных игр и формирует топ пять игроков по очкам.
    Возвращает список объектов класса WinGame.
    """
    win_games = list(map(lambda x: WinGame(x), win_games))
    best_games = {}
    for win_game in win_games:
        username = win_game.username
        score = best_games.get(username)
        if not score or score.points < win_game.points:
            best_games.update({username: win_game})
    best_games = list(best_games.values())
    leaderboard = sorted(best_games[:5], key=lambda x: x.points, reverse=True)
    for rank, game in enumerate(leaderboard):
        game.set_rank(rank + 1)
    return leaderboard


def read_player_ship_field(data):
    """Считывает игровое поле игрока.

    На основании нажатий чекбоксов, формирует поле игрока и соответствующую ему матрицу имен и статусов чекбоксов.
    Возвращает:
        поле игрока вида [[0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1], ...], где
            '1' - координата корабля;
        матрицу имен чекбоксов вида [['01', '0']], где
            '01' - имя чекбокса состоящее из номера строки и столбца чекбокса,
            '0' - статус чекбокса (было нажатие или нет).
    """
    player_ship_field = generate_empty_matrix(10)
    checkboxes_names = generate_buttons_names()
    for key, value in data.items():
        if key != 'csrfmiddlewaretoken':
            row = int(key[-2])
            column = int(key[-1])
            player_ship_field[row][column] = 1
            checkboxes_names[row][column][1] = value[0]
    return player_ship_field, checkboxes_names


def matrix_to_str(matrix, option=0):
    """Конвертация матрицы в строку.

    Конвертирует матрицу в строку для записи в текстовое поле базы данных.
    Применяется для конвертации игрового поля (option = 0) и сообщений о ходах (option = True).
    Возвращает строку вида '0100000001|0100000001|0000011100...'.
    """
    string_matrix = ''
    if option:
        for line in matrix:
            for elem in line:
                string_matrix += f'{str(elem)}+'
            string_matrix = string_matrix[:-1]
            string_matrix += '|'
    else:
        for line in matrix:
            for elem in line:
                string_matrix += str(elem)
            string_matrix += '|'
    string_matrix = string_matrix[:-1]
    return string_matrix


def str_to_matrix(string_matrix, option=0):
    """Конвертация строки в матрицу.

    Конвертирует строковое представление матрицы из базы данных в список (матрицу).
    Применяется для конвертации игрового поля (option = 0) и сообщений о ходах (option = True).
    Возвращает список вида [[0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1], ...].
    """
    if option:
        matrix = list(map(lambda x: x.split('+'), string_matrix.split('|')))
    else:
        matrix = list(map(lambda x: list(x), string_matrix.split('|')))
        matrix = [[int(elem) for elem in line] for line in matrix]
    return matrix


def phone_number_formatting(phone_number):
    """Форматирование номера телефона.

    В случае если введенный номер допустимого формата, приводит его к формату '+375(xx)xxx-xx-xx'.
    """
    patterns = settings.PHONE_NUMBER_PATTERNS
    for pattern in patterns:
        match = re.fullmatch(pattern, phone_number)
        if match:
            phone_raw = phone_number.replace('-', '').replace('(', '').replace(')', '')
            phone_number = f'+375({phone_raw[-9:-7]}){phone_raw[-7:-4]}-{phone_raw[-4:-2]}-{phone_raw[-2:]}'
            break
    return phone_number


def prepare_ships(ship_field):
    """Функция для доп. представления кораблей.

    Вспомогательная функция. Добавляет к координатам корабля информацию о его ранениях и размере.
    """
    hits = 0
    ships = find_ships(ship_field)
    prepared_ships = []
    for ship in ships:
        size = len(ship)
        prepared_ships.append([ship, [hits, size]])
    return prepared_ships


def enemy_ships_left(enemy_ship_field):
    """Возвращает количество оставшихся кораблей противника."""
    ships_amount = {4: 1, 3: 2, 2: 3, 1: 4, 'total': 10}
    enemy_ships = find_ships(enemy_ship_field, 4)
    for enemy_ship in enemy_ships:
        ship_size = len(enemy_ship)
        ships_amount[ship_size] = ships_amount.get(ship_size) - 1
        ships_amount['total'] = ships_amount.get('total') - 1
    return ships_amount
