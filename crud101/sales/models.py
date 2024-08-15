from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contact(models.Model):
    customer = models.ForeignKey(
        Customer, related_name="contacts", on_delete=models.CASCADE
    )
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} {self.phone_number}"


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    primary_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True
    )
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()

    def __str__(self):
        return f"Sale {self.id} for {self.customer.name}"
