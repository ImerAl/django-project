# Generated by Django 4.2 on 2023-05-15 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moneyflow', '0003_moneyinformation_pay_date_cut_off'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyinformation',
            name='pay_date',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
