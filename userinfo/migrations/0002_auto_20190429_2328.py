# Generated by Django 2.1.7 on 2019-04-29 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adress',
            name='user',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='addr',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userinfo.Adress'),
        ),
        migrations.AlterField(
            model_name='adress',
            name='ads',
            field=models.CharField(default='null', max_length=300, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='adress',
            name='aname',
            field=models.CharField(default='null', max_length=50, verbose_name='收货人'),
        ),
        migrations.AlterField(
            model_name='adress',
            name='phone',
            field=models.CharField(default='null', max_length=20, verbose_name='电话'),
        ),
    ]
