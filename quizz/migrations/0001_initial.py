# Generated by Django 3.0.3 on 2020-05-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longesity', models.IntegerField()),
                ('discount_type', models.CharField(max_length=30)),
                ('discount_rate', models.IntegerField()),
                ('npv', models.FloatField()),
                ('irr', models.IntegerField()),
                ('pi', models.IntegerField()),
            ],
        ),
    ]
