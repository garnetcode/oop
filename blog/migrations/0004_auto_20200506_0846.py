# Generated by Django 2.2 on 2020-05-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200506_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='scene',
            field=models.ImageField(default='hit.png', null=True, upload_to='scenes/'),
        ),
    ]