from django.db import models
from django.utils import timezone

from core.models import Country, State


class Base(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Zone(Base):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zone"

    def __str__(self):
        return self.name


class ZoneConnection(Base):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    country = models.ManyToManyField(Country)
    state = models.ManyToManyField(State, blank=True)

    class Meta:
        verbose_name = "Zone Connection"
        verbose_name_plural = "Zone Connection"

    def __str__(self):
        return f"{self.zone} + {self.country}"


class WeightCost(Base):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=20, decimal_places=3)
    amount = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        verbose_name = "Weight Cost"
        verbose_name_plural = "Weight Cost"

    def __str__(self):
        return f"{self.zone} + {self.amount}"
