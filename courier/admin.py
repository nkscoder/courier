from django.contrib import admin

from .models import WeightCost, Zone, ZoneConnection

try:
    from import_export.admin import ImportExportModelAdmin

    AdminBase = ImportExportModelAdmin
except ImportError:
    AdminBase = admin.ModelAdmin


class WeightCostAdmin(AdminBase):
    list_display = ("zone", "weight", "amount")


class ZoneAdmin(AdminBase):
    list_display = ("name",)


class ZoneConnectionAdmin(AdminBase):
    list_display = ("zone",)


admin.site.register(Zone, ZoneAdmin)
admin.site.register(WeightCost, WeightCostAdmin)
admin.site.register(ZoneConnection, ZoneConnectionAdmin)
