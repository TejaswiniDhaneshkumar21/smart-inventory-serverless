from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),  # Default to login
    path('signup/', views.signup, name='signup'), # Root URL maps to signup view
    path('dashboard/', views.dashboard, name='dashboard'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/create/', views.supplier_create, name='supplier_create'),
    path('suppliers/update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    path('rawmaterials/', views.rawmaterial_list, name='rawmaterial_list'),
    path('rawmaterials/create/', views.rawmaterial_create, name='rawmaterial_create'),
    path('rawmaterials/update/<int:pk>/', views.rawmaterial_update, name='rawmaterial_update'),
    path('rawmaterials/delete/<int:pk>/', views.rawmaterial_delete, name='rawmaterial_delete'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/update/<int:pk>/', views.product_update, name='product_update'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('stockentries/', views.stockentry_list, name='stockentry_list'),
    path('stockentries/create/', views.stockentry_create, name='stockentry_create'),
    path('stockentries/update/<int:pk>/', views.stockentry_update, name='stockentry_update'),
    path('stockentries/delete/<int:pk>/', views.stockentry_delete, name='stockentry_delete'),
    path('spoilageassessments/', views.spoilageassessment_list, name='spoilageassessment_list'),
    path('spoilageassessments/create/', views.spoilageassessment_create, name='spoilageassessment_create'),
    path('spoilageassessments/update/<int:pk>/', views.spoilageassessment_update, name='spoilageassessment_update'),
    path('spoilageassessments/delete/<int:pk>/', views.spoilageassessment_delete, name='spoilageassessment_delete'),
    path('spoilageassessment/', views.spoilageassessment_list, name='spoilageassessment_list'),
    path('spoilageassessment/create/', views.spoilageassessment_create, name='spoilageassessment_create'),
    path('spoilageassessment/<int:pk>/update/', views.spoilageassessment_update, name='spoilageassessment_update'),
    path('spoilageassessment/<int:pk>/delete/', views.spoilageassessment_delete, name='spoilageassessment_delete'),
    path('sqs-monitor/', views.sqs_monitor, name='sqs_monitor'),
]