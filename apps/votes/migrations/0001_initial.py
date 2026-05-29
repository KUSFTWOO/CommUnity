# Generated migration for votes app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('expires_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='polls', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PollOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('votes_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='votes.poll')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votes', to='votes.polloption')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='votes.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='polloption',
            index=models.Index(fields=['poll'], name='votes_pollo_poll_id_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='poll',
            index=models.Index(fields=['created_by'], name='votes_poll_created_by_id_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='poll',
            index=models.Index(fields=['expires_at'], name='votes_poll_expires_at_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='vote',
            index=models.Index(fields=['poll', 'user'], name='votes_vote_poll_id_user_id_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='vote',
            index=models.Index(fields=['user'], name='votes_vote_user_id_123456_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('poll', 'user')},
        ),
    ]
