# Generated by Django 4.2.7 on 2023-11-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0007_remove_comments_liked_by_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
