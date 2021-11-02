# Generated by Django 2.1.7 on 2019-03-24 12:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webscrape', '0003_auto_20190323_1501'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcLandData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, null=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('land_type', models.CharField(max_length=20, null=True)),
                ('land_size', models.FloatField(default=0, null=True)),
                ('land_availability', models.BooleanField(default=0)),
                ('date_collected', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('raw', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='webscrape.RawLandData')),
            ],
        ),
    ]
