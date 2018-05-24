# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.IntegerField()),
                ('volume', models.DecimalField(max_digits=64, decimal_places=4)),
                ('price', models.DecimalField(max_digits=32, decimal_places=8)),
            ],
            options={
                'ordering': ('time',),
            },
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='history',
            name='symbol',
            field=models.ForeignKey(to='binance_feed.Symbol'),
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together=set([('symbol', 'time')]),
        ),
    ]
