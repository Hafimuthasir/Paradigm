# Generated by Django 4.0.6 on 2022-12-24 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0017_alter_posts_discount_price_alter_posts_is_premium_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='discount_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='posts',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
