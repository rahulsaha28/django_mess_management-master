# Generated by Django 2.2.2 on 2019-07-01 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bazar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cradit_tk', models.FloatField(default=0)),
                ('activate', models.BooleanField(default=False)),
                ('date_created', models.DateField()),
            ],
        ),
    ]
