# Generated by Django 3.2.8 on 2021-10-31 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_auto_20211031_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='author_status',
            field=models.BooleanField(null=True),
        ),
    ]