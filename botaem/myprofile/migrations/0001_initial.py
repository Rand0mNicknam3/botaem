# Generated by Django 5.1.2 on 2024-11-23 09:50

import django.core.validators
import myprofile.utils
import myprofile.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, default='FAANG Senior developer 18 y.o.', max_length=250, validators=[django.core.validators.MaxLengthValidator(250)])),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='default_images/profile.jpg', null=True, upload_to=myprofile.utils.profile_image_path, validators=[myprofile.validators.validate_image_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])),
                ('slug', models.SlugField(max_length=250, unique=True, verbose_name='URL')),
            ],
        ),
    ]
