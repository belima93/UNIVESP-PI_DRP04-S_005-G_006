from atexit import register
from django import template
from estoque.models import Imagem_MP, Imagem_Produto

register = template.Library()

@register.filter(name='get_first_image_mp')
def get_first_image_MP(materiaprima):
    imagem = Imagem_MP.objects.filter(materia_prima=materiaprima).first()
    if imagem:
        return imagem.imagem.url
    else:
        return False
    

@register.filter(name='get_first_image_produto')
def get_first_image_produto(produto):
    imagem = Imagem_Produto.objects.filter(produto=produto).first()
    if imagem:
        return imagem.imagem.url
    else:
        return False
