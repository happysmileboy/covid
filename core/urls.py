from django.urls import path, include
from core import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('transaction', views.TransactionViewsets, basename='transaction')

urlpatterns = [
    path('home/<str:vaccine_type>/<int:pk>/', views.home, name='home'),
    path('logistics/<str:vaccine_type>/<int:pk>/', views.logistics, name='logistics'),
    path('condition_detail/<str:vaccine_type>/<int:vaccine_pk>/<int:logistics_pk>', views.condition_detail, name='condition_detail'),
    path('', include((router.urls, 'core'))),

]