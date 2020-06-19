from itertools import filterfalse
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import (redirect,
                              render, )
from sea_battle.models import User
from sea_battle.funcs import (get_session_key,
                              get_signed_user,
                              phone_number_formatting, )
from sea_battle.forms import (RegForm,
                              SignInForm, )


referer_list = []


def sign_in(request):
    session_key = get_session_key(request)
    signed_user = get_signed_user(session_key).first()

    if request.method == 'GET':
        referer = request.META.get('HTTP_REFERER')
        custom_referer = request.session.get(f'referer_{session_key}')
        referer = referer or custom_referer or 'home_page'
        referer_list.append(referer)
        if signed_user and signed_user.session_key == session_key:
            # если пользователь авторизирован и переход на страницу авторизации был сделан после регистрации нового
            # пользователя, что возможно только по вводу урла страницы регистрации, то переход будет на ту страницу,
            # на которой был введен урл страницы регистрации.
            if 'registration' in referer:
                referer = custom_referer or 'home_page'
            referer_list.clear()
            return redirect(referer)
        else:
            form = SignInForm()
            return render(request, 'sign_in_page.html', {'form': form})
    elif request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user_object = User.objects.filter(username=username)
            user = user_object.first()
            if password == user.password:
                if user.login != 1:
                    old_user_mark = f'{user.session_key}_{user.username}'
                    new_user_mark = f'{session_key}_{user.username}'
                    old_session_titles = [
                        f'enemy_ships_{old_user_mark}',
                        f'player_ships_{old_user_mark}',
                        f'player_miss_flag_{old_user_mark}',
                        f'combo_counter_{old_user_mark}',
                    ]
                    new_session_titles = [
                        f'enemy_ships_{new_user_mark}',
                        f'player_ships_{new_user_mark}',
                        f'player_miss_flag_{new_user_mark}',
                        f'combo_counter_{new_user_mark}',
                    ]
                    user_object.update(login=1)
                    user_object.update(session_key=session_key)
                    user_object.update(last_activity_date=timezone.now())
                    # если игра была начата с одном session_key (в одном брауезере), а продолжилась на новом,
                    # то все сессии со старым session_key, переносятся на новый.
                    for i, old_session_title in enumerate(old_session_titles):
                        value = request.session.get(old_session_title)
                        if value:
                            request.session[new_session_titles[i]] = value
                            del request.session[old_session_title]
                    # после авторизации будет осуществлен переход на предыдущую страницу игнорируя страницу регистрации.
                    referer = referer_list[-1] if referer_list else None
                    if referer and 'registration' in referer:
                        referer = None
                        if len(referer_list) > 1:
                            referer = list(filterfalse(lambda x: 'registration' in x, referer_list))[-1]
                    custom_referer = request.session.get(f'referer_{session_key}')
                    referer = referer or custom_referer or 'home_page'
                    referer_list.clear()
                    return redirect(referer)
                else:
                    error = "Cannot sign in. You already signed in on the other device."
                    messages.add_message(request, messages.ERROR, error)
        return render(request, 'sign_in_page.html', {'form': form})


def registration(request):
    session_key = get_session_key(request)
    _ = get_signed_user(session_key)
    form = RegForm()

    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['conf_password']
            phone_number = data['phone_number']
            phone_number = phone_number_formatting(phone_number)
            data.update([('first_name', data.get('first_name').capitalize()),
                         ('last_name', data.get('last_name').capitalize()),
                         ('phone_number', phone_number), ])
            User.objects.create(**data)
            return redirect('sign_in')
    return render(request, 'reg_page.html', {'form': form})
