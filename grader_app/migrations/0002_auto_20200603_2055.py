# Generated by Django 3.0.6 on 2020-06-04 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='marked_body',
            field=models.TextField(default=models.TextField()),
        ),
    ]
