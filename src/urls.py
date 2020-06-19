from django.contrib import admin
from django.urls import path
from sea_battle.views import (sign_in,
                              registration,
                              account_page,
                              home_page,
                              preparation_page,
                              game_page, )


urlpatterns = [
    path('secret_admin/', admin.site.urls),
    path('sign_in/', sign_in, name='sign_in'),
    path('registration/', registration, name='registration'),
    path('account/<str:username>', account_page, name='account_page'),
    path('account/', account_page, name='account_page'),
    path('', home_page, name='home_page'),
    path('preparation/', preparation_page, name='preparation_page'),
    path('game/', game_page, name='game_page'),
]
