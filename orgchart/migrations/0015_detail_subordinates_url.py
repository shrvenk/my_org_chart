# Generated by Django 2.2.11 on 2020-03-15 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orgchart', '0014_auto_20200315_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='subordinates_url',
            field=models.TextField(null=True),
        ),
    ]
