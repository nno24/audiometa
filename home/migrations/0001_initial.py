# Generated by Django 4.0.4 on 2022-05-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_file_name', models.CharField(blank=True, max_length=50, null=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]