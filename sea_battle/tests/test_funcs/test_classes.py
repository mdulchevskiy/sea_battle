from django.test import TestCase
from sea_battle.tests.test_funcs.test_converting import normal_field
from sea_battle.funcs import (UserGameInfo,
                              WinGame, )
from sea_battle.models import (Game,
                               User, )


class SeaBattleProfilePageClassesTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            username='mdulchevskiy',
            password='1111111111',
            first_name='Maxim',
            last_name='Dulchevskiy',
            email='',
            phone_number='+375(29)111-11-11',
        )
        User.objects.create(
            username='rsanchez',
            password='1111111111',
            first_name='Rick',
            last_name='Sanchez',
            email='',
            phone_number='+375(29)111-11-11',
        )
        User.objects.create(
            username='msmith',
            password='1111111111',
            first_name='Morty',
            last_name='Smith',
            email='',
            phone_number='+375(29)111-11-11',
        )
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user_type = ['Guest', 'User', 'User', 'User', 'User', 'User']
        user = [None, user1, user1, user1, user1, user2]
        status = ['Win', 'Win', 'Win', 'Lose', 'Aborted', 'Win']
        moves = [60, 33, 40, 50, 20, 20]
        points = [50, 100, 255, 0, 0, 350]
        hits = [20, 20, 20, 10, 16, 20]
        sunks = [10, 10, 10, 4, 9, 10]
        accuracy = [0.3, 0.6, 0.5, 0.2, 0.8, 1]
        for i in range(len(user_type)):
            Game.objects.create(
                user_type=user_type[i],
                user=user[i],
                status=status[i],
                moves=moves[i],
                points=points[i],
                hits=hits[i],
                sunks=sunks[i],
                accuracy=accuracy[i],
                player_field='empty',
                player_field_with_enemy_moves='empty',
                enemy_field='empty',
                enemy_field_with_player_moves='empty',
                messages='no messages',
            )
        for i in range(7, 1, -1):
            Game.objects.create(
                status='Win',
                moves=i*10,
                points=i*10,
                player_field=normal_field,
                enemy_field=normal_field,
                enemy_field_with_player_moves=normal_field,
                player_field_with_enemy_moves=normal_field,
                messages='no message',
            )

    def test_win_game_class(self):
        """Провекра корректности работы класса "WinGame"."""
        game = Game.objects.filter(id=9).first()
        win_game_object = WinGame(game)
        self.assertFalse(win_game_object.user)
        self.assertEqual(win_game_object.username, 'Guest_000009')
        self.assertIsNone(win_game_object.rank)
        win_game_object.set_rank(3)
        self.assertEqual(win_game_object.rank, 3)

    def test_usergameinfo_class_creation(self):
        """Проверка корректности создания класса "UserGameInfo"."""
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.id, user.id)
        self.assertEqual(user_info.username, user.username)
        self.assertEqual(user_info.first_name, user.first_name)
        self.assertEqual(user_info.last_name, user.last_name)
        self.assertEqual(user_info.email, user.email)
        self.assertEqual(user_info.phone_number, user.phone_number)
        self.assertEqual(user_info.date, user.registration_date)
        self.assertEqual(user_info.profile_pic, user.profile_pic)
        self.assertEqual(user_info.login, user.login)

    def test_usergameinfo_class_all_games_method(self):
        """Проверка корректности работы метода "all_games".

        Проверка работы метода "all_games", возвращающего список объектов всех игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        all_games = [Game.objects.get(id=2), Game.objects.get(id=3), Game.objects.get(id=4)]
        self.assertEqual(list(user_info.all_games()), all_games)

    def test_usergameinfo_class_win_games_method(self):
        """Проверка корректности работы метода "win_games".

        Проверка работы метода "win_games", возвращающего список объектов всех победных игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        all_games = [Game.objects.get(id=2), Game.objects.get(id=3)]
        self.assertEqual(list(user_info.win_games()), all_games)

    def test_usergameinfo_class_battles_method(self):
        """Проверка корректности работы метода "battles".

        Проверка работы метода "battles", возвращающего количество всех игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.battles, 3)

    def test_usergameinfo_class_victories_method(self):
        """Проверка корректности работы метода "victories".

        Проверка работы метода "victories", возвращающего количество всех победных игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.victories, 2)

    def test_usergameinfo_class_victories_pct_first_format_method(self):
        """Проверка корректности работы метода "victories_pct_first_format".

        Проверка работы метода "victories_pct_first_format",
        возвращающего процент всех победных игр игрока в формате "00%".
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.victories_pct_first_format, '67%')

    def test_usergameinfo_class_victories_pct_second_format_method(self):
        """Проверка корректности работы метода "victories_pct_second_format".

        Проверка работы метода "victories_pct_second_format",
        возвращающего процент всех победных игр игрока в формате "00.00%".
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.victories_pct_second_format, '66.67%')

    def test_usergameinfo_class_defeats_method(self):
        """Проверка корректности работы метода "defeats".

        Проверка работы метода "defeats", возвращающего количество всех поражений игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.defeats, 1)

    def test_usergameinfo_class_defeats_pct_method(self):
        """Проверка корректности работы метода "defeats_pct".

        Проверка работы метода "defeats_pct", возвращающего процент
        всех поражений игрока в формате "00.00%".
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.defeats_pct, '33.33%')

    def test_usergameinfo_class_destroyed_warships_method(self):
        """Проверка корректности работы метода "destroyed_warships".

        Проверка работы метода "destroyed_warships", возвращающего количество
        всех потопленых игроком кораблей противника.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.destroyed_warships, 24)

    def test_usergameinfo_class_accuracy_first_format_method(self):
        """Проверка корректности работы метода "accuracy_first_format".

        Проверка работы метода "accuracy_first_format",
        возвращающего точность попаданий игрока в формате "00%".
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.accuracy_first_format, '43%')

    def test_usergameinfo_class_accuracy_second_format_method(self):
        """Проверка корректности работы метода "accuracy_second_format".

        Проверка работы метода "accuracy_second_format",
        возвращающего точность попаданий игрока в формате "00.00%".
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.accuracy_second_format, '43.33%')

    def test_usergameinfo_class_last_five_battles_method(self):
        """Проверка корректности работы метода "last_five_battles".

        Проверка работы метода "last_five_battles", возвращающего
        список объектов последних пяти игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        last_five_battles = [Game.objects.get(id=4), Game.objects.get(id=3), Game.objects.get(id=2)]
        self.assertEqual(list(user_info.last_five_battles), last_five_battles)

    def test_usergameinfo_class_amount_of_last_five_battles_method(self):
        """Проверка корректности работы метода "amount_of_last_five_battles".

        Проверка работы метода "amount_of_last_five_battles", возвращающего
        количество последних игр игрока (не более 5).
        Необходим для html верстки таблицы последних игр игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.amount_of_last_five_battles, 3)

    def test_usergameinfo_class_best_game_method(self):
        """Проверка корректности работы метода "best_game".

        Проверка работы метода "best_game", возвращающего
        максимальное количество когда-либо набранных игроком очков.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.best_game, 255)

    def test_usergameinfo_class_fastest_game_method(self):
        """Проверка корректности работы метода "fastest_game".

        Проверка работы метода "fastest_game", возвращающего
        минимальное количество ходов, за которое игрок завершал игру.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.fastest_game, 33)

    def test_usergameinfo_class_best_accuracy_method(self):
        """Проверка корректности работы метода "best_accuracy".

        Проверка работы метода "best_accuracy", возвращающего
        максимальную точность игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.best_accuracy, '60.00%')

    def test_usergameinfo_class_rank_method_case_1(self):
        """Проверка корректности работы метода "rank". Ч.1

        Проверка работы метода "rank", возвращающего рейтинг игрока.
        """
        user = User.objects.filter().first()
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.rank, 2)

    def test_usergameinfo_class_rank_method_case_2(self):
        """Проверка корректности работы метода "rank". Ч.2

        Проверка работы метода "rank", возвращающего рейтинг игрока,
        когда им еще не было сыграно ни одной игры.
        """
        user = User.objects.get(id=3)
        user_info = UserGameInfo(user)
        self.assertEqual(user_info.rank, '-')
