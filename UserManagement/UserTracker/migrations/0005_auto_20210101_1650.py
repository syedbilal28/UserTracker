# Generated by Django 3.1.4 on 2021-01-01 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserTracker', '0004_auto_20210101_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contact_number',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
