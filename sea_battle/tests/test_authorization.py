from django.test import TestCase
from sea_battle.models import User


class SeaBattleAuthorizationViewTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='mdulchevskiy',
            password='1111111111',
            first_name='Maxim',
            last_name='Dulchevskiy',
            email='mdulchevskiy@gmail.com',
            phone_number='80291111111',
            session_key='session_key'
        )
        User.objects.create(
            username='amorgan',
            password='1111111111',
            first_name='Arthur',
            last_name='Morgan',
            email='amorgan@gmail.com',
            phone_number='80291111111',
            session_key=self.client.session.session_key,
        )

    def test_post_sign_in(self):
        """Проверка авторизации пользователя."""
        user = User.objects.filter(id=1).first()
        self.assertEqual(user.login, 0)
        self.client.post('/sign_in/', {
            'username': 'mdulchevskiy',
            'password': '1111111111',
        })
        user = User.objects.filter(id=1).first()
        self.assertEqual(user.login, 1)

    def test_post_sign_in_and_switch_session_ip(self):
        """Проверка изменения "session_key" в сессиях пользователя.

        Проверка изменения названий сессий ("session_key" в "user_mark") при смене браузера игрока
        (создание сессий с новыми именами и удаление старых).
        """
        user_object = User.objects.filter(id=1)
        user = user_object.first()
        self.assertEqual(user.login, 0)
        session = self.client.session
        old_user_mark = f'{user.session_key}_{user.username}'
        session[f'enemy_ships_{old_user_mark}'] = 'enemy_ships'
        session[f'player_ships_{old_user_mark}'] = 'player_ships'
        session[f'player_miss_flag_{old_user_mark}'] = 'miss_flag'
        session.save()
        self.client.post('/sign_in/', {
            'username': 'mdulchevskiy',
            'password': '1111111111',
        })
        session_key = session.session_key
        new_user_mark = f'{session_key}_{user.username}'
        user_object = User.objects.filter(id=1)
        user = user_object.first()
        self.assertEqual(user.login, 1)
        enemy_ships = self.client.session[f'enemy_ships_{new_user_mark}']
        player_ships = self.client.session[f'player_ships_{new_user_mark}']
        player_miss_flag = self.client.session[f'player_miss_flag_{new_user_mark}']
        self.assertEqual(enemy_ships, 'enemy_ships')
        self.assertEqual(player_ships, 'player_ships')
        self.assertEqual(player_miss_flag, 'miss_flag')
        self.assertIsNone(self.client.session.get('enemy_ships_session_key_mdulchevskiy'))
        self.assertIsNone(self.client.session.get('player_ships_session_key_mdulchevskiy'))
        self.assertIsNone(self.client.session.get('player_miss_flag_session_key_mdulchevskiy'))

    def test_get_sign_in_with_referer(self):
        """Проверка перенаправления при авторизации (HTTP_REFERER).

        Проверка авторизации пользователя и перенаправления на страницу, с которой
        был выполнен переход по ссылке на страницу авторизации (через HTTP_REFERER).
        """
        user = User.objects.filter(id=1).first()
        self.assertEqual(user.login, 0)
        self.client.get('/sign_in/', HTTP_REFERER='/preparation/')
        response = self.client.post('/sign_in/', {
            'username': 'mdulchevskiy',
            'password': '1111111111',
        })
        user = User.objects.filter(id=1).first()
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/preparation/')

    def test_get_sign_in_with_sessions(self):
        """Проверка перенаправления при авторизации (sessions).

        Проверка авторизации пользователя и перенаправления на страницу, с которой
        был выполнен переход по урлу на страницу авторизации (через sessions).
        """
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 0)
        self.client.get('/preparation/')
        self.client.get('/sign_in/')
        response = self.client.post('/sign_in/', {
            'username': 'amorgan',
            'password': '1111111111',
        })
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/preparation/')

    def test_get_sign_in_with_referer_and_sessions(self):
        """Проверка перенаправления при авторизации (HTTP_REFERER и sessions).

        Проверка авторизации пользователя и корректности перенаправления на страницу,
        с которой был выполнен переход на страницу авторизации, при наличии разных
        HTTP_REFERER и sessions.
        """
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 0)
        self.client.get('/preparation/')
        self.client.get('/sign_in/', HTTP_REFERER='/')
        response = self.client.post('/sign_in/', {
            'username': 'amorgan',
            'password': '1111111111',
        })
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_get_sign_in_without_referer_and_sessions(self):
        """Проверка перенаправления при авторизации (HTTP_REFERER и sessions отсутствуют).

        Проверка авторизации пользователя и перенаправления на домашнюю страницу,
        если страница авторизации была открыта сразу после запуска сайта
        (HTTP_REFERER и sessions отсутсвуют).
        """
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 0)
        response = self.client.post('/sign_in/', {
            'username': 'amorgan',
            'password': '1111111111',
        })
        user = User.objects.filter(id=2).first()
        self.assertEqual(user.login, 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')

    def test_post_registration(self):
        """Проверка регистрации пользователя.

        Проверка регистрации пользователя и перенаправления на страницу авторизации.
        """
        user = User.objects.filter(username='jmarston').first()
        self.assertIsNone(user)
        response = self.client.post('/registration/', {
            'first_name': 'John',
            'last_name': 'Marston',
            'email': 'jmarston@gmail.com',
            'phone_number': '+375(29)111-11-11',
            'address': 'confidential',
            'username': 'jmarston',
            'password': '1111111111',
            'conf_password': '1111111111',
        })
        user = User.objects.filter(username='jmarston').first()
        self.assertIsNotNone(user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_post_registration_when_already_sign_in_and_had_referer(self):
        """Проверка перенаправления при регистрации пользователя. Ч.1

        Проверка регистрации пользователя и перенаправления на страницу, с которой
        был выполнен переход на страницу регистрации, если пользователь уже авторизирован.
        """
        user_object = User.objects.filter(id=2)
        user_object.update(login=1)
        user = user_object.first()
        self.assertEqual(user.login, 1)
        self.client.get('/preparation/')
        self.client.get('/registration/')
        new_user = User.objects.filter(username='jmarston').first()
        self.assertIsNone(new_user)
        response = self.client.post('/registration/', {
            'first_name': 'John',
            'last_name': 'Marston',
            'email': 'jmarston@gmail.com',
            'phone_number': '+375(29)111-11-11',
            'address': 'confidential',
            'username': 'jmarston',
            'password': '1111111111',
            'conf_password': '1111111111',
        }, follow=True)
        user = User.objects.filter(username='jmarston').first()
        self.assertIsNotNone(user)
        referer = response.redirect_chain[-1][0]
        status_code = response.redirect_chain[-1][1]
        self.assertEqual(status_code, 302)
        self.assertEqual(referer, '/preparation/')

    def test_post_registration_when_already_sign_in_and_had_no_referer(self):
        """Проверка перенаправления при регистрации пользователя. Ч.1

        Проверка регистрации пользователя и перенаправления на домашнюю страницу,
        если пользователя уже авторизирован и страница регистрации была открыта
        сразу после запуска сайта.
        """
        user_object = User.objects.filter(id=2)
        user_object.update(login=1)
        user = user_object.first()
        self.assertEqual(user.login, 1)
        new_user = User.objects.filter(username='jmarston').first()
        self.assertIsNone(new_user)
        response = self.client.post('/registration/', {
            'first_name': 'John',
            'last_name': 'Marston',
            'email': 'jmarston@gmail.com',
            'phone_number': '+375(29)111-11-11',
            'address': 'confidential',
            'username': 'jmarston',
            'password': '1111111111',
            'conf_password': '1111111111',
        }, follow=True)
        user = User.objects.filter(username='jmarston').first()
        self.assertIsNotNone(user)
        referer = response.redirect_chain[-1][0]
        status_code = response.redirect_chain[-1][1]
        self.assertEqual(status_code, 302)
        self.assertEqual(referer, '/')
