# Generated by Django 5.1.1 on 2024-10-16 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_employmenthistory_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='how_did_you_find_out',
            field=models.CharField(choices=[('counseller', 'Academic Counseller'), ('friend', 'Friend'), ('advertisement', 'Advertisement')], max_length=50),
        ),
    ]
