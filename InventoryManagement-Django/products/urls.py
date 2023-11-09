from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('new', views.ProductCreateView.as_view(), name='new-product'),
    path('templates/', views.ProductCreateView.as_view(), name='product'),
    path('templates/delete/<int:pk>/', views.product_delete, name='product-delete'),
    path('templates/update/<int:pk>/', views.product_update, name='product-update'),

    path('product/export', views.export_products_to_csv, name='export_products'),



    ]
urlpatterns += staticfiles_urlpatterns()