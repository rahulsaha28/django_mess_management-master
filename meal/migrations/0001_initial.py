# Generated by Django 2.2.2 on 2019-07-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultMeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b', models.FloatField(default=0)),
                ('l', models.FloatField(default=0)),
                ('d', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b', models.FloatField(default=0)),
                ('l', models.FloatField(default=0)),
                ('d', models.FloatField(default=0)),
                ('date_of_creation', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
