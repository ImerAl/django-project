# Generated by Django 4.2 on 2023-05-15 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyflow', '0011_cut_off'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyinformation',
            name='pay_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
