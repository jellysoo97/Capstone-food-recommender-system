# Generated by Django 4.0.4 on 2022-05-23 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IngreGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.TextField(blank=True, db_column='GROUP', null=True)),
                ('sub_igrdt', models.TextField(blank=True, db_column='SUB_IGRDT', null=True)),
            ],
            options={
                'db_table': 'ingre_group',
                'managed': True,
            },
        ),
    ]
