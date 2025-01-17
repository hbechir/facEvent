# Generated by Django 5.0.4 on 2024-05-02 14:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('club', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('started', 'Started'), ('delayed', 'Delayed'), ('ended', 'Ended')], default='pending', max_length=10)),
                ('starting_date_time', models.DateTimeField()),
                ('ending_date_time', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('max_attendees', models.IntegerField()),
                ('event_type', models.CharField(choices=[('private', 'Private'), ('public', 'Public')], default='public', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('organizing_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.club')),
            ],
        ),
    ]
