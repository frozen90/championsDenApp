# Generated by Django 3.0.1 on 2020-04-25 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('championsDen', '0026_feedback_feeback_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='grade',
            field=models.CharField(choices=[('Excellent', 'A'), ('Overall Good', 'B'), ('Poor', 'C'), ('Very Poor', 'D')], max_length=13, null=True),
        ),
    ]