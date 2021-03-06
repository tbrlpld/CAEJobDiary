# Generated by Django 2.0.9 on 2019-08-11 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0008_auto_20190520_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='job',
            name='logfile_path',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='job',
            name='readme_filename',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='job',
            name='solver',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='job',
            name='sub_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='job',
            name='sub_dir',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='job',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
