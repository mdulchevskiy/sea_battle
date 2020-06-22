from django.test import TestCase
from django.utils import timezone
from sea_battle.models import Game
from sea_battle.funcs.converting import (get_leaderboard,
                                         phone_number_formatting,
                                         prepare_ships,
                                         read_player_ship_field,
                                         matrix_to_str,
                                         str_to_matrix, )


normal_field = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class SeaBattleConvertingFuncsTestCase(TestCase):
    def setUp(self):
        for i in range(7, 1, -1):
            Game.objects.create(
                status='Win',
                game_date=timezone.now(),
                moves=i*10,
                points=i*10,
                player_field=normal_field,
                enemy_field=normal_field,
                enemy_field_with_player_moves=normal_field,
                player_field_with_enemy_moves=normal_field,
                messages='no message',
            )

    def test_get_leaderboard(self):
        """Проверка формирования таблицы лидеров (топ-5)."""
        win_games = Game.objects.filter(status='Win')
        top = get_leaderboard(win_games)
        self.assertEqual(top[0].rank, 1)
        self.assertEqual(top[0].username, 'Guest_000001')
        self.assertEqual(top[0].points, 70)
        self.assertEqual(top[-1].rank, 5)
        self.assertEqual(top[-1].username, 'Guest_000005')
        self.assertEqual(top[-1].points, 30)

    def test_read_player_ship_field(self):
        """Проверка считывания кораблей, которые ввел игрок."""
        data = {
            '09': ['1'], '13': ['1'], '14': ['1'], '20': ['1'], '26': ['1'],
            '36': ['1'], '40': ['1'], '44': ['1'], '46': ['1'], '50': ['1'],
            '54': ['1'], '56': ['1'], '58': ['1'], '60': ['1'], '62': ['1'],
            '64': ['1'], '79': ['1'], '81': ['1'], '82': ['1'], '89': ['1'],
        }
        expected_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        expected_checkboxes_names = [
            [['00', '0'], ['01', '0'], ['02', '0'], ['03', '0'], ['04', '0'],
             ['05', '0'], ['06', '0'], ['07', '0'], ['08', '0'], ['09', '1']],
            [['10', '0'], ['11', '0'], ['12', '0'], ['13', '1'], ['14', '1'],
             ['15', '0'], ['16', '0'], ['17', '0'], ['18', '0'], ['19', '0']],
            [['20', '1'], ['21', '0'], ['22', '0'], ['23', '0'], ['24', '0'],
             ['25', '0'], ['26', '1'], ['27', '0'], ['28', '0'], ['29', '0']],
            [['30', '0'], ['31', '0'], ['32', '0'], ['33', '0'], ['34', '0'],
             ['35', '0'], ['36', '1'], ['37', '0'], ['38', '0'], ['39', '0']],
            [['40', '1'], ['41', '0'], ['42', '0'], ['43', '0'], ['44', '1'],
             ['45', '0'], ['46', '1'], ['47', '0'], ['48', '0'], ['49', '0']],
            [['50', '1'], ['51', '0'], ['52', '0'], ['53', '0'], ['54', '1'],
             ['55', '0'], ['56', '1'], ['57', '0'], ['58', '1'], ['59', '0']],
            [['60', '1'], ['61', '0'], ['62', '1'], ['63', '0'], ['64', '1'],
             ['65', '0'], ['66', '0'], ['67', '0'], ['68', '0'], ['69', '0']],
            [['70', '0'], ['71', '0'], ['72', '0'], ['73', '0'], ['74', '0'],
             ['75', '0'], ['76', '0'], ['77', '0'], ['78', '0'], ['79', '1']],
            [['80', '0'], ['81', '1'], ['82', '1'], ['83', '0'], ['84', '0'],
             ['85', '0'], ['86', '0'], ['87', '0'], ['88', '0'], ['89', '1']],
            [['90', '0'], ['91', '0'], ['92', '0'], ['93', '0'], ['94', '0'],
             ['95', '0'], ['96', '0'], ['97', '0'], ['98', '0'], ['99', '0']],
        ]
        received_field, received_checkboxes_names = read_player_ship_field(data)
        self.assertEqual(received_field, expected_field)
        self.assertEqual(received_checkboxes_names, expected_checkboxes_names)

    def test_matrix_to_str(self):
        """Проверка конвертации матрицы кораблей в строку кораблей."""
        matrix = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]
        expected_string_matrix = '0000100000|0100100001|0000000001|1000001001|1000000000|' \
                                 '0001110000|0000000110|0000010000|1111000000|0000001000'
        received_string_matrix = matrix_to_str(matrix)
        self.assertEqual(received_string_matrix, expected_string_matrix)

    def test_str_to_matrix(self):
        """Проверка конвертации строки кораблей в матрицу кораблей."""
        string_matrix = '0000100000|0100100001|0000000001|1000001001|1000000000|' \
                        '0001110000|0000000110|0000010000|1111000000|0000001000'
        expected_matrix = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]
        received_matrix = str_to_matrix(string_matrix)
        self.assertEqual(received_matrix, expected_matrix)

    def test_matrix_to_str_with_option(self):
        """Проверка конвертации матрицы уведомлений в строку уведомлений."""
        expected_string_matrix = 'A1 - Miss!+1|E3 - Miss!+0|B2 - Miss!+1'
        matrix = [
            ['A1 - Miss!', '1'],
            ['E3 - Miss!', '0'],
            ['B2 - Miss!', '1'],
        ]
        received_string_matrix = matrix_to_str(matrix, option=True)
        self.assertEqual(received_string_matrix, expected_string_matrix)

    def test_str_to_matrix_with_option(self):
        """Проверка конвертации строки уведомлений в матрицу уведомлений."""
        string_matrix = 'A1 - Miss!+1|E3 - Miss!+0|B2 - Miss!+1'
        expected_matrix = [
            ['A1 - Miss!', '1'],
            ['E3 - Miss!', '0'],
            ['B2 - Miss!', '1'],
        ]
        received_matrix = str_to_matrix(string_matrix, option=True)
        self.assertEqual(received_matrix, expected_matrix)

    def test_phone_number_formatting(self):
        """Проверка форматирования номеров."""
        test_phone_number_1 = '+375(29)111-11-11'
        test_phone_number_2 = '+375(29)1111111'
        test_phone_number_3 = '+375291111111'
        test_phone_number_4 = '8(029)111-11-11'
        test_phone_number_5 = '8(029)1111111'
        test_phone_number_6 = '8(029)111-11-11'
        test_phone_number_7 = '80291111111'
        test_phone_number_8 = '823424214124'
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_1))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_2))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_3))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_4))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_5))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_6))
        self.assertEqual(test_phone_number_1, phone_number_formatting(test_phone_number_7))
        self.assertEqual(test_phone_number_8, phone_number_formatting(test_phone_number_8))

    def test_prepare_ships(self):
        """Проверка работы функции для доп. представления кораблей."""
        ship_field = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        ]
        expected_prepared_ships = [
            [[[3, 0], [4, 0]], [0, 2]],
            [[[0, 4], [1, 4]], [0, 2]],
            [[[1, 9], [2, 9], [3, 9]], [0, 3]],
            [[[5, 3], [5, 4], [5, 5]], [0, 3]],
            [[[6, 7], [6, 8]], [0, 2]],
            [[[8, 0], [8, 1], [8, 2], [8, 3]], [0, 4]],
            [[[1, 1]], [0, 1]],
            [[[3, 6]], [0, 1]],
            [[[7, 5]], [0, 1]],
            [[[9, 6]], [0, 1]],
        ]
        received_prepared_ships = prepare_ships(ship_field)
        self.assertEqual(received_prepared_ships, expected_prepared_ships)
