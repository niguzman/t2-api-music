# Generated by Django 3.1.7 on 2021-05-02 04:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210502_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='genre',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator('^[a-zA-Z]*$', 'Only characters are allowed.')]),
        ),
    ]
