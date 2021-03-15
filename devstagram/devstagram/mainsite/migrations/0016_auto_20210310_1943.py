# Generated by Django 3.1.7 on 2021-03-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0015_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='pictures'),
        ),
        migrations.AlterField(
            model_name='profilepicture',
            name='image',
            field=models.ImageField(default='media/profile_pictures/default.png', upload_to='profile_pictures'),
        ),
    ]
