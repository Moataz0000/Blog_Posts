# Generated by Django 5.0.4 on 2024-04-12 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
