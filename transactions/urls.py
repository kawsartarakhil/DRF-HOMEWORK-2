from django.urls import path
from . import views

urlpatterns = [

path('register/', views.register_view, name='register'),

path('login/', views.login_view, name='login'),

path('logout/', views.logout_view, name='logout'),

path('transactions/', views.transactions, name='transactions'),

path(
    'transactions/<int:pk>/',
    views.transaction_detail,
    name='transaction_detail'
),

path('summary/', views.summary, name='summary'),
]