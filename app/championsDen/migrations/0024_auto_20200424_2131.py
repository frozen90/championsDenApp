# Generated by Django 3.0.1 on 2020-04-24 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('championsDen', '0023_auto_20200424_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='body',
            field=models.TextField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='new_message',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(choices=[('BR1', 'Brazil'), ('EUN1', 'EU Nordic East'), ('EUW1', 'EU West'), ('JP1', 'Japan'), ('KR', 'Korea'), ('LA1', 'Latin America 1'), ('LA2', 'Latin America 2'), ('NA1', 'North America'), ('OC1', 'Oceania'), ('TR1', 'Turkey'), ('RU', 'Russia')], max_length=7, null=True)),
                ('feedback_given', models.BooleanField(default=False)),
                ('feedback_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback_receiver', to=settings.AUTH_USER_MODEL)),
                ('feedback_sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]