# Generated by Django 3.2 on 2023-04-07 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_delete_genretitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id']},
        ),
    ]
