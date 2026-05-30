from django.contrib import admin

from .models import CourierCountry, CourierRegion, WeightCost, Zone, ZoneConnection

try:
    from import_export.admin import ImportExportModelAdmin

    AdminBase = ImportExportModelAdmin
except ImportError:
    AdminBase = admin.ModelAdmin


@admin.register(CourierCountry)
class CourierCountryAdmin(AdminBase):
    list_display = ("name", "code", "is_domestic")
    list_filter = ("is_domestic",)
    search_fields = ("name", "code")


@admin.register(CourierRegion)
class CourierRegionAdmin(AdminBase):
    list_display = ("name", "country", "code")
    list_filter = ("country",)
    search_fields = ("name", "code", "country__name")


@admin.register(Zone)
class ZoneAdmin(AdminBase):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ZoneConnection)
class ZoneConnectionAdmin(AdminBase):
    list_display = ("zone",)
    filter_horizontal = ("countries", "regions")
    search_fields = ("zone__name", "countries__name", "regions__name")


@admin.register(WeightCost)
class WeightCostAdmin(AdminBase):
    list_display = ("zone", "weight", "amount")
    list_filter = ("zone",)
    search_fields = ("zone__name",)
