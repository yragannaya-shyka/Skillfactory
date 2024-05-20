# Generated by Django 5.0.4 on 2024-05-20 08:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_portal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_type',
            new_name='name',
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('AR', 'Статья'), ('NW', 'Новость')], default='AR', max_length=2)),
                ('public_date', models.DateTimeField(auto_now_add=True)),
                ('topic', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('public_date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_portal.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(through='news_portal.PostCategory', to='news_portal.category'),
        ),
    ]
