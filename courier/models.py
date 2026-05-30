from django.db import models
from django.utils import timezone

class Base(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CourierCountry(Base):
    """Generic country/destination used for zone mapping."""

    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=10, blank=True)
    is_domestic = models.BooleanField(
        default=False,
        help_text="Domestic destinations can use region-level zones and weight multipliers.",
    )

    class Meta:
        verbose_name = "Courier Country"
        verbose_name_plural = "Courier Countries"
        ordering = ("name",)

    def __str__(self):
        return self.name


class CourierRegion(Base):
    """Generic state/province/region under a country."""

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(
        CourierCountry,
        on_delete=models.CASCADE,
        related_name="regions",
    )

    class Meta:
        verbose_name = "Courier Region"
        verbose_name_plural = "Courier Regions"
        ordering = ("country__name", "name")
        unique_together = ("country", "name")

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Zone(Base):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"
        ordering = ("name",)

    def __str__(self):
        return self.name


class ZoneConnection(Base):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="connections")
    countries = models.ManyToManyField(
        "courier.CourierCountry",
        blank=True,
        related_name="zone_connections",
    )
    regions = models.ManyToManyField(
        "courier.CourierRegion",
        blank=True,
        related_name="zone_connections",
    )

    class Meta:
        verbose_name = "Zone Connection"
        verbose_name_plural = "Zone Connections"

    def __str__(self):
        return str(self.zone)


class WeightCost(Base):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="weight_costs")
    weight = models.DecimalField(max_digits=20, decimal_places=3)
    amount = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        verbose_name = "Weight Cost"
        verbose_name_plural = "Weight Costs"
        ordering = ("zone__name", "weight")

    def __str__(self):
        return f"{self.zone} @ {self.weight} = {self.amount}"
