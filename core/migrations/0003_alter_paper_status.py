# Generated by Django 3.2.8 on 2022-01-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_paper_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='status',
            field=models.CharField(default='Submitted', max_length=30),
        ),
    ]
