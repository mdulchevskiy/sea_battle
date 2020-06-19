from django.test import TestCase
from sea_battle.funcs import enemy_attack


class Request:
    def __init__(self, session):
        self.session = session


message = [['A1 - Miss!', '1']]
title = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
request = Request(session={'player_ships': None})


class SeaBattleEnemyAttackTestCase(TestCase):
    """Проверка корректности атаки противника. Ч.1

    Проверка корректности вариантов атаки противника с учетом ранения
    двухпалубного корабля, некасающегося границ поля.
    """
    def test_shot_in_hit_two_decker_far_from_border(self):
        number = None
        player_ship_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        player_ships = [
            [[[6, 5], [7, 5]], [0, 2]],
            [[[3, 7], [4, 7]], [0, 2]],
            [[[2, 9], [3, 9], [4, 9]], [0, 3]],
            [[[1, 3], [1, 4], [1, 5]], [0, 3]],
            [[[4, 2], [4, 3], [4, 4], [4, 5]], [0, 4]],
            [[[7, 2], [7, 3]], [1, 2]],
            [[[3, 0]], [0, 1]],
            [[[6, 0]], [0, 1]],
            [[[8, 9]], [0, 1]],
            [[[9, 4]], [0, 1]],
        ]
        expected_ship_field_1 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_field_2 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_field_3 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 2, 2, 2, 2, 1, 0, 0, 0, 0],
            [0, 2, 4, 4, 2, 1, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_field_4 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_fields = [
            expected_ship_field_1, expected_ship_field_2,
            expected_ship_field_3, expected_ship_field_4,
        ]
        expected_messages = [
            [['A1 - Miss!', '1'], ['C7 - Miss!', '0']],
            [['A1 - Miss!', '1'], ['C9 - Miss!', '0']],
            [['A1 - Miss!', '1'], ['D8 - Sunk!', '0']],
            [['A1 - Miss!', '1'], ['B8 - Miss!', '0']],
        ]
        expected_miss_flags = [False, False, True, False]
        received_ship_field, received_message, received_miss_flag = enemy_attack(
            request, player_ship_field, player_ships, message, title, None)
        self.assertIn(received_ship_field, expected_ship_fields)
        for i, expected_ship_field in enumerate(expected_ship_fields):
            if received_ship_field == expected_ship_field:
                number = i
        self.assertEqual(received_message, expected_messages[number])
        self.assertEqual(received_miss_flag, expected_miss_flags[number])

    def test_shot_in_hit_three_decker_near_from_border(self):
        """Проверка корректности атаки противника. Ч.2

        Проверка корректности вариантов атаки противника с учетом ранения
        трехпалубного корабля, касающегося границ поля.
        """
        number = None
        player_ship_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        player_ships = [
            [[[6, 5], [7, 5]], [0, 2]],
            [[[3, 7], [4, 7]], [0, 2]],
            [[[2, 9], [3, 9], [4, 9]], [1, 3]],
            [[[1, 3], [1, 4], [1, 5]], [0, 3]],
            [[[4, 2], [4, 3], [4, 4], [4, 5]], [0, 4]],
            [[[7, 2], [7, 3]], [0, 2]],
            [[[3, 0]], [0, 1]],
            [[[6, 0]], [0, 1]],
            [[[8, 9]], [0, 1]],
            [[[9, 4]], [0, 1]],
        ]
        expected_ship_field_1 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_field_2 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 3],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_field_3 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 3],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ship_fields = [expected_ship_field_1, expected_ship_field_2, expected_ship_field_3]
        expected_messages = [
            [['A1 - Miss!', '1'], ['J2 - Miss!', '0']],
            [['A1 - Miss!', '1'], ['J4 - Hit!', '0']],
            [['A1 - Miss!', '1'], ['I3 - Miss!', '0']],
        ]
        expected_miss_flags = [False, True, False]
        received_ship_field, received_message, received_miss_flag = enemy_attack(
            request, player_ship_field, player_ships, message, title, None)
        self.assertIn(received_ship_field, expected_ship_fields)
        for i, expected_ship_field in enumerate(expected_ship_fields):
            if received_ship_field == expected_ship_field:
                number = i
        self.assertEqual(received_message, expected_messages[number])
        self.assertEqual(received_miss_flag, expected_miss_flags[number])
