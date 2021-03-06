# Generated by Django 2.2.2 on 2019-07-03 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0003_auto_20190702_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='pending',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EditedMeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b', models.FloatField(default=0)),
                ('l', models.FloatField(default=0)),
                ('d', models.FloatField(default=0)),
                ('meal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='meal.Meal')),
            ],
        ),
    ]
