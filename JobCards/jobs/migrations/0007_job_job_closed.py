# Generated by Django 3.1.4 on 2021-02-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20210205_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_closed',
            field=models.BooleanField(default=False),
        ),
    ]