# Generated by Django 4.0.3 on 2022-03-25 14:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='author_issue', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('LOW', 'low'), ('MEDIUM', 'medium'), ('HIGH', 'high')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('TO DO', 'to do'), ('IN PROGRESS', 'in progress'), ('DONE', 'done')], max_length=128),
        ),
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('BUG', 'bug'), ('IMPROVE', 'improve'), ('TASK', 'task')], max_length=128),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('BACK-END', 'back-end'), ('FRONT-END', 'front-end'), ('iOS', 'iOS'), ('ANDROID', 'Android')], max_length=128),
        ),
    ]