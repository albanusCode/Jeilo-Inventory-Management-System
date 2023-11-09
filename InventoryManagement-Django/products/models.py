from django.db import models

class Product(models.Model):
    code = models.CharField(max_length = 100, default='')
    name = models.CharField(max_length = 100, null = True)
    type = models.CharField(max_length = 50 )
    description = models.CharField(max_length = 50 , default = "")
    quantity = models.PositiveIntegerField(null = True)
    is_deleted = models.BooleanField(default=False)
    def __str__ (self):
        return f"{self.type}: {self.name} = {self.quantity}"