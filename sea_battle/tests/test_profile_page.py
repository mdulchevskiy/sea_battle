from unittest import mock
from django.test import TestCase
from sea_battle.views.profile_page import UserGameInfo
from sea_battle.models import User


class CustomFormClass:
    def __init__(self, valid, data=None, size=None, width=None, height=None):
        self.cleaned_data = {'upload': CustomFileClass(size, width, height)} if data else {'upload': None}
        self.valid = valid

    def is_valid(self):
        return True if self.valid else False


class CustomFileClass:
    def __init__(self, size, width, height):
        self.size = size
        self.image = CustomImageClass(width, height)

    @staticmethod
    def chunks():
        return [b'image']


class CustomImageClass:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.format = 'png'


class CustomGameInfoClass:
    pic_exist = True
    login = 1
    username = 'mdulchevskiy'
    first_name = 'Maxim'
    last_name = 'Dulchevskiy'
    email = 'email@gmail.com'
    phone_number = 'phone_number'


class SeaBattleProfilePageViewTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='mdulchevskiy',
            password='1111111111',
            first_name='Maxim',
            last_name='Dulchevskiy',
            email='',
            phone_number='+375(29)111-11-11',
            session_key=self.client.session.session_key,
        )
        User.objects.create(
            username='rsanchez',
            password='1111111111',
            first_name='Rick',
            last_name='Sanchez',
            email='',
            phone_number='+375(29)111-11-11',
            session_key=self.client.session.session_key,
        )

    def test_redirection_when_not_sign_in_case_1(self):
        """Проверка перенаправления неавторизированного пользоватля. Ч.1

        Проверка перенаправления на страницу авторизации 'sign_in/', если
        неавторизированный пользователь переходит по урлу 'account/'.
        """
        user = User.objects.filter(login=1).first()
        self.assertIsNone(user)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')

    def test_redirection_when_not_sign_in_case_2(self):
        """Проверка перенаправления неавторизированного пользоватля. Ч.2

        Проверка перенаправления на страницу авторезированного пользователя
        после успешной авторизации, если неавторизированный пользователь
        переход по урлу 'account/'.
        """
        # перенаправление на страницу авторизации 'sign_in/'.
        user = User.objects.filter(login=1).first()
        self.assertIsNone(user)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/sign_in/')
        # успешная авторизация пользователя 'mdulchevskiy'.
        response = self.client.post('/sign_in/', {'username': 'mdulchevskiy', 'password': '1111111111'})
        self.assertEqual(response['Location'], '/account/')
        # перенаправление на страницу авторезированного пользователя по урлу 'account/'.
        user = User.objects.filter(login=1).first()
        self.assertIsNotNone(user)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], f'/account/{user.username}')

    def test_rendering_404_page(self):
        """Проверка отображения 404-страницы.

        Проверка отображения ошибки 404, если был произведен переход по урлу
        несуществующего пользователя.
        """
        user = User.objects.filter(login=1).first()
        self.assertIsNone(user)
        response = self.client.get('/account/non-existent-user')
        self.assertEqual(response.status_code, 200)
        check = b'GO HOME' in response.content
        self.assertTrue(check)

    def test_redirection_when_sign_in(self):
        """Проверка перенаправления авторизированного пользоватля.

        Проверка перенаправления на страницу авторизированного пользователя
        при переходе по урлу 'account/'.
        """
        user_object = User.objects.filter(id=1)
        user_object.update(login=1)
        user = user_object.first()
        self.assertIsNotNone(user)
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], f'/account/{user.username}')

    def test_rendering_basic_editing_tools_for_your_acc_when_sign_in(self):
        """Проверка отображения шаблона. Ч.1

        Проверка отображения функционала по редактированию собственного
        профиля для авторизированного пользователя.
        """
        user_object = User.objects.filter(id=1)
        user_object.update(login=1)
        user = user_object.first()
        self.assertIsNotNone(user)
        response = self.client.get(f'/account/{user.username}')
        check_1 = b'Edit' in response.content
        check_2 = b'Edit profile' in response.content
        check_3 = b'Send stat. to mail' in response.content
        check = check_1 and check_2 and check_3
        self.assertTrue(check)

    def test_rendering_basic_editing_tools_for_not_your_acc_when_sign_in(self):
        """Проверка отображения шаблона. Ч.2

        Проверка отсутствия отображения функционала по редактированию чужого
        профиля для авторизированного пользователя.
        """
        user_object = User.objects.filter(id=1)
        user_object.update(login=1)
        user = user_object.first()
        self.assertIsNotNone(user)
        response = self.client.get('/account/rsanchez')
        check_1 = b'Edit' in response.content
        check_2 = b'Edit profile' in response.content
        check_3 = b'Send stat. to mail' in response.content
        check = check_1 or check_2 or check_3
        self.assertFalse(check)

    def test_rendering_basic_editing_tools_for_any_acc_when_not_sign_in(self):
        """Проверка отображения шаблона. Ч.3

        Проверка отсутствия отображения функционала по редактированию любого
        профиля для неавторизированного пользователя.
        """
        user = User.objects.filter(login=1).first()
        self.assertIsNone(user)
        response = self.client.get('/account/mdulchevskiy')
        check_1 = b'Edit' in response.content
        check_2 = b'Edit profile' in response.content
        check_3 = b'Send stat. to mail' in response.content
        check = check_1 or check_2 or check_3
        self.assertFalse(check)
        response = self.client.get('/account/rsanchez')
        check_1 = b'Edit' in response.content
        check_2 = b'Edit profile' in response.content
        check_3 = b'Send stat. to mail' in response.content
        check = check_1 or check_2 or check_3
        self.assertFalse(check)

    def test_rendering_editing_tools_for_profile_pic_case_1(self):
        """Проверка отображения шаблона. Ч.4

        Проверка наличия отображения функционала по редактированию изображения
        профиля (изображение профиля присутствует).
        """
        User.objects.filter(id=1).update(login=1)
        with mock.patch('sea_battle.views.profile_page.UserGameInfo') as mock_con:
            mock_con.return_value = CustomGameInfoClass()
            response = self.client.post('/account/mdulchevskiy')
            check_1 = b'<label class="label_for_image_input" for="image_field">Choose Image' in response.content
            check_2 = b'<button class="upload_button" name="upload_pic" value="1">Upload' in response.content
            check_3 = b'<button class="remove_button" name="remove_pic" value="1">Remove Image' in response.content
            check = check_1 and check_2 and check_3
            self.assertTrue(check)

    def test_rendering_editing_tools_for_profile_pic_case_2(self):
        """Проверка отображения шаблона. Ч.5

        Проверка наличия отображения функционала по редактированию изображения
        профиля (изображение профиля отсутствует).
        """
        custom_game_info = CustomGameInfoClass()
        custom_game_info.pic_exist = False
        User.objects.filter(id=1).update(login=1)
        with mock.patch('sea_battle.views.profile_page.UserGameInfo') as mock_con:
            mock_con.return_value = custom_game_info
            response = self.client.post('/account/mdulchevskiy')
            check_1 = b'<label class="label_for_image_input" for="image_field">Choose Image' in response.content
            check_2 = b'<button class="upload_button" name="upload_pic" value="1">Upload' in response.content
            check_3 = b'<button class="remove_button" name="remove_pic" value="1">Remove Image' not in response.content
            check = check_1 and check_2 and check_3
            self.assertTrue(check)

    def test_save_personal_info(self):
        """Проверка редактирования личных данных профиля.

        Проверка сохранения изменения личных данных профиля при их редактировании.
        """
        user_object = User.objects.filter(id=1)
        user_object.update(login=1, email='maksimdulchevskii@mail.ru')
        user = user_object.first()
        self.assertEqual(user.first_name, 'Maxim')
        self.assertEqual(user.last_name, 'Dulchevskiy')
        self.assertEqual(user.email, 'maksimdulchevskii@mail.ru')
        self.assertEqual(user.phone_number, '+375(29)111-11-11')
        content = {
            'save_info': True,
            'first_name': 'john',
            'last_name': 'marston',
            'email': 'jmarston@gmail.com',
            'phone_number': '+375291234567'
        }
        self.client.post('/account/mdulchevskiy', content)
        user = User.objects.filter(id=1).first()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Marston')
        self.assertEqual(user.email, 'jmarston@gmail.com')
        self.assertEqual(user.phone_number, '+375(29)123-45-67')

    def test_send_email_not_valid_email_case(self):
        """Проверка отправки email. Ч.1

        Проверка вывода на шаблон сообщения "Cannot send email. User's email not valid.",
        если в профиле указана невалидная почта.
        """
        with mock.patch('sea_battle.views.profile_page.check_connection') as mock_con:
            mock_con.return_value = True
            User.objects.filter(id=1).update(email='mail.ru', login=1)
            message = b"email not valid."
            response = self.client.post('/account/mdulchevskiy', {'send_mail': True})
            check = message in response.content
            self.assertTrue(check)

    def test_send_email_success_case(self):
        """Проверка отправки email. Ч.2

        Проверка вывода на шаблон сообщения "Your profile statistics has been send to your email.",
        если сообщение было успешно отправлено.
        """
        User.objects.filter(id=1).update(email='maksimdulchevskii@mail.ru', login=1)
        with mock.patch('sea_battle.views.profile_page.check_connection') as mock_con:
            mock_con.return_value = True
            message = b'Your profile statistics has been send to your email.'
            response = self.client.post('/account/mdulchevskiy', {'send_mail': True})
            check = message in response.content
            self.assertTrue(check)

    def test_send_email_no_email_case(self):
        """Проверка отправки email. Ч.3

        Проверка вывода на шаблон сообщения "Cannot send email. No email address in the profile.",
        если в профиле не указана почта.
        """
        User.objects.filter(id=1).update(login=1)
        with mock.patch('sea_battle.views.profile_page.check_connection') as mock_con:
            mock_con.return_value = True
            message = b'Cannot send email. No email address in the profile.'
            response = self.client.post('/account/mdulchevskiy', {'send_mail': True})
            check = message in response.content
            self.assertTrue(check)

    def test_send_email_no_connection_case(self):
        """Проверка отправки email. Ч.4

        Проверка вывода на шаблон сообщения "Cannot send email. Check your internet connection.",
        если отсутствует соединение с интернетом.
        """
        User.objects.filter(id=1).update(login=1)
        with mock.patch('sea_battle.views.profile_page.check_connection') as mock_con:
            mock_con.return_value = False
            message = b'Cannot send email. Check your internet connection.'
            response = self.client.post('/account/mdulchevskiy', {'send_mail': True})
            check = message in response.content
            self.assertTrue(check)

    def test_successful_pic_upload(self):
        """Проверка загрузки изображения.

        Проверка корректности работы загрузки изображения, соответсвуюшего всем ограничениям,
        его сохранения, добавления в базу данных и соответствующего отображения шаблона.
        """
        user_object = User.objects.filter(id=2)
        user_object.update(login=1)
        user = user_object.first()
        user_info = UserGameInfo(user)
        self.assertFalse(user_info.pic_exist)
        self.assertEqual(user.profile_pic.name, '')
        with mock.patch('sea_battle.views.profile_page.UploadForm') as mock_con:
            mock_con.return_value = CustomFormClass(True, True, 600, 300, 300)
            self.client.post(f'/account/{user.username}', {'upload_pic': True})
        user = User.objects.filter(id=2).first()
        user_info = UserGameInfo(user)
        self.assertTrue(user_info.pic_exist)
        self.assertEqual(user.profile_pic.name, 'rsanchez.png')
        user.profile_pic.delete(save=False)

    def test_remove_nonexistent_pic(self):
        """Проверка удаления изображения. Ч.1

        Проверка корректности работы при попытке удаления несуществующего изображения профиля.
        """
        user_object = User.objects.filter(id=2)
        user_object.update(login=1)
        user = user_object.first()
        response = self.client.post(f'/account/{user.username}', {'remove_pic': True})
        check = b'Cannot remove nonexistent picture.' in response.content
        self.assertTrue(check)

    def test_successful_remove(self):
        """Проверка удаления изображения. Ч.2

        Проверка корректности работы удаления изображения профиля, обновления
        информации в базе данных и соответствующего отображения шаблона.
        """
        # загрузка изображения.
        user_object = User.objects.filter(id=2)
        user_object.update(login=1)
        user = user_object.first()
        user_info = UserGameInfo(user)
        self.assertFalse(user_info.pic_exist)
        self.assertEqual(user.profile_pic.name, '')
        with mock.patch('sea_battle.views.profile_page.UploadForm') as mock_con:
            mock_con.return_value = CustomFormClass(True, True, 600, 300, 300)
            self.client.post(f'/account/{user.username}', {'upload_pic': True})
        user = User.objects.filter(id=2).first()
        user_info = UserGameInfo(user)
        self.assertTrue(user_info.pic_exist)
        self.assertEqual(user.profile_pic.name, 'rsanchez.png')
        # удаление изображения.
        self.client.post(f'/account/{user.username}', {'remove_pic': True})
        user = User.objects.filter(id=2).first()
        user_info = UserGameInfo(user)
        self.assertFalse(user_info.pic_exist)
        self.assertIsNone(user.profile_pic.name)
