from copy import deepcopy
from django.test import TestCase
from sea_battle.forms import UserInfoForm


main_data = {
    'first_name': 'Maxim',
    'last_name': 'Dulchevskiy',
    'email': 'mail@mail.ru',
    'phone_number': '+375(29)111-11-11',
}


class SeaBattleUserInfoFormTestCase(TestCase):
    def test_user_info_form_with_valid_data(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.1"""
        form = UserInfoForm(data=main_data)
        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.1

        Проверка работы валидации поля "first_name" (required).
        """
        data = deepcopy(main_data)
        data['first_name'] = ''
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Required field')

    def test_first_name_invalid_case_1(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.2.1

        Проверка работы валидации поля "first_name" (invalid).
        """
        data = deepcopy(main_data)
        data['first_name'] = 'Ma xim'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_first_name_invalid_case_2(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.2.2

        Проверка работы валидации поля "first_name" (invalid).
        """
        data = deepcopy(main_data)
        data['first_name'] = 'Ma_/?xim'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_first_name_invalid_case_3(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.2.3

        Проверка работы валидации поля "first_name" (invalid).
        """
        data = deepcopy(main_data)
        data['first_name'] = 'Ma123xim'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['first_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_last_name_required(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.3

        Проверка работы валидации поля "last_name" (required).
        """
        data = deepcopy(main_data)
        data['last_name'] = ''
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Required field')

    def test_last_name_invalid_case_1(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.4.1

        Проверка работы валидации поля "last_name" (invalid).
        """
        data = deepcopy(main_data)
        data['last_name'] = 'Dulche vskiy'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_last_name_invalid_case_2(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.4.2

        Проверка работы валидации поля "last_name" (invalid).
        """
        data = deepcopy(main_data)
        data['last_name'] = 'Dul_?<chevskiy'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_last_name_invalid_case_3(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.4.3

        Проверка работы валидации поля "last_name" (invalid).
        """
        data = deepcopy(main_data)
        data['last_name'] = 'Dulc124hevskiy'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['last_name'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_phone_number_required(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.5

        Проверка работы валидации поля "phone_number" (required).
        """
        data = deepcopy(main_data)
        data['phone_number'] = ''
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['phone_number'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Required field')

    def test_phone_number_invalid(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.6

        Проверка работы валидации поля "phone_number" (invalid).
        """
        data = deepcopy(main_data)
        data['phone_number'] = '1111111'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['phone_number'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')

    def test_phone_number_case_1(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.1

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '+375(29)111-11-11'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_phone_number_case_2(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.2

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '+375(29)1111111'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_phone_number_case_3(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.3

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '+375291111111'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_phone_number_case_4(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.4

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '8(029)111-11-11'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_phone_number_case_5(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.5

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '8(029)111-11-11'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_phone_number_case_6(self):
        """Проверка работы формы "user_info" при введенных валидных данных. Ч.2.6

        Проверка работы валидации поля "phone_number".
        """
        data = deepcopy(main_data)
        data['phone_number'] = '80291111111'
        form = UserInfoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_email_required(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.7

        Проверка работы валидации поля "email" (required).
        """
        data = deepcopy(main_data)
        data['email'] = ''
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['email'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Required field')

    def test_email_invalid(self):
        """Проверка работы формы "user_info" при введенных невалидных данных. Ч.8

        Проверка работы валидации поля "email" (invalid).
        """
        data = deepcopy(main_data)
        data['email'] = 'mailru'
        form = UserInfoForm(data=data)
        error_message = form.errors.as_data()['email'][0].message
        self.assertFalse(form.is_valid())
        self.assertEqual(error_message, 'Not valid field')
