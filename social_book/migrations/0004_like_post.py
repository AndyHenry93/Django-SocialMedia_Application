# Generated by Django 4.1 on 2022-10-07 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_book', '0003_rename_user_name_post_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like_Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
    ]
