from django.shortcuts import render, get_object_or_404, redirect
from .forms import MateriaPrimaForm
from .models import Categoria,Imagem, Fornecedores, LinhaProduto, TipoMadeira, MateriaPrima
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
def add_materiasprimas(request):
    if request.method == "GET":
        descricao = request.GET.get('descricao')
        categoria = request.GET.get('categoria')
        id_material = request.GET.get('id_material')
        
        materia_prima = MateriaPrima.objects.all()

        if descricao:
            materia_prima = materia_prima.filter(descricao__icontains=descricao)

        if categoria:
            materia_prima = materia_prima.filter(categoria__titulo=categoria)

        if id_material:
            materia_prima = materia_prima.filter(id_material=id_material)

        categorias = Categoria.objects.all()
        fornecedores = Fornecedores.objects.all()
        
        return render(request, 'add_materiaprima.html', {'materiasprimas': materia_prima, 'categorias': categorias, 'fornecedores': fornecedores})
    
    elif request.method == "POST":
        id_material = request.POST.get('id_material')
        descricao = request.POST.get('descricao')
        categoria = request.POST.get('categoria')
        fornecedor = request.POST.get('fornecedor')
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

        materia_prima = MateriaPrima(
            id_material=id_material,
            descricao=descricao,
            categoria_id=categoria,
            quantidade=quantidade,
            largura=largura,
            comprimento=comprimento,
            valor_peca=valor_peca,
            valor_m2=valor_m2
        )
        materia_prima.save()
        materia_prima.fornecedores.set([fornecedor])


        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{materia_prima.id}.jpg'

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

            img_dj = Imagem(imagem=img_final, materia_prima=materia_prima)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Materia Prima cadastrada com sucesso')
        return redirect(reverse('add_materiasprimas'))
    

def MATERIAPRIMA(request, slug):
    materia_prima_x = get_object_or_404(MateriaPrima, slug=slug)
    if request.method == "GET":
        form = MateriaPrimaForm(instance=materia_prima_x)
        return render(request, 'materiaprima.html', {'form': form, 'materiaprima': materia_prima_x})
    elif request.method == "POST":
        form = MateriaPrimaForm(request.POST, instance=materia_prima_x)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matéria Prima atualizada com sucesso')
            return redirect('add_materiasprimas')  # Redireciona para a URL 'add_materiasprimas'
        else:
            messages.error(request, 'Ocorreu um erro ao salvar a matéria prima. Por favor, corrija os erros abaixo.')
            return render(request, 'materiaprima.html', {'form': form, 'materiaprima': materia_prima_x})
        

def editar_insumos(request, slug):
    materia_prima_x = get_object_or_404(MateriaPrima, slug=slug)
    if request.method == 'POST':
        form = MateriaPrimaForm(request.POST, instance=materia_prima_x)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materia Prima atualizado com sucesso')
            return redirect('materiaprima', slug=materia_prima_x.slug)  # Corrigir este redirecionamento
        else:
            messages.error(request, 'Ocorreu um erro ao salvar a materia prima. Por favor, corrija os erros abaixo.')
    else:
        form = MateriaPrimaForm(instance=materia_prima_x)
    return render(request, 'editar_insumos.html', {'form': form, 'materia prima': materia_prima_x})
