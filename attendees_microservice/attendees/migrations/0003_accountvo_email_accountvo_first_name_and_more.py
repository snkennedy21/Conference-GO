# Generated by Django 4.0.3 on 2022-08-25 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_accountvo'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountvo',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='accountvo',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='accountvo',
            name='is_active',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='accountvo',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='accountvo',
            name='updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]