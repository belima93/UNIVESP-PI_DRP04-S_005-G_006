from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProdutoForm
from .models import Categoria, Produto, Imagem
from django.http import HttpResponse
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator

@has_permission_decorator('cadastrar_produtos')
def add_produto(request):
    if request.method == "GET":
        descricao = request.GET.get('descricao')
        categoria = request.GET.get('categoria')
        id_material = request.GET.get('id_material')
        produtos = Produto.objects.all()

        if descricao:
            produtos = produtos.filter(descricao__icontains=descricao)

        if categoria:
            produtos = produtos.filter(categoria=categoria)

        if id_material:
            produtos = produtos.filter(id=id_material)

        categorias = Categoria.objects.all()
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos': produtos})
    elif request.method == "POST":
        id_material = request.POST.get('id_material')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        quantidade = request.POST.get('quantidade')
        largura = request.POST.get('largura')
        comprimento = request.POST.get('comprimento')
        valor_peca = request.POST.get('valor_peca')
        valor_m2 = request.POST.get('valor_m2')

        # Convertendo para float com 2 casas decimais
        quantidade = int(quantidade)
        largura = round(float(largura), 2)
        comprimento = round(float(comprimento), 2)
        valor_peca = round(float(valor_peca), 2)
        valor_m2 = round(float(valor_m2), 2)

        produto = Produto(id_material=id_material,
                  descricao=descricao,
                  categoria_id=categoria,
                  quantidade=quantidade,
                  largura=largura,
                  comprimento=comprimento,
                  valor_peca=valor_peca,
                  valor_m2=valor_m2)

        produto.save()

        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), f"Art_Madeira {date.today()}", (255, 255, 255))
            output = BytesIO()
            img.save(output, format="JPEG", quality=100)
            output.seek(0)
            img_final = InMemoryUploadedFile(output,
                                             'ImageField',
                                             name,
                                             'image/jpeg',
                                             sys.getsizeof(output),
                                             None
                                             )

            img_dj = Imagem(imagem=img_final, produto=produto)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso')
        return redirect(reverse('add_produto'))

def produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    if request.method == "GET":
        form = ProdutoForm(instance=produto)
        return render(request, 'produto.html', {'form': form, 'produto': produto})
    elif request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso')
            return redirect('add_produto')  # Redireciona para a URL 'add_produto'
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o produto. Por favor, corrija os erros abaixo.')
            return render(request, 'produto.html', {'form': form, 'produto': produto})
    
def editar_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso')
            return redirect(reverse('produto', kwargs={'slug': produto.slug}))
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o produto. Por favor, corrija os erros abaixo.')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})
