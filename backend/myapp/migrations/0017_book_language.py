# Generated by Django 4.2.18 on 2025-02-13 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_language_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ManyToManyField(to='myapp.language'),
        ),
    ]
