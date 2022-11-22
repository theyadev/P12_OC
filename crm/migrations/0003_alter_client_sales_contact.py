# Generated by Django 4.1.2 on 2022-11-22 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_client_sales_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales_contact_client', to='crm.client'),
        ),
    ]
