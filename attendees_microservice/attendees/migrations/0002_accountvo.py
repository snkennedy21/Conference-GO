# Generated by Django 4.0.3 on 2022-08-24 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountVO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
