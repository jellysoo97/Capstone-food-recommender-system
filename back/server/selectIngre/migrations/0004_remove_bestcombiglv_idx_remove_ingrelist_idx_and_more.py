# Generated by Django 4.0.4 on 2022-05-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selectIngre', '0003_remove_vegetype_idx_alter_vegetype_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bestcombiglv',
            name='idx',
        ),
        migrations.RemoveField(
            model_name='ingrelist',
            name='idx',
        ),
        migrations.AlterField(
            model_name='bestcombiglv',
            name='id',
            field=models.IntegerField(blank=True, db_column='ID', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ingrelist',
            name='id',
            field=models.IntegerField(blank=True, db_column='ID', primary_key=True, serialize=False),
        ),
    ]
