from django.db import models

class Discount(models.Model):
    code = models.CharField(max_length=10 , unique=True)
    OPTION_KIND = [
        ('per', 'per'),
        ('val', 'val'),
    ]
    kind = models.CharField(max_length=10, choices=OPTION_KIND)
    amount = models.IntegerField()
    expiration_date = models.DateTimeField()
    number_of_times = models.IntegerField()

    def __str__(self):
        return f'{self.code}'

