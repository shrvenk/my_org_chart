# Generated by Django 2.2.11 on 2020-03-15 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orgchart', '0012_auto_20200315_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='manager',
        ),
    ]
