from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('trades/<int:trade_id>/', views.trade_detail, name='trade_detail'),
    path('filter/', views.filter, name='filter'),
    path('upload/', views.upload_files, name='upload'),
    path('deleteTrade/', views.delete_trade, name='deleteTrade'),
]
