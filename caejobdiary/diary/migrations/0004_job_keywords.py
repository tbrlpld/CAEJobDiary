# Generated by Django 2.0.9 on 2019-05-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0003_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='keywords',
            field=models.ManyToManyField(to='diary.Keyword'),
        ),
    ]
