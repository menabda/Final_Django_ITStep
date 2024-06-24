# Generated by Django 5.0.6 on 2024-06-24 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_author_alter_book_author'),
        ('countries_plus', '0005_auto_20160224_1804'),
        ('languages_plus', '0004_auto_20171214_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', to='countries_plus.country'),
        ),
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='languages_plus.language'),
        ),
    ]