# Generated by Django 2.0.9 on 2019-05-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0005_auto_20190511_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
