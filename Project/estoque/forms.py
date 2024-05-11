from django import forms
from .models import MateriaPrima , Produto, Fornecedores


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = "__all__"



class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
        fields = "__all__"