# Generated by Django 3.2.3 on 2022-04-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20220427_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='price',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
