# Generated by Django 5.0 on 2024-04-01 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
    ]
