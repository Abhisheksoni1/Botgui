# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binance_feed', '0002_auto_20180510_1127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='history',
            unique_together=set([]),
        ),
    ]
