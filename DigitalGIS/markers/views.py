"""Markers view."""
import json
from django.core.serializers import serialize
from django.views.generic.base import TemplateView


from .models import Marker, Mask

class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["masks"] = json.loads(serialize("geojson", Mask.objects.all()[:]))
        return context
# Create your views here.
