# Generated by Django 5.0.3 on 2024-04-15 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0018_remove_gereratingexam_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='gereratingexam',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
