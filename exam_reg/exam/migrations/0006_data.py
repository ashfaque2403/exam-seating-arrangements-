# Generated by Django 5.0.3 on 2024-04-03 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_rename_subject_name_subject_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('row_number', models.IntegerField()),
                ('column_number', models.IntegerField()),
            ],
        ),
    ]
