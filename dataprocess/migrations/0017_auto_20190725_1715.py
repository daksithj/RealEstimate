# Generated by Django 2.1.7 on 2019-07-25 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0016_backlogentries_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proclanddata',
            name='aesthetic',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='days_since',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='highway',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='hospital',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='paddy',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='quarry',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='rubber',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='school',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='supermarket',
        ),
        migrations.RemoveField(
            model_name='proclanddata',
            name='temple',
        ),
    ]
