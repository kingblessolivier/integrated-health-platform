from django.urls import path

from .views import GoodsReceiveVerify, PurchaseOrderCreate, ReorderRecommendation

urlpatterns = [
    path("supply/reorder/", ReorderRecommendation.as_view(), name="supply-reorder"),   # SCRO
    path("supply/orders/", PurchaseOrderCreate.as_view(), name="supply-po"),            # SCPO
    path("supply/orders/<uuid:po_id>/receive/", GoodsReceiveVerify.as_view()),          # SCRV
]
