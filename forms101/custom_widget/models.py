from django.db import models


class Email(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    from_email = models.EmailField(max_length=254)
    to_email = models.EmailField(max_length=254)

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    name = models.CharField(max_length=150)
    email = models.ForeignKey(
        Email, related_name="attachments", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="attachments/")

    def __str__(self):
        return self.image.url


class Order(models.Model):
    customer_name = models.CharField(max_length=150)
    quantity = models.DecimalField(decimal_places=0, max_digits=5)
    unit_price = models.DecimalField(decimal_places=2, max_digits=5)
