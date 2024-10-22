# Generated by Django 5.0.7 on 2024-07-29 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_alter_movie_rating"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="searched",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.ImageField(upload_to="posters/"),
        ),
    ]
