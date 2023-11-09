from . import views
from django.urls import path
from .views import send_inquiry_view
from transactions.views import SupplierUpdateView


urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<int:pk>/update/', views.SupplierMaterialUpdateView.as_view(), name='update-supplier-material'),
    path('suppliers/<str:material_id>/remove', views.SupplierMaterialDeleteView.as_view(), name='remove-supplier-material'),
    path('<int:pk>', send_inquiry_view, name='supplier-send-inquiry'),
    path('suppliers/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('new/', views.SupplierCreateView.as_view(), name='new-material'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'),
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'),
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<name>/', views.SaleView.as_view(), name='customer'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),
    path('sales/export', views.export_orders_to_csv, name='export_orders'),


    path('purchases/<billno>', views.PurchaseBillView.as_view(), name='purchase-bill'),
    path('purchase/<str:billno>/download/', views.PurchaseBillView.as_view(), name='purchase-bill-pdf'),

    path('sales/<billno>', views.SaleBillView.as_view(), name='sale-bill'),
    path('sales/<str:billno>/download/', views.SaleBillView.as_view(), name='sale-bill-pdf'),
    
    path('transactions/suppliers/supplier/<str:name>/', views.SupplierProfileView.as_view(), name='supplier'),
    path('sale_list/', views.send_quotation_email, name='send_quotation_email'),
]
