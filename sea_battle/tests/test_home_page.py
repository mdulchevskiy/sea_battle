from django.test import TestCase
from django.utils import timezone
from sea_battle.models import (Game,
                               User, )


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


class SeaBattleHomePageViewTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='mbellrat',
            password='1234567890',
            first_name='Micah',
            last_name='Bell',
            email='mbellrat@gmail.com',
            phone_number='80291111111',
            login=1,
            session_key=self.client.session.session_key,
        )
        Game.objects.create(
            game_date=timezone.now(),
            user=User.objects.get(id=1),
            player_field=normal_field,
            enemy_field=normal_field,
            enemy_field_with_player_moves=normal_field,
            player_field_with_enemy_moves=normal_field,
            messages='no message',
        )
        Game.objects.create(
            game_date=timezone.now(),
            status='Win',
            player_field=normal_field,
            enemy_field=normal_field,
            enemy_field_with_player_moves=normal_field,
            player_field_with_enemy_moves=normal_field,
            messages='no message',
        )

    def test_post_sign_out(self):
        """Проверка пост запроса. Ч.1

        Проверка выхода пользователя и перенаправления на страницу,
        с которой был совершен выход.
        """
        user = User.objects.get(username='mbellrat')
        self.assertEqual(user.login, 1)
        response = self.client.post('/', {'sign_out': '1'}, HTTP_REFERER='/preparation/')
        user = User.objects.get(username='mbellrat')
        self.assertEqual(user.login, 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/preparation/')

    def test_post_new_game(self):
        """Проверка пост запроса. Ч.2

        Проверка старта новой игры и перенаправления на страницу подготовки.
        """
        game = Game.objects.get(id=1)
        self.assertEqual(game.status, 'Started')
        response = self.client.post('/', {'continue_game': 'new_game'})
        game = Game.objects.get(id=1)
        self.assertEqual(game.status, 'Aborted')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/preparation/')

    def test_post_continue_game(self):
        """Проверка пост запроса. Ч.3

        Проверка продолжения ранее начатой игры и перенаправления на страницу игры.
        """
        game = Game.objects.get(id=1)
        self.assertEqual(game.status, 'Started')
        response = self.client.post('/', {'continue_game': 'continue'})
        game = Game.objects.get(id=1)
        self.assertEqual(game.status, 'Started')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/game/')

    def test_rendering_basic_elements(self):
        """Проверка отображения основных элементов шаблона."""
        response = self.client.get('/')
        check_1 = b'Rank' in response.content
        check_2 = b'Username' in response.content
        check_3 = b'Points' in response.content
        check_4 = b'mbellrat' in response.content
        check = check_1 and check_2 and check_3 and check_4
        self.assertTrue(check)
