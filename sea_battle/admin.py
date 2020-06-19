from django.contrib import admin
from django.contrib.sessions.models import Session
from sea_battle.models import (Game,
                               User, )


admin.site.register(User)
admin.site.register(Game)
admin.site.register(Session)
