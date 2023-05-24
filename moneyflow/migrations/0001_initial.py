# Generated by Django 4.2 on 2023-04-23 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(default='0000000000', max_length=10)),
                ('insert_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneralCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('insert_date', models.DateField()),
                ('done_date', models.DateField()),
                ('transaction_type', models.BooleanField()),
                ('description', models.TextField()),
                ('detained', models.BooleanField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moneyflow.batch')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moneyflow.generalcategory')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moneyflow.typec')),
            ],
        ),
    ]
