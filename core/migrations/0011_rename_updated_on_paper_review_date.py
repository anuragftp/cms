# Generated by Django 3.2.8 on 2022-01-03 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_paper_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper',
            old_name='updated_on',
            new_name='review_date',
        ),
    ]
