# Generated by Django 3.1.1 on 2020-12-12 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dormsys', '0016_auto_20201212_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='approval',
            old_name='student_name',
            new_name='name',
        ),
    ]
