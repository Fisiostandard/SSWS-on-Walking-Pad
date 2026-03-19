from django.urls import path
from vault import views

urlpatterns = [
    path('api/lookup/', views.lookup, name='lookup'),
    path('api/register/', views.register, name='register'),
    path('api/lookup-or-create/', views.lookup_or_create, name='lookup_or_create'),
    path('api/search/', views.search, name='search'),
]
