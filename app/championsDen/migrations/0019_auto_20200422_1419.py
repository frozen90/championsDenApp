# Generated by Django 3.0.1 on 2020-04-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championsDen', '0018_course_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image_field',
            field=models.ImageField(upload_to='static/courses_logo/'),
        ),
    ]