from copy import deepcopy
from django.test import TestCase
from sea_battle.forms import SignInForm
from sea_battle.models import User


main_data = {
    'username': 'mdulchevskiy',
    'password': '1111111111',
}


class SeaBattleSignInFormTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='mdulchevskiy',
            password='1111111111',
            first_name='Maxim',
            last_name='Dulchevskiy',
            email='mail@mail.ru',
            phone_number='+375(29)111-11-11',
        )

    def test_sign_in_form_with_valid_data(self):
        """Проверка работы формы авторизации при введенных валидных данных."""
        form = SignInForm(data=main_data)
        self.assertTrue(form.is_valid())

    def test_username(self):
        """Проверка работы валидации поля "username" (пользователь не найден)."""
        data = deepcopy(main_data)
        data['username'] = 'mdulc hevskiy'
        form = SignInForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'User with that username was not found!')

    def test_username_required(self):
        """Проверка работы валидации поля "username" (required)."""
        data = deepcopy(main_data)
        data['username'] = ''
        form = SignInForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Username is required')

    def test_password(self):
        """Проверка работы валидации поля "password" (некорректный пароль)."""
        data = deepcopy(main_data)
        data['password'] = '1111111112'
        form = SignInForm(data=data)
        error_message = form.errors.as_data()['password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Incorrect password')

    def test_password_required(self):
        """Проверка работы валидации поля "password" (required)."""
        data = deepcopy(main_data)
        data['password'] = ''
        form = SignInForm(data=data)
        error_message = form.errors.as_data()['password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Password is required')
