# Generated by Django 5.1.2 on 2024-12-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0003_clientinfo_model_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinfo',
            name='model_file',
            field=models.CharField(default='', max_length=300),
        ),
    ]
