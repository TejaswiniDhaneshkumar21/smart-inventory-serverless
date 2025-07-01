from django.db import models
from django.contrib.auth.models import User

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    reliability_score = models.FloatField(default=0.0)  # 0 to 100

    def __str__(self):
        return self.name

class RawMaterial(models.Model):
    name = models.CharField(max_length=100)
    batch_id = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    expiry = models.DateField()
    quantity = models.FloatField()
    invoice = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.batch_id})"

class Product(models.Model):
    name = models.CharField(max_length=100)
    raw_materials = models.ManyToManyField(RawMaterial)
    production_date = models.DateField()

    def __str__(self):
        return self.name

class StockEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}"

class SpoilageAssessment(models.Model):
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment_date = models.DateField(auto_now_add=True)
    avg_temp = models.FloatField(default=25.0, help_text="Average temperature (°C)")
    days_stored = models.IntegerField(default=0, help_text="Days stored")
    spoilage_risk = models.FloatField(default=0.0, help_text="Spoilage risk percentage (0-100)")
    notification_sent = models.BooleanField(default=False, help_text="Whether an SNS notification has been sent")

    def __str__(self):
        return f"{self.raw_material.name} - {self.assessment_date}"