# Generated by Django 5.1.3 on 2024-11-20 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuposi', '0004_registrations_session_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Giga_chat_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giga_name', models.CharField(max_length=100)),
                ('giga_surname', models.CharField(max_length=100)),
                ('giga_age', models.CharField(max_length=10)),
                ('giga_height', models.CharField(max_length=10)),
                ('giga_photo', models.CharField(max_length=1000)),
            ],
        ),
    ]