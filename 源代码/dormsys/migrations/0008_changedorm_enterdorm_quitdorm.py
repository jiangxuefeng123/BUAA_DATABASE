# Generated by Django 3.1.1 on 2020-12-12 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormsys', '0007_auto_20201212_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeDorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=20)),
                ('room_number', models.CharField(max_length=20)),
                ('region', models.CharField(max_length=20)),
                ('tutor_number', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('apply_time', models.DateTimeField()),
                ('deal_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='EnterDorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=20)),
                ('room_number', models.CharField(max_length=20)),
                ('region', models.CharField(max_length=20)),
                ('tutor_number', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('apply_time', models.DateTimeField()),
                ('deal_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='QuitDorm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=20)),
                ('room_number', models.CharField(max_length=20)),
                ('region', models.CharField(max_length=20)),
                ('tutor_number', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('apply_time', models.DateTimeField()),
                ('deal_time', models.DateTimeField()),
            ],
        ),
    ]
