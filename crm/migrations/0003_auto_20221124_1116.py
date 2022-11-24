from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create the groups
    Group.objects.get_or_create(name='Sales')
    Group.objects.get_or_create(name='Support')

    # Get the permissions
    add_client = Permission.objects.get(codename='add_client')
    view_own_client = Permission.objects.get(codename='view_own_client')
    edit_own_client = Permission.objects.get(codename='edit_own_client')

    add_event = Permission.objects.get(codename='add_event')
    view_own_event = Permission.objects.get(codename='view_own_event')
    edit_own_event = Permission.objects.get(codename='edit_own_event')

    view_own_contract = Permission.objects.get(codename='view_own_contract')
    edit_own_contract = Permission.objects.get(codename='edit_own_contract')

    # Assign the permissions to the groups
    sales_group = Group.objects.get(name='Sales')
    support_group = Group.objects.get(name='Support')

    sales_group.permissions.add(add_client, view_own_client, edit_own_client,
                                add_event, view_own_contract, edit_own_contract)

    support_group.permissions.add(
        view_own_event, edit_own_event, view_own_client)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_client_options_alter_contract_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
