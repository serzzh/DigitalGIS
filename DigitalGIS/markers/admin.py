"""Markers admin."""

from django.contrib.gis import admin

from .models import Marker
from .models import Mask

@admin.register(Marker)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("name", "location")

@admin.register(Mask)
class MaskAdmin(admin.GeoModelAdmin):
    """Masks admin."""

    list_display = ("condition", "geometry")