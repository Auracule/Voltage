# Generated by Django 4.0.5 on 2022-07-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_shopcart_name_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='name_id',
            field=models.CharField(blank=True, default='a', max_length=20, null=True),
        ),
    ]
