from django.urls import path
from . import views

urlpatterns = [
    
    path('add_materiaprima/', views.add_materiasprimas, name = 'add_materiasprimas'),
    path('materiaprima/<slug:slug>/', views.MATERIAPRIMA, name = 'materiaprima'),
    path('editar_materiaprima/<slug:slug>/', views.editar_insumos, name='editar_materiaprima')
    
]
