# Generated by Django 4.0.2 on 2022-02-25 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0006_attendance_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='attendance',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.types'),
        ),
    ]