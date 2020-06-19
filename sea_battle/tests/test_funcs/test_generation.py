from django.test import TestCase
from sea_battle.funcs import ship_field_validation
from sea_battle.funcs.generation import (generate_buttons_names,
                                         generate_empty_matrix,
                                         generate_rand_ship_field, )


class SeaBattleGenerationFuncsTestCase(TestCase):
    def test_generate_empty_matrix(self):
        """Проверка корректной генерации пустой матрицы."""
        received_empty_matrix = generate_empty_matrix(3)
        expected_empty_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertEqual(received_empty_matrix, expected_empty_matrix)

    def test_get_buttons_names(self):
        """Проверка корректной генерации матрицы имен для радио баттонов."""
        received_buttons_names = generate_buttons_names()
        received_first_row = received_buttons_names[0]
        received_last_row = received_buttons_names[-1]
        expected_first_row = [
            ['00', '0'], ['01', '0'], ['02', '0'], ['03', '0'], ['04', '0'],
            ['05', '0'], ['06', '0'], ['07', '0'], ['08', '0'], ['09', '0']
        ]
        expected_last_row = [
            ['90', '0'], ['91', '0'], ['92', '0'], ['93', '0'], ['94', '0'],
            ['95', '0'], ['96', '0'], ['97', '0'], ['98', '0'], ['99', '0']
        ]
        self.assertEqual(received_first_row, expected_first_row)
        self.assertEqual(received_last_row, expected_last_row)

    def test_rand_ship_field(self):
        """Проверка корректности генерации случайного расположения кораблей."""
        random_field = generate_rand_ship_field()
        self.assertFalse(ship_field_validation(random_field))
