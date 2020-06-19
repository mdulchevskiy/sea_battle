import requests
from statistics import mean
from operator import itemgetter
from django.db.models import Q
from sea_battle.models import (Game,
                               User, )


class WinGame:
    """Вспомогательный класс для упрощения расчета таблицы лидеров.

    Используется для функции "get_leaderboard".
    """
    def __init__(self, game):
        self.game = game
        self.points = game.points
        self.rank = None

    def __repr__(self):
        return f'WG: {self.game.pk} {self.game.points}'

    @property
    def user(self):
        return True if self.game.user else False

    @property
    def username(self):
        return self.game.user.username if self.game.user else f'Guest_{str(self.game.pk).rjust(6, "0")}'

    def set_rank(self, rank):
        self.rank = rank


class UserGameInfo:
    """Вспомогательный класс для вывода пользовательской информации.

    Используется в "profile_page".
    """
    def __init__(self, user):
        self.user = user
        self.id = user.id
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.email = user.email
        self.phone_number = user.phone_number
        self.date = user.registration_date
        self.profile_pic = user.profile_pic
        self.login = user.login

    def all_games(self):
        return Game.objects.filter(Q(user__username=self.username) &
                                   ~Q(status='Aborted') & ~Q(status='Started')).all()

    def win_games(self):
        return Game.objects.filter(Q(user__username=self.username, status='Win')).all()

    @property
    def battles(self):
        return len(self.all_games())

    @property
    def victories(self):
        return len(self.win_games())

    @property
    def victories_pct_first_format(self):
        victories = '{:.0%}'.format(self.victories / self.battles) if self.battles else 0
        return victories

    @property
    def victories_pct_second_format(self):
        victories = '{:.2%}'.format(self.victories / self.battles) if self.battles else 0
        return victories

    @property
    def defeats(self):
        return self.battles - self.victories

    @property
    def defeats_pct(self):
        defeats = '{:.2%}'.format(self.defeats / self.battles) if self.battles else 0
        return defeats

    @property
    def destroyed_warships(self):
        return sum([game.sunks for game in self.all_games()])

    @property
    def accuracy_first_format(self):
        accuracy = '{:.0%}'.format(mean([game.accuracy for game in self.all_games()])) if self.battles else 0
        return accuracy

    @property
    def accuracy_second_format(self):
        accuracy = '{:.2%}'.format(mean([game.accuracy for game in self.all_games()])) if self.battles else 0
        return accuracy

    @property
    def last_five_battles(self):
        games = Game.objects.filter(Q(user__username=self.username) & Q(Q(status='Win') | Q(status='Lose')))
        return games.order_by('-id')[:5]

    @property
    def amount_of_last_five_battles(self):
        return len(self.last_five_battles)

    @property
    def best_game(self):
        return max([game.points for game in self.win_games()]) if self.victories else 0

    @property
    def fastest_game(self):
        return min([game.moves for game in self.win_games()]) if self.victories else 0

    @property
    def best_accuracy(self):
        accuracy = '{:.2%}'.format(max([game.accuracy for game in self.win_games()])) if self.victories else 0
        return accuracy

    @property
    def rank(self):
        if self.win_games():
            users = User.objects.all()
            top_list = [(user.username, UserGameInfo(user).best_game) for user in users]
            top_list.sort(key=itemgetter(1), reverse=True)
            top_dict = {user[0]: num + 1 for num, user in enumerate(top_list)}
            return top_dict[self.username]
        else:
            return '-'

    @property
    def pic_exist(self):
        try:
            response = requests.get(self.profile_pic.url)
        except Exception:
            return False
        else:
            return True if response.status_code == 200 else False
