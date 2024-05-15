from django.shortcuts import render, get_object_or_404, redirect
from .forms import MateriaPrimaForm, ProdutoForm, FornecedorForm
from .models import Categoria,Imagem_MP,Imagem_Produto, Fornecedores, LinhaProduto, TipoMadeira, MateriaPrima, Produto
from vendas.models import Vendas,Insumos
from django.http import HttpResponse, HttpResponseRedirect
from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator
from decimal import Decimal
from django.dispatch import receiver
import json





@has_permission_decorator('cadastrar_materiaprima')
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
        estoque_min= request.POST.get('estoque_min')
        largura = request.POST.get('largura')
        comprimento = request.POST.get('comprimento')
        valor_peca = request.POST.get('valor_peca')        

        # Convertendo para float com 2 casas decimais
        quantidade = int(quantidade)
        estoque_min = int(estoque_min)
        largura = round(float(largura), 2)
        comprimento = round(float(comprimento), 2)
        valor_peca = round(float(valor_peca), 2)        

        materia_prima = MateriaPrima(
            id_material=id_material,
            descricao=descricao,
            categoria_id=categoria,            
            quantidade=quantidade,
            estoque_min=estoque_min,
            largura=largura,
            comprimento=comprimento,
            valor_peca=valor_peca          
        )
        materia_prima.save()
        
        materia_prima.fornecedores.add(fornecedor) 



        for f in request.FILES.getlist('imagens_MP'):
            name = f'{date.today()}-{materia_prima.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), f"Art_Madeira {date.today()}", (255,0,0))
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

            img_dj = Imagem_MP(imagem=img_final, materia_prima=materia_prima)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Materia Prima cadastrada com sucesso')
        return redirect(reverse('add_materiasprimas'))
    
    else:
    # Se o fornecedor não existe, trate o erro de alguma maneira
    # Por exemplo, redirecione o usuário para uma página de erro ou exiba uma mensagem de erro
        messages.error(request, 'Fornecedor não encontrado. Certifique-se de selecionar um fornecedor válido.')
        return redirect(reverse('add_materiasprimas'))
    
@has_permission_decorator('cadastrar_materiaprima')
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
        
@has_permission_decorator('cadastrar_materiaprima')
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


def excluir_insumos(request, slug):
    if request.method == 'POST':
        materia_prima_id = request.POST.get('materia_prima_id')
        MateriaPrima.objects.filter(id=materia_prima_id).delete()
        messages.success(request, 'Matéria-prima excluída com sucesso')
        return HttpResponseRedirect(reverse('add_materiasprimas'))  # ou qualquer outra página após a exclusão
    else:
        return HttpResponseNotAllowed(['POST'])
    

#############################################################################################

