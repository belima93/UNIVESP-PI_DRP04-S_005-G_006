from django.contrib import admin
from .models import Categoria, TipoMadeira, LinhaProduto, Mercadoria,Fornecedores,MateriaPrima

admin.site.register(Categoria)
admin.site.register(TipoMadeira)
admin.site.register(LinhaProduto)
admin.site.register(Mercadoria)
admin.site.register(Fornecedores)
admin.site.register(MateriaPrima)