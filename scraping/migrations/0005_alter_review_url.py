# Generated by Django 3.2.8 on 2021-10-31 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_auto_20211031_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='url',
            field=models.CharField(max_length=250),
        ),
    ]
