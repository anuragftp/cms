# Generated by Django 3.2.8 on 2021-12-27 15:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_rename_assignpaper_paperassign'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Review',
            new_name='Reviewer',
        ),
    ]
