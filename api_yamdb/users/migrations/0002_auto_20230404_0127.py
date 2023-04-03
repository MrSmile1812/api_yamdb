# Generated by Django 3.2 on 2023-04-03 22:27

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='conformition_code',
            new_name='confirmation_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[users.validators.UnicodeUsernameValidator()], verbose_name='Username'),
        ),
    ]
