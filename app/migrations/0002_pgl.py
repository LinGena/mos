# Generated by Django 4.2.4 on 2023-08-10 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pgl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_id', models.IntegerField()),
                ('activity_id', models.IntegerField()),
                ('pgl', models.FloatField()),
            ],
            options={
                'db_table': 'pgl',
                'managed': False,
            },
        ),
    ]