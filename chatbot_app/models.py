from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

# Create your models here.
# chatbot_app/models.py

def validate_phone_number(value):
    # Check if the provided value has exactly 11 digits, starts with "01", and all characters are numeric
    if len(value) == 11 and value.startswith("01") and value.isdigit():
        return value
    else:
        # Raise a ValidationError if the phone number doesn't match the specified pattern
        raise ValidationError("Invalid phone number")

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.TextField(validators=[validate_phone_number])
    email = models.EmailField(validators=[EmailValidator(message="Invalid email address")])
    address = models.TextField()

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

class Complaint(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    summary = models.TextField()
    unique_id = models.UUIDField(unique=True)
