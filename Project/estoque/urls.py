from django.urls import path
from . import views

urlpatterns = [
    
    path('add_materiaprima/', views.add_materiasprimas, name = 'add_materiasprimas'),
    path('materiaprima/<slug:slug>/', views.MATERIAPRIMA, name = 'materiaprima'),
    path('editar_materiaprima/<slug:slug>/', views.editar_insumos, name='editar_materiaprima'),    
    path('excluir-insumos/<slug:slug>/', views.excluir_insumos, name='excluir-insumos'),
    path('add_produto/', views.add_produto, name="add_produto"),
    path('produto/<slug:slug>', views.produto, name="produto"),
    path('editar_produto/<slug:slug>/', views.editar_produto, name='editar_produto'),
    path('excluir-produto/<slug:slug>/', views.excluir_produto, name='excluir_produto'),
    path('add_fornecedor/', views.add_fornecedor, name = 'add_fornecedor'),
    path('fornecedor/<slug:slug>/', views.fornecedor, name = 'fornecedor'),
    path('editar_fornecedor/<slug:slug>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('excluir-fornecedor/<slug:slug>/', views.excluir_fornecedor, name='excluir_fornecedor'),
    path('estoque_home', views.home, name='estoque_home'),
    path('produto/editar/<slug:slug>/', views.prod_valor_venda, name='prod_valor_venda'),
    
]
