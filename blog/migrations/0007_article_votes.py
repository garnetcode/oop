# Generated by Django 2.2 on 2020-05-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200506_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]
