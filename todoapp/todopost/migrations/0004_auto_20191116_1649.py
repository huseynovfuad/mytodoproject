# Generated by Django 2.2.7 on 2019-11-16 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todopost', '0003_auto_20191116_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='finished',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 13, 49, 40, 736206, tzinfo=utc)),
        ),
    ]