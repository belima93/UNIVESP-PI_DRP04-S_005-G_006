from django.urls import path
from . import views

urlpatterns = [
    
    path('add_materiaprima/', views.add_materiasprimas, name = 'add_materiasprimas'),
    path('materiaprima/<slug:slug>/', views.MATERIAPRIMA, name = 'materiaprima'),
    path('editar_materiaprima/<slug:slug>/', views.editar_insumos, name='editar_materiaprima'),
    path('add_produto/', views.add_produto, name="add_produto"),
    path('produto/<slug:slug>', views.produto, name="produto"),
    path('editar_produto/<slug:slug>/', views.editar_produto, name='editar_produto'),
    path('add_fornecedor/', views.add_fornecedor, name = 'add_fornecedor'),
    path('fornecedor/<slug:slug>/', views.fornecedor, name = 'fornecedor'),
    path('editar_fornecedor/<slug:slug>/', views.editar_fornecedor, name='editar_fornecedor')    
]
