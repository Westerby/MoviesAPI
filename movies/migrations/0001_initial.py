# Generated by Django 2.0.7 on 2018-07-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('year', models.IntegerField()),
                ('rated', models.TextField()),
                ('released', models.TextField()),
                ('runtime', models.TextField()),
                ('genre', models.TextField()),
                ('director', models.TextField()),
                ('writer', models.TextField()),
                ('actors', models.TextField()),
                ('plot', models.TextField()),
                ('language', models.TextField()),
                ('country', models.TextField()),
                ('awards', models.TextField()),
                ('poster', models.TextField()),
                ('metascore', models.TextField()),
                ('imdb_rating', models.TextField()),
                ('imdb_votes', models.TextField()),
                ('imdb_id', models.TextField()),
                ('type', models.TextField()),
                ('dvd', models.TextField()),
                ('box_office', models.TextField()),
                ('production', models.TextField()),
                ('website', models.TextField()),
            ],
        ),
    ]
