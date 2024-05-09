from django import forms
from .models import MateriaPrima , Produto


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = "__all__"



class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"