# Generated by Django 2.0.3 on 2018-03-21 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_machine',
            options={'verbose_name': 'Kullanıcıya Ait Cihazlar', 'verbose_name_plural': 'Kullanıcıya Ait Cihazlar'},
        ),
        migrations.AddField(
            model_name='machine',
            name='active',
            field=models.BooleanField(default=0, verbose_name='Aktif/Pasif'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default=None, upload_to='users', verbose_name='Profil Fotoğrafı'),
        ),
    ]
