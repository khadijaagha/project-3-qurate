# Generated by Django 4.2.2 on 2023-06-22 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_comment_parent_user_likes_comment_likes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_likes',
            old_name='comment_likes',
            new_name='comments',
        ),
        migrations.RenameField(
            model_name='user_likes',
            old_name='post_likes',
            new_name='posts',
        ),
    ]
