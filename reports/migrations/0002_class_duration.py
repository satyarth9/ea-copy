# Generated by Django 3.0.4 on 2020-10-05 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='duration',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]