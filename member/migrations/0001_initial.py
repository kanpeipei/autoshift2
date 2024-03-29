# Generated by Django 2.2.6 on 2019-12-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('age', models.IntegerField(verbose_name='age')),
                ('partner_number', models.IntegerField(unique=True, verbose_name='partner_number')),
                ('hourly_pay', models.IntegerField(verbose_name='hourly_pay')),
                ('is_counter', models.BooleanField(verbose_name='is_counter')),
                ('is_fryer', models.BooleanField(verbose_name='is_fryer')),
                ('is_kitchen', models.BooleanField(verbose_name='is_kitchen')),
                ('is_smg', models.BooleanField(verbose_name='is_smg')),
                ('is_opener', models.BooleanField(verbose_name='is_opener')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
            ],
            options={
                'db_table': 'members',
            },
        ),
    ]
