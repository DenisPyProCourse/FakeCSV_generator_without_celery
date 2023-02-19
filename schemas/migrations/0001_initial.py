# Generated by Django 4.1.7 on 2023-02-19 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sep', models.CharField(choices=[(',', 'Comma (,)'), ('.', 'Dot (.)'), ('-', 'Hyphen (-)'), (':', 'Colon (:)'), (';', 'Semicolon (;)')], default=',', max_length=20)),
                ('str_char', models.CharField(choices=[("'", 'Quotes ()'), ('"', 'Double quotes ("")'), (' ', 'Blank ( )')], default='"', max_length=20)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_schem', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Ready', 'Ready'), ('Processing', 'Processing'), ('Error', 'Error')], default='Processing', max_length=20)),
                ('rows', models.PositiveIntegerField(blank=True, null=True)),
                ('load_lnk', models.URLField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('task_id', models.TextField(blank=True, null=True)),
                ('schema', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='has_dataset', to='schemas.schema')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Columns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(max_length=50)),
                ('cl_type', models.CharField(choices=[('Full name', 'Full name'), ('Job', 'Job'), ('Email', 'Email'), ('Domain name', 'Domain name'), ('Phone number', 'Phone number'), ('Company name', 'Company name'), ('Text', 'Text'), ('Integer', 'Integer'), ('Address', 'Address'), ('Date', 'Date')], default='Integer', max_length=20)),
                ('cl_ord', models.PositiveIntegerField()),
                ('from_int', models.PositiveIntegerField(blank=True, null=True)),
                ('to_int', models.PositiveIntegerField(blank=True, null=True)),
                ('schem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_column', to='schemas.schema')),
            ],
            options={
                'ordering': ('cl_ord',),
            },
        ),
    ]