# Generated by Django 3.2.3 on 2022-04-27 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_entity_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='cover_img',
            field=models.ImageField(blank=True, default='profiles/user-default.png', null=True, upload_to='profiles/'),
        ),
    ]
