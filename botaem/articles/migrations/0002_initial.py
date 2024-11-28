# Generated by Django 5.1.2 on 2024-11-23 09:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article_likes',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='articles.article'),
        ),
        migrations.AddField(
            model_name='article_likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article_params',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='params', to='articles.article'),
        ),
        migrations.AddField(
            model_name='article_read_later',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_later', to='articles.article'),
        ),
        migrations.AddField(
            model_name='article_read_later',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_later_articles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article_params',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='articles.topic'),
        ),
    ]
