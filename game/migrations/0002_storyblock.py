# Generated by Django 3.0.8 on 2020-11-13 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_text', models.TextField()),
                ('story', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question_story', to='game.Question')),
            ],
        ),
    ]