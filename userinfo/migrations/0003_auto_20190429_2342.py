# Generated by Django 2.1.7 on 2019-04-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_auto_20190429_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='uname',
            field=models.CharField(max_length=50, unique=True, verbose_name='用户名'),
        ),
    ]
