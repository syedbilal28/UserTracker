# Generated by Django 3.1.4 on 2020-12-04 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserTracker', '0006_auto_20201204_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyBarGraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bar_graph', models.ImageField(blank=True, upload_to='BarGraphs')),
            ],
        ),
    ]