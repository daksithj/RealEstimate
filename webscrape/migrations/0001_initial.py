# Generated by Django 2.1.7 on 2019-03-22 09:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawLandData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0)),
                ('price_type', models.CharField(max_length=10)),
                ('location1', models.CharField(max_length=30)),
                ('location2', models.CharField(max_length=30)),
                ('land_type', models.CharField(max_length=20)),
                ('land_size', models.FloatField(default=0)),
                ('land_availability', models.CharField(max_length=20)),
                ('heading', models.TextField()),
                ('about', models.TextField()),
                ('date_collected', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
