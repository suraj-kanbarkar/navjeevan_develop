# Generated by Django 2.1.5 on 2020-06-29 15:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TeacherStu', '0003_stu_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='stu_task',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
