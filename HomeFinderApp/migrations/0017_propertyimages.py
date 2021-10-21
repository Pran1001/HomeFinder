# Generated by Django 3.2.7 on 2021-10-13 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HomeFinderApp', '0016_post_imagefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='Images')),
                ('property_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HomeFinderApp.post')),
            ],
            options={
                'db_table': 'PropertyImages',
            },
        ),
    ]