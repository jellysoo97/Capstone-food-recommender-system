# Generated by Django 3.2.13 on 2022-06-10 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('firstPreference', '0003_auto_20220610_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('recipe_id', models.IntegerField()),
                ('ratings', models.FloatField(null=True)),
            ],
        ),
    ]
