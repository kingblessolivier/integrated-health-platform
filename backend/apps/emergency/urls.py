from django.urls import path

from .views import DispatchNearest, Handover, SosIntake

urlpatterns = [
    path("emergency/sos/", SosIntake.as_view(), name="sos"),                          # EMIN
    path("emergency/dispatches/<uuid:dispatch_id>/assign/", DispatchNearest.as_view()),  # EMDS
    path("emergency/dispatches/<uuid:dispatch_id>/handover/", Handover.as_view()),    # EMHO
]
