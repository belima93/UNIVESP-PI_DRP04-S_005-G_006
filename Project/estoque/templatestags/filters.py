from atexit import register
from django import template
from estoque.models import Imagem

register = template.Library()

@register.filter(name='get_first_image')
def get_first_image(materiaprima):
    imagem = Imagem.objects.filter(materia_prima=materiaprima).first()
    if imagem:
        return imagem.imagem.url
    else:
        return False
