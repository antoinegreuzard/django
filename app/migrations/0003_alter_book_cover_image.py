# Generated by Django 5.0.2 on 2024-03-07 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_author_photo_alter_book_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
