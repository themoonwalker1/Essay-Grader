# Generated by Django 3.0.6 on 2020-06-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grader_app', '0003_auto_20200604_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='marked_body',
            field=models.TextField(default=''),
        ),
    ]