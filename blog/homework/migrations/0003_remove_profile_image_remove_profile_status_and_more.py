# Generated by Django 4.0.1 on 2022-02-08 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0002_profile_image_profile_status_alter_profile_user_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='image',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='status',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
