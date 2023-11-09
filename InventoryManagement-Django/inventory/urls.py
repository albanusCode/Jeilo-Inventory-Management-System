from django.urls import path
from . import views

urlpatterns = [
    path('material/', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete/', views.StockDeleteView.as_view(), name='delete-stock'),

    path('accessories/', views.AccessoriesListView.as_view(), name='Accessories'),
    path('add', views.AccessoriesCreateView.as_view(), name='add-accessory'),
    path('accessory/<pk>/edit', views.AccessoriesUpdateView.as_view(), name='edit-accessory'),
    path('accessory/<pk>/delete', views.AccessoriesDeleteView.as_view(), name='delete-accessory'),

    path('stock/export', views.export_stocks_to_csv, name='export_materials'),
    path('accessory/export', views.export_accessories_to_csv, name='export_accessories'),




]