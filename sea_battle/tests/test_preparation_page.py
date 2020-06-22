from django.test import TestCase
from django.utils import timezone
from sea_battle.models import Game


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


class SeaBattlePreparationPageViewTestCase(TestCase):
    def test_redirection_when_game_already_started(self):
        """Проверка перенаправления.

        Проверка перенаправления на страницу игры, когда игра уже начата.
        """
        Game.objects.create(
            game_date=timezone.now(),
            player_field=normal_field,
            enemy_field=normal_field,
            enemy_field_with_player_moves=normal_field,
            player_field_with_enemy_moves=normal_field,
            messages='no message',
            user_session_key=self.client.session.session_key,
        )
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        response = self.client.get('/preparation/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/game/')

    def test_stay_at_preparation_when_field_incorrect(self):
        """Проверка заполнения поля.

        Проверка корректного поведения при передаче неправильно заполненного поля игрока.
        """
        data = {
            '01': ['1'], '08': ['1'], '14': ['1'], '15': ['1'], '31': ['1'],
            '32': ['1'], '33': ['1'], '36': ['1'], '37': ['1'], '61': ['1'],
            '63': ['1'], '64': ['1'], '65': ['1'], '66': ['1'], '82': ['1'],
            '83': ['1'], '84': ['1'], '87': ['1'], '90': ['1'],
        }
        response = self.client.post('/preparation/', data)
        check = b'Cells marked incorrectly.'
        self.assertTrue(check in response.content)
        game = Game.objects.filter(status='Started').first()
        self.assertIsNone(game)

    def test_create_game(self):
        """Проверка создания игры."""
        data = {
            '01': ['1'], '08': ['1'], '14': ['1'], '15': ['1'], '31': ['1'],
            '32': ['1'], '33': ['1'], '36': ['1'], '37': ['1'], '61': ['1'],
            '63': ['1'], '64': ['1'], '65': ['1'], '66': ['1'], '82': ['1'],
            '83': ['1'], '84': ['1'], '87': ['1'], '90': ['1'], '80': ['1'],
        }
        response = self.client.post('/preparation/', data)
        game = Game.objects.filter(status='Started').first()
        self.assertIsNotNone(game)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/game/')
