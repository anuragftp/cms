# Generated by Django 3.2.8 on 2022-01-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220102_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='is_review_submit',
            field=models.BooleanField(default=False),
        ),
    ]
