# Generated by Django 2.1.7 on 2019-07-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocess', '0017_auto_20190725_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelMeta',
            fields=[
                ('type', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('last_date', models.DateTimeField(auto_now_add=True)),
                ('accuracy', models.DecimalField(decimal_places=2, max_digits=5)),
                ('MAE', models.DecimalField(decimal_places=2, max_digits=5)),
                ('training_num', models.IntegerField(default=0)),
                ('test_num', models.IntegerField(default=0)),
            ],
        ),
    ]