@has_permission_decorator('cadastrar_produtos')
def add_produto(request):
    if request.method == "GET":

        nomenclatura = request.GET.get('nomenclatura')
        categoria = request.GET.get('categoria')
        id_produto = request.GET.get('id_produto')
        tipo_madeira = request.GET.get('tipo_madeira')
        linha = request.GET.get('linha')
        produtos = Produto.objects.all()

        if nomenclatura:
            produtos = produtos.filter(nomenclatura__icontains=nomenclatura)

        if categoria:
            produtos = produtos.filter(categoria__titulo=categoria)

        if id_produto:
            produtos = produtos.filter(id_produto=id_produto)

        if tipo_madeira:
            produtos = produtos.filter(tipo_madeira__titulo=tipo_madeira)

        if linha:
            produtos = produtos.filter(linha_produto__titulo=linha)
        
        categorias = Categoria.objects.all()
        tipo_madeiras = TipoMadeira.objects.all()
        linhas = LinhaProduto.objects.all()

        return render(request, 'add_produto.html', {'produtos': produtos, 'categorias': categorias, 'tipos_madeiras': tipo_madeiras, 'linhas': linhas})
    
    elif request.method == "POST":
        id_produto = request.POST.get('id_produto')
        nomenclatura = request.POST.get('nomenclatura')
        categoria_id = request.POST.get('categoria')
        tipo_madeira_id = request.POST.get('tipo_madeira')
        linha_produto_id = request.POST.get('linha_produto')
        quantidade = request.POST.get('quantidade')
        estoque_min = request.POST.get('estoque_min')
        comprimento_M =request.POST.get('comprimento_M')
        altura_M = request.POST.get('altura_M')
        valor_m2 = request.POST.get('valor_m2')
        fundo = request.POST.get('fundo')
        custo_MDF =request.POST.get('custo_MDF')
        tercerizacao = request.POST.get('tercerizacao')
        corte = request.POST.get('corte')
        montagem = request.POST.get('montagem')
        lixa = request.POST.get('lixa')
        acabamento_pintura = request.POST.get('acabamento_pintura')

        # Convertendo para float com 2 casas decimais
        quantidade = int(quantidade)
        estoque_min = int(estoque_min)
        comprimento_M = round(float(comprimento_M), 2)
        altura_M = round(float(altura_M), 2)
        valor_m2 = round(float(valor_m2), 2)
        fundo = round(float(fundo), 2)
        custo_MDF = round(float(custo_MDF), 2)
        tercerizacao = round(float(tercerizacao), 2)
        corte = round(float(corte), 2)
        montagem = round(float(montagem), 2)
        lixa = round(float(lixa), 2)
        acabamento_pintura = round(float(acabamento_pintura), 2)

        

        produto = Produto(
            id_produto=id_produto,
            nomenclatura=nomenclatura,
            categoria_id=categoria_id,
            tipo_madeira_id=tipo_madeira_id,
            linha_produto_id = linha_produto_id,
            quantidade=quantidade,
            estoque_min=estoque_min,
            comprimento_M=comprimento_M,
            altura_M=altura_M,
            valor_m2=valor_m2,            
            fundo=fundo,           
            custo_MDF=custo_MDF,            
            tercerizacao=tercerizacao,           
            corte=corte,
            montagem=montagem,
            lixa=lixa,
            acabamento_pintura=acabamento_pintura)
        
        produto.save()
        
        calcular_custosadicionais_produto(produto)
        calcular_custosfinais_produtos(produto)
        valoresfinais_produto(produto)


        for f in request.FILES.getlist('imagens_produto'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img)
            draw.text((20, 280), f"Art_Madeira {date.today()}", (255,0,0))
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


            img_dj = Imagem_Produto(imagem = img_final, produto=produto)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso')
        return redirect(reverse('add_produto'))
    

def produto(request, slug):    
    produto_X = get_object_or_404(Produto, slug=slug)
    if request.method == "GET":
        form = ProdutoForm(instance=produto_X)
        return render(request, 'produto.html', {'form': form, 'produto': produto_X})
    elif request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto_X)
        if form.is_valid():
            form.save()
            # Após salvar o formulário, chame a função para recalcular os valores finais do produto
            valoresfinais_produto(request)
            messages.success(request, 'Produto atualizado com sucesso')
            return redirect('add_produto')  # Redireciona para a URL 'add_produto'
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o produto. Por favor, corrija os erros abaixo.')
            return render(request, 'produto.html', {'form': form, 'materiaprima': produto_X})



def editar_produto(request, slug):
    produto_X = get_object_or_404(Produto, slug=slug)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto_X)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso')
            return redirect('produto', slug=produto_X.slug)  # Corrigir este redirecionamento
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o produto. Por favor, corrija os erros abaixo.')
    else:
        form = ProdutoForm(instance=produto_X)
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto_X})

def calcular_custosadicionais_produto(produto):

    produtos = Produto.objects.all()

    for produto in produtos:
        produto.custo_da_madeira = round(float((produto.comprimento_M * produto.altura_M) * produto.valor_m2), 2)
        produto.P_V_Madeira_x4 = round(float(produto.custo_da_madeira * 4), 2)
        produto.fundo_total_x4 = round(float(produto.fundo * 4), 2)
        produto.P_V_MDF_x2 = round(float(produto.custo_MDF * 2), 2)
        produto.P_V_Terc =  round(float(produto.tercerizacao * 2), 2)

        produto.save()

    
def calcular_custosfinais_produtos(produto):

    produtos = Produto.objects.all()

    for produto in produtos:

        produto.custo_final =  round(float(produto.custo_da_madeira + produto.fundo + produto.custo_MDF + produto.tercerizacao + produto.corte + produto.montagem + produto.lixa + produto.acabamento_pintura),2)

        produto.valor_sugerido = round(float(produto.P_V_Madeira_x4 + produto.fundo_total_x4 + produto.P_V_MDF_x2 + produto.P_V_Terc + produto.corte + produto.montagem + produto.lixa + produto.acabamento_pintura),2)

        produto.save()


