from django.db import migrations


def create_customers_and_contacts(apps, schema_editor):
    Customer = apps.get_model("sales", "Customer")
    Contact = apps.get_model("sales", "Contact")

    # Creating Customers
    customer1 = Customer.objects.create(name="John Doe")
    customer2 = Customer.objects.create(name="Jane Smith")

    # Creating Contacts for Customer 1
    Contact.objects.create(
        customer=customer1,
        email="john@work.com",
        phone_number="111-222-3333",
        is_primary=True,
    )
    Contact.objects.create(
        customer=customer1,
        email="johm@home.com",
        phone_number="444-555-6666",
        is_primary=False,
    )

    # Creating Contacts for Customer 2
    Contact.objects.create(
        customer=customer2,
        email="jane@work.com",
        phone_number="777-888-9999",
        is_primary=True,
    )
    Contact.objects.create(
        customer=customer2,
        email="jane@home.com",
        phone_number="000-111-2222",
        is_primary=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_customers_and_contacts),
    ]
