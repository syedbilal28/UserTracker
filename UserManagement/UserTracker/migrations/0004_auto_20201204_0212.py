# Generated by Django 3.1.4 on 2020-12-03 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserTracker', '0003_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='temperature',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Temperature',
        ),
    ]