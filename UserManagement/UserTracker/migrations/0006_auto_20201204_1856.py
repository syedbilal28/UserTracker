# Generated by Django 3.1.4 on 2020-12-04 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserTracker', '0005_auto_20201204_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='login',
            old_name='user',
            new_name='profile',
        ),
    ]