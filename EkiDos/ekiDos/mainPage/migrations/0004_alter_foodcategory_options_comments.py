# Generated by Django 4.2.7 on 2023-11-28 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainPage', '0003_foodcategory_anchor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodcategory',
            options={'verbose_name': 'Категория ФастФуда', 'verbose_name_plural': 'Категории ФастФуда'},
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
