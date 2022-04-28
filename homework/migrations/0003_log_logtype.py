# Generated by Django 3.2.3 on 2022-04-27 19:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0002_alter_execution_appraise_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('finish_time', models.DateTimeField(null=True)),
                ('execution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homework.execution')),
                ('log_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homework.logtype')),
            ],
        ),
    ]