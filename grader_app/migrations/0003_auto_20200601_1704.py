# Generated by Django 3.0.6 on 2020-06-01 21:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grader_app', '0002_auto_20200601_1026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essay',
            name='email',
        ),
        migrations.AlterField(
            model_name='essay',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='student',
            field=models.BooleanField(default=False),
        ),
    ]