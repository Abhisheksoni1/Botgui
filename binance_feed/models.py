from django.db import models

# Create your models here


class History(models.Model):
    symbol = models.CharField(max_length=32)
    time = models.IntegerField()
    volume = models.DecimalField(decimal_places=4, max_digits=64)
    price = models.DecimalField(decimal_places=8, max_digits=32)

    def __str__(self):
        return self.symbol + str(self.time)

    class Meta:
        # unique_together = ('symbol', 'time',)
        ordering = ('time',)

