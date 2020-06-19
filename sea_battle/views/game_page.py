from string import ascii_uppercase as ltr
from itertools import (count,
                       islice, )
from django.conf import settings
from django.shortcuts import (redirect,
                              render, )
from sea_battle.funcs import (enemy_attack,
                              enemy_ships_left,
                              find_ships,
                              generate_buttons_names,
                              get_game_data,
                              get_session_key,
                              get_ship_perimeter,
                              str_to_matrix,
                              matrix_to_str,
                              prepare_ships, )


def game_page(request):
    session_key = get_session_key(request)
    request.session[f'referer_{session_key}'] = 'game_page'
    signed_user, game_object = get_game_data(session_key)
    started_game = game_object.first()

    if not started_game:
        return redirect('home_page')

    username = f'Guest_{str(started_game.id).rjust(6, "0")}' if not started_game.user else started_game.user.username
    user_mark = f'{session_key}_{username}'
    titles = list(islice(count(1), 10))
    radio_names = generate_buttons_names()
    game_status = None
    move_counter = started_game.moves
    points = started_game.points
    enemy_field_with_player_moves = started_game.enemy_field_with_player_moves
    player_field_with_enemy_moves = started_game.player_field_with_enemy_moves
    message = str_to_matrix(started_game.messages, option=True)
    message = [] if not message[0][0] else message
    enemy_ship_field = str_to_matrix(enemy_field_with_player_moves) \
        if enemy_field_with_player_moves else str_to_matrix(started_game.enemy_field)
    player_ship_field = str_to_matrix(player_field_with_enemy_moves) \
        if player_field_with_enemy_moves else str_to_matrix(started_game.player_field)
    player_miss_flag = request.session.get(f'player_miss_flag_{user_mark}')
    combo_counter = request.session.get(f'combo_counter_{user_mark}') or 0
    enemy_ships = request.session.get(f'enemy_ships_{user_mark}') or prepare_ships(enemy_ship_field)
    player_ships = request.session.get(f'player_ships_{user_mark}') or prepare_ships(player_ship_field)
    session_titles = [
        f'enemy_ships_{user_mark}',
        f'player_ships_{user_mark}',
        f'player_miss_flag_{user_mark}',
        f'combo_counter_{user_mark}',
    ]

    if request.method == 'POST':
        end_game_flag = request.POST.get('end_game')
        if end_game_flag == 'end_game':
            game_object.update(status='Aborted')
            return redirect('home_page')
        elif player_miss_flag:
            player_ship_field, message, player_miss_flag = enemy_attack(
                request, player_ship_field, player_ships, message, titles, user_mark)
            game_object.update(
                player_field_with_enemy_moves=matrix_to_str(player_ship_field),
                messages=matrix_to_str(message, option=True),
                moves=move_counter, )
            request.session[f'player_miss_flag_{user_mark}'] = player_miss_flag
            shot_ships = len(find_ships(player_ship_field, 4))
            if shot_ships == 10:
                game_object.update(
                    status='Lose',
                    points=0,
                    accuracy=started_game.hits / move_counter, )
                game_status = 'Lose'
                for session_title in session_titles:
                    del request.session[session_title]
        else:
            move = request.POST.get('move')
            if not move:
                return redirect('game_page')
            move = list(map(int, move))
            move_value = enemy_ship_field[move[0]][move[1]]
            if move_value == 1 or move_value == 0:
                for i, ship_info in enumerate(enemy_ships):
                    ship = ship_info[0]
                    if move in ship:
                        enemy_ship_field[move[0]][move[1]] = 3
                        hit_count = enemy_ships[i][1][0]
                        ship_size = enemy_ships[i][1][1]
                        hit_count += 1
                        if hit_count == ship_size:
                            for coordinate in ship:
                                enemy_ship_field[coordinate[0]][coordinate[1]] = 4
                            ship_perimeter = get_ship_perimeter(ship)
                            for coordinate in ship_perimeter:
                                enemy_ship_field[coordinate[0]][coordinate[1]] = 2
                            message.append([f'{ltr[move[1]]}{titles[move[0]]} - Sunk!', '1'])
                            game_object.update(
                                sunks=started_game.sunks + 1,
                                hits=started_game.hits + 1, )
                        else:
                            message.append([f'{ltr[move[1]]}{titles[move[0]]} - Hit!', '1'])
                            game_object.update(hits=started_game.hits + 1)
                        enemy_ships[i][1][0] = hit_count
                        combo_counter += 1
                        request.session[f'enemy_ships_{user_mark}'] = enemy_ships
                        request.session[f'combo_counter_{user_mark}'] = combo_counter
                        break
                else:
                    player_miss_flag = True
                    combo_counter = 0
                    request.session[f'combo_counter_{user_mark}'] = combo_counter
                    request.session[f'player_miss_flag_{user_mark}'] = player_miss_flag
                    enemy_ship_field[move[0]][move[1]] = 2
                    message.append([f'{ltr[move[1]]}{titles[move[0]]} - Miss!', '1'])
                move_counter += 1
                if combo_counter > 1:
                    points += 5 * (combo_counter - 1)
                game_object.update(
                    enemy_field_with_player_moves=matrix_to_str(enemy_ship_field),
                    messages=matrix_to_str(message, option=True),
                    points=points,
                    moves=move_counter, )
                shot_ships = len(find_ships(enemy_ship_field, 4))
                if shot_ships == 10:
                    game_object.update(
                        status='Win',
                        points=settings.MAX_MOVES - move_counter + points,
                        accuracy=started_game.hits / move_counter, )
                    game_status = 'Win'
                    for session_title in session_titles:
                        del request.session[session_title]

    for i, line in enumerate(radio_names):
        for j, radio_name in enumerate(line):
            radio_names[i][j][1] = enemy_ship_field[i][j]

    return render(request, 'game_page.html', {
        'player': username,
        'signed_user': signed_user,
        'player_ship_field': zip(titles, player_ship_field),
        'enemy_ship_field': zip(titles, enemy_ship_field),
        'message': message,
        'moves': move_counter,
        'points': points,
        'game_status': game_status,
        'enemy_turn': player_miss_flag,
        'ships_amount': enemy_ships_left(enemy_ship_field),
        'radio_names': zip(titles, radio_names), })
