# Generated by Django 3.0.1 on 2020-04-22 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championsDen', '0013_course_image_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image_field',
            field=models.ImageField(default='static/images/course_logo.png', height_field=340, upload_to='static/courses_logo/', width_field=240),
        ),
    ]