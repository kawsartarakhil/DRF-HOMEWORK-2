from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Transaction(models.Model):

    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.01)])
    type = models.CharField(max_length=10,choices=TYPE_CHOICES)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

def __str__(self):
    return f'{self.category} - {self.amount}'