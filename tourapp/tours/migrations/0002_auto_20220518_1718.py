# Generated by Django 3.2.12 on 2022-05-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsaction',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tourrating',
            name='rating',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='newsaction',
            unique_together={('user', 'news')},
        ),
        migrations.AlterUniqueTogether(
            name='tourrating',
            unique_together={('user', 'tour')},
        ),
        migrations.RemoveField(
            model_name='newsaction',
            name='type',
        ),
    ]
