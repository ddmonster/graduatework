# Generated by Django 2.2.1 on 2019-05-24 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartinfo', '0003_order_goods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='goods',
            field=models.ManyToManyField(related_name='goods', to='commodity.Goods'),
        ),
    ]
