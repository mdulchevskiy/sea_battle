# Generated by Django 3.0.7 on 2020-06-16 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sea_battle', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='user_ip',
            new_name='user_session_key',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='ip',
            new_name='session_key',
        ),
    ]
