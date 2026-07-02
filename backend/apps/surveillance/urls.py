from django.urls import path

from .views import ClusterMap, OutbreakAlerts

urlpatterns = [
    path("surveillance/clusters/", ClusterMap.as_view(), name="clusters"),   # SVMP
    path("surveillance/alerts/", OutbreakAlerts.as_view(), name="alerts"),    # SVAL
]
