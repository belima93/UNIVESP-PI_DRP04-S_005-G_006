import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Vendas
from estoque.models import Produto

def vendas_produto(request):
    if request.method == 'POST':
        data = request.POST
        produtos_venda = json.loads(data.get('produtos', '[]'))
        quantidade_venda = json.loads(data.get('quantidades', '[]'))
        produtos_indisponiveis = []

        # Criamos uma lista para armazenar todas as vendas a serem realizadas
        vendas = []

        for prod_id, qty in zip(produtos_venda, quantidade_venda):
            produto = get_object_or_404(Produto, id=prod_id)
            qty_int = int(qty)  # Convertendo a quantidade para inteiro
            if produto.quantidade < qty_int:
                produtos_indisponiveis.append(produto.nomenclatura)
            else:
                # Adicionamos a venda à lista de vendas a serem realizadas
                vendas.append((produto, qty_int))

        if produtos_indisponiveis:
            messages.error(request, f'Produtos indisponíveis: {", ".join(produtos_indisponiveis)}')
        else:
            # Realizamos as vendas e deduzimos o estoque fora do loop de vendas
            for produto, qty in vendas:
                venda = Vendas(produto=produto, quantidade=qty)
                produto.quantidade -= qty
                produto.save()
            messages.success(request, 'Venda realizada com sucesso')

        return redirect('vendas_produto')

    produtos = Produto.objects.all()
    return render(request, 'vendas_produto.html', {'produtos': produtos})