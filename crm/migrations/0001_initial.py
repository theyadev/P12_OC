# Generated by Django 4.1.2 on 2022-11-22 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sales_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_contact_client', to='crm.client')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendees', models.IntegerField()),
                ('date', models.DateField()),
                ('notes', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.client')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='support_contact_event', to='crm.client')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_due', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='crm.client')),
                ('sales_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales_contact_contract', to='crm.client')),
            ],
        ),
    ]
