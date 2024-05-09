from django.contrib import admin
from .models import Categoria, TipoMadeira, LinhaProduto, Produto,Fornecedores,MateriaPrima

admin.site.register(Categoria)
admin.site.register(TipoMadeira)
admin.site.register(LinhaProduto)
admin.site.register(Produto)
admin.site.register(Fornecedores)
admin.site.register(MateriaPrima)