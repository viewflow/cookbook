from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    options = models.ManyToManyField("Option", blank=True)

    def __str__(self):
        return f"Order #{self.pk} ({self.customer.name})"

    class Meta:
        ordering = ("created",)
        verbose_name_plural = "orders"

    @property
    def total(self):
        return sum(item.total for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} (Order #{self.order.pk})"

    @property
    def total(self):
        return self.unit_price * self.quantity


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
