from django.test import TestCase
from django.utils import timezone
from sea_battle.models import Game
from sea_battle.funcs import (matrix_to_str,
                              str_to_matrix, )


base_ship_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
base_ships = [
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


class SeaBattleGamePageViewTestCase(TestCase):
    def setUp(self):
        Game.objects.create(
            game_date=timezone.now(),
            player_field=matrix_to_str(base_ship_field),
            enemy_field=matrix_to_str(base_ship_field),
            enemy_field_with_player_moves=matrix_to_str(base_ship_field),
            player_field_with_enemy_moves=matrix_to_str(base_ship_field),
            messages='A1 - Miss!+1|E3 - Miss!+0',
            user_session_key=self.client.session.session_key,
        )

    def test_redirection_when_game_not_started(self):
        """Проверка перенаправления.

        Проверка перенаправления на домашнюю страницу, если нет начатой игры.
        """
        Game.objects.filter(id=1).update(status='Aborted')
        game = Game.objects.filter(status='Started').first()
        self.assertIsNone(game)
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_end_game(self):
        """Проверка выхода из игры.

        Проверка выхода из игры, связанных с этим изменений в базе данных и
        перенаправления на домашнюю страницу.
        """
        game = Game.objects.filter(id=1).first()
        self.assertIsNotNone(game)
        response = self.client.post('/game/', {'end_game': 'end_game'})
        game = Game.objects.filter(status='Started').first()
        self.assertIsNone(game)
        game = Game.objects.filter(status='Aborted').first()
        self.assertIsNotNone(game)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_enemy_move(self):
        """Проверка атаки противника.

        Проверка корректности выполнения кода во время хода противника."""
        expected_field = [
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
        session = self.client.session
        game = Game.objects.get(id=1)
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'player_miss_flag_{user_mark}'] = True
        session[f'player_ships_{user_mark}'] = base_ships
        session.save()
        self.client.post('/game/')
        game = Game.objects.filter(status='Started').first()
        received_player_field = str_to_matrix(game.player_field_with_enemy_moves)
        self.assertIsNotNone(game)
        self.assertTrue(self.client.session[f'player_miss_flag_{user_mark}'])
        self.assertEqual(received_player_field, expected_field)

    def test_enemy_move_and_win(self):
        """Проверка победы противника.

        Проверка корректности выполнения кода во время хода противника,
        в котором он выигрывает игру.
        """
        ship_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [4, 0, 0, 0, 0, 0, 0, 4, 0, 4],
            [0, 2, 3, 3, 3, 1, 0, 4, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 4, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        ]
        ships = [
            [[[6, 5], [7, 5]], [2, 2]],
            [[[3, 7], [4, 7]], [2, 2]],
            [[[2, 9], [3, 9], [4, 9]], [3, 3]],
            [[[1, 3], [1, 4], [1, 5]], [3, 3]],
            [[[4, 2], [4, 3], [4, 4], [4, 5]], [3, 4]],
            [[[7, 2], [7, 3]], [2, 2]],
            [[[3, 0]], [1, 1]],
            [[[6, 0]], [1, 1]],
            [[[8, 9]], [1, 1]],
            [[[9, 4]], [1, 1]],
        ]
        expected_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [4, 2, 2, 2, 2, 2, 2, 4, 0, 4],
            [0, 2, 4, 4, 4, 4, 2, 4, 0, 4],
            [0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
            [4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 4, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        ]
        Game.objects.create(
            game_date=timezone.now(),
            moves=1,
            player_field=matrix_to_str(ship_field),
            enemy_field=matrix_to_str(ship_field),
            enemy_field_with_player_moves=matrix_to_str(ship_field),
            player_field_with_enemy_moves=matrix_to_str(ship_field),
            messages='A1 - Miss!+1|E3 - Miss!+0',
            user_session_key=self.client.session.session_key,
        )
        Game.objects.filter(id=1).update(status='Aborted')
        session = self.client.session
        game = Game.objects.get(id=2)
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'player_miss_flag_{user_mark}'] = True
        session[f'player_ships_{user_mark}'] = ships
        session[f'enemy_ships_{user_mark}'] = None
        session[f'combo_counter_{user_mark}'] = None
        session.save()
        self.client.post('/game/')
        game = Game.objects.filter(status='Lose').first()
        received_player_field = str_to_matrix(game.player_field_with_enemy_moves)
        self.assertIsNotNone(game)
        self.assertEqual(received_player_field, expected_field)

    def test_player_dont_move(self):
        """Проверка корректности выполнения кода, когда игрок не выбрал поле для хода."""
        game = Game.objects.get(id=1)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = base_ships
        session.save()
        self.client.post('/game/')
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        received_enemy_field = str_to_matrix(game.enemy_field_with_player_moves)
        received_moves = game.moves
        received_messages = game.messages
        received_ships = self.client.session[f'enemy_ships_{user_mark}']
        self.assertEqual(received_enemy_field, base_ship_field)
        self.assertEqual(received_moves, 0)
        self.assertEqual(received_messages, 'A1 - Miss!+1|E3 - Miss!+0')
        self.assertEqual(received_ships, base_ships)

    def test_player_move_and_sunk(self):
        """Проверка корректности выполнения кода при затоплении игроком корабля противника."""
        expected_field = [
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
        expected_ships = [
            [[[6, 5], [7, 5]], [0, 2]],
            [[[3, 7], [4, 7]], [0, 2]],
            [[[2, 9], [3, 9], [4, 9]], [0, 3]],
            [[[1, 3], [1, 4], [1, 5]], [0, 3]],
            [[[4, 2], [4, 3], [4, 4], [4, 5]], [0, 4]],
            [[[7, 2], [7, 3]], [2, 2]],
            [[[3, 0]], [0, 1]],
            [[[6, 0]], [0, 1]],
            [[[8, 9]], [0, 1]],
            [[[9, 4]], [0, 1]],
        ]
        game = Game.objects.get(id=1)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = base_ships
        session.save()
        self.client.post('/game/', {'move': ['73']})
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        received_player_field = str_to_matrix(game.enemy_field_with_player_moves)
        received_moves = game.moves
        received_messages = game.messages
        received_ships = self.client.session[f'enemy_ships_{user_mark}']
        self.assertEqual(received_player_field, expected_field)
        self.assertEqual(received_moves, 1)
        self.assertEqual(received_messages, 'A1 - Miss!+1|E3 - Miss!+0|D8 - Sunk!+1')
        self.assertEqual(received_ships, expected_ships)

    def test_player_move_and_miss(self):
        """Проверка корректности выполнения кода при промахе игрока."""
        expected_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 3, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        game = Game.objects.get(id=1)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = base_ships
        session.save()
        self.client.post('/game/', {'move': ['83']})
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        received_player_field = str_to_matrix(game.enemy_field_with_player_moves)
        received_moves = game.moves
        received_messages = game.messages
        self.assertEqual(received_player_field, expected_field)
        self.assertEqual(received_moves, 1)
        self.assertEqual(received_messages, 'A1 - Miss!+1|E3 - Miss!+0|D9 - Miss!+1')
        self.assertTrue(self.client.session[f'player_miss_flag_{user_mark}'])

    def test_player_move_and_hit(self):
        """Проверка корректности выполнения кода при попадании игроком."""
        expected_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 2, 0, 0, 1, 0, 0, 0, 0],
            [0, 2, 3, 1, 0, 3, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]
        expected_ships = [
            [[[6, 5], [7, 5]], [1, 2]],
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
        game = Game.objects.get(id=1)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = base_ships
        session.save()
        self.client.post('/game/', {'move': ['75']})
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        received_player_field = str_to_matrix(game.enemy_field_with_player_moves)
        received_moves = game.moves
        received_messages = game.messages
        received_ships = self.client.session[f'enemy_ships_{user_mark}']
        self.assertEqual(received_player_field, expected_field)
        self.assertEqual(received_moves, 1)
        self.assertEqual(received_messages, 'A1 - Miss!+1|E3 - Miss!+0|F8 - Hit!+1')
        self.assertEqual(received_ships, expected_ships)

    def test_player_move_and_win(self):
        """Проверка победы игрока.

        Проверка корректности выполнения кода во время хода игрока,
        в котором он выигрывает игру.
        """
        ship_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [4, 0, 0, 0, 0, 0, 0, 4, 0, 4],
            [0, 2, 3, 3, 3, 1, 0, 4, 0, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 4, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        ]
        ships = [
            [[[6, 5], [7, 5]], [2, 2]],
            [[[3, 7], [4, 7]], [2, 2]],
            [[[2, 9], [3, 9], [4, 9]], [3, 3]],
            [[[1, 3], [1, 4], [1, 5]], [3, 3]],
            [[[4, 2], [4, 3], [4, 4], [4, 5]], [3, 4]],
            [[[7, 2], [7, 3]], [2, 2]],
            [[[3, 0]], [1, 1]],
            [[[6, 0]], [1, 1]],
            [[[8, 9]], [1, 1]],
            [[[9, 4]], [1, 1]],
        ]
        expected_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [4, 2, 2, 2, 2, 2, 2, 4, 0, 4],
            [0, 2, 4, 4, 4, 4, 2, 4, 0, 4],
            [0, 2, 2, 2, 2, 2, 2, 0, 0, 0],
            [4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 0, 4, 4, 0, 4, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
            [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        ]
        Game.objects.create(
            game_date=timezone.now(),
            player_field=matrix_to_str(ship_field),
            enemy_field=matrix_to_str(ship_field),
            enemy_field_with_player_moves=matrix_to_str(ship_field),
            player_field_with_enemy_moves=matrix_to_str(ship_field),
            messages='',
            user_session_key=self.client.session.session_key,
        )
        Game.objects.filter(id=1).update(status='Aborted')
        game = Game.objects.get(id=2)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = ships
        session[f'player_ships_{user_mark}'] = None
        session[f'player_miss_flag_{user_mark}'] = None
        session.save()
        self.client.post('/game/', {'move': ['45']})
        game = Game.objects.filter(status='Win').first()
        self.assertIsNotNone(game)
        received_enemy_field = str_to_matrix(game.enemy_field_with_player_moves)
        received_moves = game.moves
        received_messages = game.messages
        self.assertEqual(received_enemy_field, expected_field)
        self.assertEqual(received_moves, 1)
        self.assertEqual(received_messages, 'F5 - Sunk!+1')

    def test_player_move_combo(self):
        """Проверка подсчета комбо.

        Проверка корректности начисления дополнительных очков за попадания подряд.
        """
        game = Game.objects.get(id=1)
        session = self.client.session
        username = f'Guest_{str(game.id).rjust(6, "0")}'
        user_mark = f'{session.session_key}_{username}'
        session[f'enemy_ships_{user_mark}'] = base_ships
        session.save()
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        self.assertEqual(game.points, 0)
        self.client.post('/game/', {'move': ['13']})
        game = Game.objects.filter(status='Started').first()
        self.assertEqual(game.points, 0)
        self.client.post('/game/', {'move': ['14']})
        game = Game.objects.filter(status='Started').first()
        self.assertEqual(game.points, 5)
        self.client.post('/game/', {'move': ['15']})
        game = Game.objects.filter(status='Started').first()
        self.assertEqual(game.points, 15)
        self.client.post('/game/', {'move': ['30']})
        game = Game.objects.filter(status='Started').first()
        self.assertEqual(game.points, 30)
        self.client.post('/game/', {'move': ['00']})
        game = Game.objects.filter(status='Started').first()
        self.assertEqual(game.points, 30)
