# Generated by Django 4.2.5 on 2023-09-25 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskphoto',
            name='photo',
            field=models.FileField(upload_to='task_photos/'),
        ),
    ]
