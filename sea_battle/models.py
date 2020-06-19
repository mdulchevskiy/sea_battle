from django.db import models
from django.db.models import SET_NULL


class User(models.Model):
    username = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=17, default=None)
    login = models.IntegerField(default=0)
    session_key = models.CharField(max_length=255, null=True)
    registration_date = models.DateField(auto_now_add=True)
    last_activity_date = models.DateTimeField(null=True)
    profile_pic = models.ImageField(null=True)

    def __str__(self):
        return f'{self.pk}: {self.username}'


class Game(models.Model):
    user_type = models.CharField(max_length=255, default='Guest')
    user = models.ForeignKey('User', null=True, on_delete=SET_NULL, related_name='games')
    user_session_key = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default='Started')
    game_date = models.DateTimeField(auto_now_add=True)
    moves = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    sunks = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    player_field = models.CharField(max_length=255)
    player_field_with_enemy_moves = models.CharField(max_length=255)
    enemy_field = models.CharField(max_length=255)
    enemy_field_with_player_moves = models.CharField(max_length=255)
    messages = models.CharField(max_length=2040)

    def __str__(self):
        return f'Game {self.pk}'
