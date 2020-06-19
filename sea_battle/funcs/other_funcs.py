from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from sea_battle.models import (Game,
                               User, )
from sea_battle.funcs.generation import (generate_buttons_names,
                                         generate_rand_ship_field, )


def get_session_key(request):
    """Возвращает ID сессии. Создает сессию, если она не была создана."""
    session_key = request.session.session_key
    if not request.session.exists(session_key):
        request.session.create()
    return session_key


def get_signed_user(session_key):
    """Возвращает авторезированного пользователя и обновляет дату его последней активности."""
    signed_user_object = User.objects.filter(Q(login=1) & Q(session_key=session_key))
    if signed_user_object.first():
        signed_user_object.update(last_activity_date=timezone.now())
    return signed_user_object


def get_game_data(session_key):
    """Вовращает авторезированного пользователя и начатаю игру в зависимости от пользователя."""
    signed_user_object = get_signed_user(session_key)
    signed_user = signed_user_object.first()
    if signed_user:
        game_object = Game.objects.filter(Q(user=signed_user) & Q(status='Started'))
    else:
        game_object = Game.objects.filter(Q(user_type='Guest') & Q(status='Started') &
                                          Q(user_session_key=session_key))
    return signed_user, game_object


def get_rand_ship_field():
    """Возвращает случайное игровое поле.

    Случайным образом формирует игрвое поле и соответствующую ему матрицу имен и статусов чекбоксов.
    Возвращает:
        поле вида [[0, 0, 0, 1, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 1], ...], где
            '1' - координата корабля;
        матрицу имен чекбоксов вида [['01', '0']], где
            '01' - имя чекбокса состоящее из номера строки и столбца чекбокса,
            '0' - статус чекбокса (было нажатие или нет).
    """
    player_ship_field = generate_rand_ship_field()
    checkboxes_names = generate_buttons_names()
    length = len(checkboxes_names)
    for i in range(length):
        for j in range(length):
            checkboxes_names[i][j][1] = str(player_ship_field[i][j])
    return player_ship_field, checkboxes_names


def sign_out_of_all_inactive_accounts():
    """Функция автоматического выхода из неактивных аккаунтов.

    Если любой аккаунт бездействует больше заданного времени, то функция выходит из него.
    """
    sign_in_users = User.objects.filter(login=1)
    current_time = timezone.now()
    if sign_in_users:
        for sign_user in sign_in_users:
            if sign_user.last_activity_date:
                idle_time = current_time - sign_user.last_activity_date
                if idle_time.seconds > settings.MAX_IDLE_TIME:
                    User.objects.filter(username=sign_user.username).update(login=0)
