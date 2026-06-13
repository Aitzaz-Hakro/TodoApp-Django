from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def clear_tasks(apps, schema_editor):
    Task = apps.get_model('TodoApp', 'Task')
    Task.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TodoApp', '0002_user'),
    ]

    operations = [
        migrations.RunPython(clear_tasks, migrations.RunPython.noop),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='tasks',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
