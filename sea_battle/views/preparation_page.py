from itertools import (count,
                       islice, )
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (redirect,
                              render, )
from sea_battle.models import Game
from sea_battle.funcs import (generate_buttons_names,
                              get_game_data,
                              get_rand_ship_field,
                              get_session_key,
                              matrix_to_str,
                              prepare_ships,
                              read_player_ship_field,
                              ship_field_validation, )


def preparation_page(request):
    session_key = get_session_key(request)
    request.session[f'referer_{session_key}'] = 'preparation_page'
    titles = list(islice(count(1), 10))
    signed_user, game_object = get_game_data(session_key)
    started_game = game_object.first()

    if started_game:
        return redirect('game_page')

    if request.method == 'GET':
        checkboxes_names = generate_buttons_names()
        checkboxes_names_with_titles = zip(titles, checkboxes_names)
        return render(request, 'preparation_page.html', {
            'checkboxes_names': checkboxes_names_with_titles,
            'signed_user': signed_user, })

    elif request.method == 'POST':
        data = dict(request.POST.lists())
        random_field_flag = data.get('get_random_field')
        if random_field_flag:
            data.pop('get_random_field')
            player_ship_field, checkboxes_names = get_rand_ship_field()
            checkboxes_names_with_titles = zip(titles, checkboxes_names)
            return render(request, 'preparation_page.html', {
                'checkboxes_names': checkboxes_names_with_titles,
                'signed_user': signed_user, })
        else:
            player_ship_field, checkboxes_names = read_player_ship_field(data)
            checkboxes_names_with_title = zip(titles, checkboxes_names)
            error = ship_field_validation(player_ship_field)
        if error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'preparation_page.html', {
                'checkboxes_names': checkboxes_names_with_title,
                'signed_user': signed_user, })
        else:
            enemy_ship_field, _ = get_rand_ship_field()
            if signed_user:
                Game.objects.create(
                    user_type='User',
                    user=signed_user,
                    player_field=matrix_to_str(player_ship_field),
                    enemy_field=matrix_to_str(enemy_ship_field),
                    user_session_key=session_key, )
            else:
                Game.objects.create(
                    player_field=matrix_to_str(player_ship_field),
                    enemy_field=matrix_to_str(enemy_ship_field),
                    user_session_key=session_key, )

            guest_game = Game.objects.filter(Q(status='Started') & Q(user_type='Guest') &
                                             Q(user_session_key=session_key)).first()
            username = f'Guest_{str(guest_game.id).rjust(6, "0")}' if guest_game else None
            username = signed_user.username if signed_user else username
            user_mark = f'{session_key}_{username}'

            request.session[f'enemy_ships_{user_mark}'] = prepare_ships(enemy_ship_field)
            request.session[f'player_ships_{user_mark}'] = prepare_ships(player_ship_field)
            request.session[f'player_miss_flag_{user_mark}'] = False
            return redirect('game_page')
