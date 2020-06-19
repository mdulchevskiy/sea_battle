from django.db.models import Q
from django.shortcuts import (redirect,
                              render, )
from sea_battle.models import (Game,
                               User, )
from sea_battle.funcs import (get_game_data,
                              get_leaderboard,
                              get_session_key,
                              sign_out_of_all_inactive_accounts, )


def home_page(request):
    session_key = get_session_key(request)
    sign_out_of_all_inactive_accounts()
    request.session[f'referer_{session_key}'] = 'home_page'
    leaderboard = get_leaderboard(Game.objects.filter(status='Win'))
    signed_user, game_object = get_game_data(session_key)
    started_game = game_object.first()

    if request.method == 'GET':
        return render(request, 'home_page.html', {
            'signed_user': signed_user,
            'leaderboard': leaderboard, })

    elif request.method == 'POST':
        sign_out_flag = request.POST.get('sign_out')
        start_game_flag = request.POST.get('start_game')
        continue_game_flag = request.POST.get('continue_game')
        if sign_out_flag:
            User.objects.filter(Q(login=1) & Q(session_key=session_key)).update(login=0)
            referer = request.META['HTTP_REFERER']
            return redirect(referer)
        elif start_game_flag:
            if started_game:
                return render(request, 'home_page.html', {
                    'signed_user': signed_user,
                    'leaderboard': leaderboard,
                    'new_game_flag': True, })
            return redirect('preparation_page')
        elif continue_game_flag:
            if continue_game_flag == 'continue':
                return redirect('game_page')
            elif continue_game_flag == 'new_game':
                game_object.update(status='Aborted')
                return redirect('preparation_page')
