# Generated by Django 3.1.4 on 2021-02-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20210210_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
