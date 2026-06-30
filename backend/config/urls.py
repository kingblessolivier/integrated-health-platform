from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.tokens import FourAxisTokenView

urlpatterns = [
    # Login issues a JWT carrying the four-axis scope + command bundle (docs/04, 49).
    path("api/v1/auth/token/", FourAxisTokenView.as_view(), name="token"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/", include("apps.patients.urls")),
    path("api/v1/", include("apps.clinical.urls")),
    path("api/v1/", include("apps.pharmacy.urls")),
    path("api/v1/", include("apps.billing.urls")),
    path("api/v1/", include("apps.community.urls")),
    path("api/v1/", include("apps.emergency.urls")),
    path("api/v1/", include("apps.claims.urls")),
    path("api/v1/", include("apps.interop.urls")),
    path("api/v1/", include("apps.surveillance.urls")),
    path("api/v1/", include("apps.diagnostics.urls")),
    path("api/v1/", include("apps.stock.urls")),
    path("api/v1/", include("apps.hr.urls")),
    path("api/v1/", include("apps.pbf.urls")),
]
