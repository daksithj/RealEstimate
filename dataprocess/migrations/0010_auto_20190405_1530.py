# Generated by Django 2.1.7 on 2019-04-05 15:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0009_prochousedata_km'),
    ]

    operations = [
        migrations.CreateModel(
            name='BacklogEntries',
            fields=[
                ('search_no', models.IntegerField(primary_key=True, serialize=False)),
                ('search_type', models.IntegerField(default=0)),
                ('date_searched', models.DateTimeField(default=datetime.datetime(2019, 4, 5, 15, 30, 12, 400421))),
            ],
        ),
        migrations.CreateModel(
            name='HouseBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, null=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('bedrooms', models.IntegerField(default=1, null=True)),
                ('bathrooms', models.IntegerField(default=1, null=True)),
                ('floor_area', models.FloatField(default=0, null=True)),
                ('floors', models.IntegerField(default=1, null=True)),
                ('parking', models.IntegerField(default=0, null=True)),
                ('land_size', models.FloatField(default=0, null=True)),
                ('land_availability', models.CharField(max_length=20, null=True)),
                ('water', models.IntegerField(default=0, null=True)),
                ('overhead', models.IntegerField(default=0, null=True)),
                ('garage', models.IntegerField(default=0, null=True)),
                ('p_garden', models.IntegerField(default=0, null=True)),
                ('servant', models.IntegerField(default=0, null=True)),
                ('hot_water', models.IntegerField(default=0, null=True)),
                ('electricity', models.IntegerField(default=0, null=True)),
                ('ac_rooms', models.IntegerField(default=0, null=True)),
                ('luxury', models.IntegerField(default=0, null=True)),
                ('security', models.IntegerField(default=0, null=True)),
                ('roof_garden', models.IntegerField(default=0, null=True)),
                ('in_garden', models.IntegerField(default=0, null=True)),
                ('furnished', models.IntegerField(default=0, null=True)),
                ('pool', models.IntegerField(default=0, null=True)),
                ('colonial', models.IntegerField(default=0, null=True)),
                ('front', models.IntegerField(default=0, null=True)),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.BacklogEntries')),
            ],
        ),
        migrations.CreateModel(
            name='LandBacklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, null=True)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('land_size', models.FloatField(default=0, null=True)),
                ('land_availability', models.BooleanField(default=0)),
                ('coconut', models.IntegerField(default=0)),
                ('tea', models.IntegerField(default=0)),
                ('cultivated', models.IntegerField(default=0)),
                ('beach', models.IntegerField(default=0)),
                ('utilities', models.IntegerField(default=0)),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataprocess.BacklogEntries')),
            ],
        ),
        migrations.RemoveField(
            model_name='tempproclanddata',
            name='raw',
        ),
        migrations.DeleteModel(
            name='TempProcLandData',
        ),
    ]
