# Generated by Django 3.1.7 on 2021-03-06 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0012_friendrequest_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='upload_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]