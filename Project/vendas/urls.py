from django.urls import path
from . import views

urlpatterns = [
    
    path('vendas_produto/', views.vendas_produto, name = 'vendas_produto'),
    path('gerar_produto/', views.gerar_produto, name = 'gerar_produto'),

]