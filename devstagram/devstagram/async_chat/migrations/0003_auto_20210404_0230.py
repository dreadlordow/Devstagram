# Generated by Django 3.1.7 on 2021-04-03 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0020_userfriends'),
        ('async_chat', '0002_auto_20210404_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmessage',
            name='post_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.picture'),
        ),
    ]