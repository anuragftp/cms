# Generated by Django 3.2.8 on 2022-01-03 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20220103_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='rating',
        ),
    ]