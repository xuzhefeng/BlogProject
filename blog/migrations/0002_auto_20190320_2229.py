# Generated by Django 2.1.5 on 2019-03-20 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'verbose_name_plural': '博客表'},
        ),
        migrations.AlterModelOptions(
            name='blogtype',
            options={'verbose_name_plural': '博客分类表'},
        ),
        migrations.RenameField(
            model_name='blogtype',
            old_name='title',
            new_name='name',
        ),
    ]
