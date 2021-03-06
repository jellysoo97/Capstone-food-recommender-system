# Generated by Django 4.0.4 on 2022-05-24 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(default='', max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('sex', models.BooleanField(default=False)),
                ('age', models.SmallIntegerField(default='')),
                ('health', models.CharField(default='없을 무', max_length=128)),
                ('vegtype', models.TextField(default='[]', max_length=128)),
                ('allergic', models.TextField(default='[]', max_length=128)),
            ],
        ),
    ]
