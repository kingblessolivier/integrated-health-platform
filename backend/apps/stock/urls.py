from django.urls import path

from .views import ExpiryMonitor, ReceiveGoods, StockInquiry

urlpatterns = [
    path("stock/", StockInquiry.as_view(), name="stock"),               # STIN
    path("stock/receive/", ReceiveGoods.as_view(), name="stock-receive"),  # STRC
    path("stock/expiring/", ExpiryMonitor.as_view(), name="stock-expiring"),  # STEX
]
