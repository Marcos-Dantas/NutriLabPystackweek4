# Generated by Django 4.0.6 on 2022-07-06 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_ativacao_activation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activation',
            old_name='ativo',
            new_name='active',
        ),
    ]