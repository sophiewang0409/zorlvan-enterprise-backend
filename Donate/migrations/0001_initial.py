# Generated by Django 3.2.6 on 2021-08-28 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('is_recurring', models.BooleanField()),
                ('start_date', models.DateField()),
                ('occurence', models.IntegerField()),
                ('times_donated', models.IntegerField()),
                ('account_id_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post_id_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Post.post')),
            ],
        ),
    ]
