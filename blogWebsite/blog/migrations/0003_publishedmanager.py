# Generated by Django 2.0.5 on 2019-04-20 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190419_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishedManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]