def valoresfinais_produto(request):
    produtos = Produto.objects.all()

    for produto in produtos:
        if not produto.valor_venda:
            produto.valor_venda = round(float(produto.valor_sugerido), 2)
        produto.lucro = round(float(produto.valor_venda) - float(produto.custo_final), 2)
        produto.save()


def excluir_produto(request, slug):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        Produto.objects.filter(id=produto_id).delete()
        messages.success(request, 'Produto excluído com sucesso')
        return HttpResponseRedirect(reverse('add_produto'))  # ou qualquer outra página após a exclusão
    else:
        return HttpResponseNotAllowed(['POST'])
    

#############################################################################################


def add_fornecedor(request):
    if request.method == "GET":
        razao_social = request.GET.get('razao_social')
        cnpj = request.GET.get('cnpj')
        
        fornecedores = Fornecedores.objects.all()

        if razao_social:
            fornecedores = fornecedores.filter(razao_social=razao_social)

        if cnpj:
            fornecedores = fornecedores.filter(cnpj=cnpj)

        return render(request, 'add_fornecedor.html', {'fornecedores': fornecedores})
    
    elif request.method == "POST":
        cnpj = request.POST.get('cnpj')
        razao_social = request.POST.get('razao_social')
        endereco = request.POST.get('endereco')
        contato = request.POST.get('contato')
        lista_insumos_ids = request.POST.getlist('lista_insumos')
        

        fornecedor = Fornecedores(
            cnpj=cnpj,
            razao_social=razao_social,
            endereco=endereco,
            contato=contato,            
            )
        fornecedor.save()

        if lista_insumos_ids:
            fornecedor.lista_insumos.add(*lista_insumos_ids)

        messages.add_message(request, messages.SUCCESS, 'Fornecedor cadastrado com sucesso')
        return redirect(reverse('add_fornecedor'))


def fornecedor(request,slug):

    fornecedor_x = get_object_or_404(Fornecedores, slug=slug)
    if request.method == "GET":
        form = FornecedorForm(instance=fornecedor_x)
        return render(request, 'fornecedor.html', {'form': form, 'fornecedor': fornecedor_x})
    elif request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor_x)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso')
            return redirect('add_fornecedor')  # Redireciona para a URL 'add_materiasprimas'
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o fornecedor. Por favor, corrija os erros abaixo.')
            return render(request, 'fornecedor.html', {'form': form, 'fornecedor': fornecedor_x})

  

def editar_fornecedor(request,slug):
    fornecedor_x = get_object_or_404(Fornecedores, slug=slug)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor_x)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso')
            return redirect('fornecedor', slug=fornecedor_x.slug)  # Corrigir este redirecionamento
        else:
            messages.error(request, 'Ocorreu um erro ao salvar o fornecedor. Por favor, corrija os erros abaixo.')
    else:
        form = FornecedorForm(instance=fornecedor_x)
    return render(request, 'editar_fornecedor.html', {'form': form, 'fornecedor': fornecedor_x})

def excluir_fornecedor(request, slug):
    if request.method == 'POST':
        fornecedor_id = request.POST.get('fornecedor_id')
        Fornecedores.objects.filter(id=fornecedor_id).delete()
        messages.success(request, 'Fornecedor excluído com sucesso')
        return HttpResponseRedirect(reverse('add_fornecedor'))  # ou qualquer outra página após a exclusão
    else:
        return HttpResponseNotAllowed(['POST'])

#######################################################


def home(request):
    produtos = Produto.objects.all()
    materias_primas = MateriaPrima.objects.all()

    # Adiciona o status de estoque a cada produto
    for produto in produtos:
        produto.status_estoque = produto.status_estoque()

    for materia_prima in materias_primas:
        materia_prima.status_estoque = materia_prima.status_estoque()

    return render(request, 'estoque_home.html', {'produtos': produtos,'materias_primas': materias_primas})



def prod_valor_venda(request, slug):    
    produto = get_object_or_404(Produto, slug=slug)
    if request.method == 'POST':
        novo_valor_venda = request.POST.get('novo_valor_venda')
        try:
            novo_valor_venda = round(float(novo_valor_venda), 2)
            produto.valor_venda = novo_valor_venda
            produto.save()
            # Chama o método para atualizar o lucro do produto
            produto.atualizar_lucro()
            messages.success(request, 'Valor de venda atualizado com sucesso')
            return redirect('estoque_home')
        except ValueError:
            messages.error(request, 'Por favor, insira um valor válido para o novo valor de venda.')
    return render(request, 'prod_valor_venda.html', {'produto': produto})


###############################################################################################################