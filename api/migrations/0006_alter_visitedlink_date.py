# Generated by Django 3.2.6 on 2021-08-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_visitedlink_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitedlink',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
