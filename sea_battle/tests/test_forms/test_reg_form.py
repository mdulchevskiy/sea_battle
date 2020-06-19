from copy import deepcopy
from django.test import TestCase
from sea_battle.forms import RegForm
from sea_battle.models import User


main_data = {
    'username': 'mdulchevskiy',
    'password': '1111111111',
    'conf_password': '1111111111',
    'first_name': 'Maxim',
    'last_name': 'Dulchevskiy',
    'email': 'maksimdulchevskii@mail.ru',
    'phone_number': '+375(29)111-11-11',
}


class SeaBattleRegFormTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='amorgan',
            password='1111111111',
            first_name='Arthur',
            last_name='Morgan',
            email='amorgan@mail.ru',
            phone_number='+375(29)111-11-11',
        )

    def test_reg_form_with_valid_data(self):
        """Проверка работы формы регистрации при введенных валидных данных. Ч.1"""
        form = RegForm(data=main_data)
        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.1

        Проверка работы валидации поля "first_name" (required).
        """
        data = deepcopy(main_data)
        data['first_name'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'First name is required')

    def test_first_name_invalid(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.2

        Проверка работы валидации поля "first_name" (invalid).
        """
        data = deepcopy(main_data)
        data['first_name'] = 'Ma xim'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid first name')

    def test_last_name_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.3

        Проверка работы валидации поля "last_name" (required).
        """
        data = deepcopy(main_data)
        data['last_name'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Last name is required')

    def test_last_name_invalid(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.4

        Проверка работы валидации поля "last_name" (invalid).
        """
        data = deepcopy(main_data)
        data['last_name'] = 'Dulche vskiy'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid last name')

    def test_phone_number_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.5

        Проверка работы валидации поля "phone_number" (required).
        """
        data = deepcopy(main_data)
        data['phone_number'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['phone_number'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Phone number is required')

    def test_phone_number_invalid(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.6

        Проверка работы валидации поля "phone_number" (invalid).
        """
        data = deepcopy(main_data)
        data['phone_number'] = '1111111'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['phone_number'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid phone number')

    def test_email_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.7

        Проверка работы валидации поля "email" (required).
        """
        data = deepcopy(main_data)
        data['email'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['email'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Email is required')

    def test_email_invalid(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.8

        Проверка работы валидации поля "email" (invalid).
        """
        data = deepcopy(main_data)
        data['email'] = 'mailru'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['email'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid email')

    def test_email_already_exist(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.9

        Проверка работы валидации поля "email". Уже используется в другом аккаунте.
        """
        data = deepcopy(main_data)
        data['email'] = 'amorgan@mail.ru'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['email'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'User with that email already exists')

    def test_username_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.10

        Проверка работы валидации поля "username" (required).
        """
        data = deepcopy(main_data)
        data['username'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Username is required')

    def test_username_already_exist(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.11

        Проверка работы валидации поля "username". Уже используется в другом аккаунте.
        """
        data = deepcopy(main_data)
        data['username'] = 'amorgan'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'User with that username already exists')

    def test_username_invalid_case_1(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.12.1

        Проверка работы валидации поля "username" (invalid).
        """
        data = deepcopy(main_data)
        data['username'] = '_max'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid username')

    def test_username_invalid_case_2(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.12.2

        Проверка работы валидации поля "username" (invalid).
        """
        data = deepcopy(main_data)
        data['username'] = 'max_'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid username')

    def test_username_invalid_case_3(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.12.3

        Проверка работы валидации поля "username" (invalid).
        """
        data = deepcopy(main_data)
        data['username'] = '.max'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid username')

    def test_username_invalid_case_4(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.12.4

        Проверка работы валидации поля "username" (invalid).
        """
        data = deepcopy(main_data)
        data['username'] = 'max.'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid username')

    def test_username_invalid_case_5(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.12.5

        Проверка работы валидации поля "username" (invalid).
        """
        data = deepcopy(main_data)
        data['username'] = 'max?-im'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['username'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Enter a valid username')

    def test_valid_username(self):
        """Проверка работы формы регистрации при введенных валидных данных. Ч.2

        Проверка работы валидации поля "username".
        """
        data = deepcopy(main_data)
        data['username'] = 'm.a_x-i.m'
        form = RegForm(data=data)
        self.assertTrue(form.is_valid())

    def test_password_invalid_case_1(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.13.1

        Проверка работы валидации поля "password" (invalid).
        """
        data = deepcopy(main_data)
        data['password'] = '123abc'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Incorrect format for password')

    def test_password_invalid_case_2(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.13.2

        Проверка работы валидации поля "password" (invalid).
        """
        data = deepcopy(main_data)
        data['password'] = '123a--c789'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Incorrect format for password')

    def test_password_invalid_case_3(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.13.3

        Проверка работы валидации поля "password" (invalid).
        """
        data = deepcopy(main_data)
        data['password'] = '123a- -c789'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Incorrect format for password')

    def test_conf_password_required(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.14

        Проверка работы валидации поля "password" (required).
        """
        data = deepcopy(main_data)
        data['conf_password'] = ''
        form = RegForm(data=data)
        error_message = form.errors.as_data()['conf_password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Password confirmation is required')

    def test_passwords_matching(self):
        """Проверка работы формы регистрации при введенных невалидных данных. Ч.15

        Проверка работы валидации поля "conf_password" (подтверждения пароля).
        """
        data = deepcopy(main_data)
        data['conf_password'] = '123'
        form = RegForm(data=data)
        error_message = form.errors.as_data()['conf_password'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, "Passwords don't match")
