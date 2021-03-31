# Generated by Django 3.1.4 on 2021-02-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('blog_file', models.FileField(upload_to='blogs/%Y/%m/%d')),
                ('blog_title', models.CharField(max_length=50, unique=True)),
                ('blog_post_date', models.DateField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
