# Generated by Django 4.1.2 on 2022-12-07 22:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_user_is_staff_alter_user_is_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
    ]