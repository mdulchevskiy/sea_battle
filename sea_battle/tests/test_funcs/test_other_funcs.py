import pytz
from django.conf import settings
from django.utils import timezone
from django.test import (TestCase,
                         override_settings, )
from sea_battle.models import (Game,
                               User, )
from datetime import (datetime,
                      timedelta, )
from sea_battle.funcs.converting import read_player_ship_field
from sea_battle.funcs.other_funcs import (get_rand_ship_field,
                                          get_game_data,
                                          get_signed_user,
                                          sign_out_of_all_inactive_accounts, )


class SeaBattleOtherFuncsTestCase(TestCase):
    def setUp(self):
        dates = [
            datetime(2020, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)),
            datetime(2020, 5, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)),
            timezone.now() - timedelta(minutes=40),
        ]
        for i, date in enumerate(dates):
            User.objects.create(
                username=f'maxi{"m" * i}',
                password='1111111111',
                first_name='Maxim',
                last_name='Dulchevskiy',
                email=f'maxi{"m" * i}@gmail.com',
                phone_number='80291111111',
                session_key='session_key',
                login=1,
                last_activity_date=date,
            )
        Game.objects.create(
            status='Started',
            user_session_key='session_key',
        )
        Game.objects.create(
            user_type='User',
            user=User.objects.get(id=3),
            status='Started',
        )

    @override_settings(MAX_IDLE_TIME=3600)
    def test_sign_out_all_inactive_accounts(self):
        """Проверка работы функции автоматического выхода из неактивных аккаунтов."""
        sign_in_users = User.objects.filter(login=1)
        self.assertEqual(len(sign_in_users), 3)
        sign_out_of_all_inactive_accounts()
        sign_in_users = User.objects.filter(login=1)
        self.assertEqual(len(sign_in_users), 1)
        self.assertEqual(sign_in_users.first().id, 3)

    @override_settings(MAX_IDLE_TIME=3600)
    def test_get_signed_user(self):
        """Проверка получения авторезированного пользователя и обновления даты его последней активности."""
        last_activity_date = User.objects.get(id=3).last_activity_date
        sign_out_of_all_inactive_accounts()
        signed_user_object = get_signed_user('session_key')
        new_activity_date = User.objects.get(id=3).last_activity_date
        self.assertIsNotNone(signed_user_object)
        self.assertEqual(signed_user_object.first().id, 3)
        self.assertNotEqual(last_activity_date, new_activity_date)

    @override_settings(MAX_IDLE_TIME=3600)
    def test_get_game_data_user_case(self):
        """Проверка получения пользователя и начатой игры.

        Случай, когда пользователь авторезирован.
        """
        sign_out_of_all_inactive_accounts()
        signed_user, game_object = get_game_data('session_key')
        self.assertIsNotNone(signed_user)
        self.assertEqual(signed_user.id, 3)
        self.assertIsNotNone(game_object)
        self.assertEqual(game_object.first().user.id, 3)

    def test_get_game_data_guest_case(self):
        """Проверка получения пользователя и начатой игры.

        Случай, когда пользователь играет как гость.
        """
        sign_out_of_all_inactive_accounts()
        signed_user, game_object = get_game_data('session_key')
        self.assertIsNone(signed_user)
        self.assertIsNotNone(game_object)
        self.assertEqual(game_object.first().user_type, 'Guest')
        self.assertEqual(game_object.first().id, 1)

    def test_get_rand_ship_field(self):
        """Проверка корректности возвращаемых значений функции случайной расстановки кораблей."""
        received_field, received_checkboxes_names = get_rand_ship_field()
        data = {}
        for i in range(10):
            for j in range(10):
                if received_field[i][j]:
                    data.update({f'{i}{j}': ['1']})
        expected_field, expected_checkboxes_names = read_player_ship_field(data)
        self.assertEqual(received_checkboxes_names, expected_checkboxes_names)
        self.assertEqual(received_field, expected_field)
