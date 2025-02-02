# Generated by Django 3.2.7 on 2024-06-18 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Onlinesms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='genz_database',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('identification_number', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('avatar', models.ImageField(default='avatars/profile.png', upload_to='avatars/')),
            ],
        ),
    ]
