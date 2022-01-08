# Generated by Django 3.2.8 on 2022-01-07 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_updated_on_paper_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paper',
            name='review_by',
            field=models.IntegerField(null=True),
        ),
    ]