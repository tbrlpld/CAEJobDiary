# Generated by Django 2.0.9 on 2019-08-19 17:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0009_auto_20190811_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(message='Tag must start with `#` (hashsymbol) and only contain numbers and letters. Spaces and punctuation are not allowed.', regex='^#[a-zA-Z0-9]*$')])),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='tags',
            field=models.ManyToManyField(blank=True, to='diary.Tag'),
        ),
    ]