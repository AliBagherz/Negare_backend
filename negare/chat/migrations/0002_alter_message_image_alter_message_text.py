# Generated by Django 4.0.3 on 2022-05-26 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_content'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='core.image'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]