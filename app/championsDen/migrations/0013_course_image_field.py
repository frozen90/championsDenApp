# Generated by Django 3.0.1 on 2020-04-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championsDen', '0012_auto_20200421_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image_field',
            field=models.ImageField(default='static/images/course_logo.png', height_field=340, upload_to='courses_logo/', width_field=240),
        ),
    ]
