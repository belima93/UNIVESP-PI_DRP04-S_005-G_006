from django.db import models
from django.template.defaultfilters import slugify

class Categoria(models.Model):
    titulo = models.CharField(max_length=40)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    id_material = models.CharField(max_length=7,default='')
    descricao = models.CharField(max_length=255, default='')  # Valor padrão para descricao
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    largura = models.DecimalField(max_digits=10, decimal_places=2)
    comprimento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_peca = models.DecimalField(max_digits=10, decimal_places=2)
    valor_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.descricao)

        return super().save(*args, **kwargs)

    def gerar_desconto(self, desconto):
        return self.preco_venda - ((self.preco_venda * desconto) / 100)

    def lucro(self):
        lucro = self.preco_venda - self.preco_compra
        return (lucro * 100) / self.preco_compra
    
class Imagem(models.Model):
    imagem = models.ImageField(upload_to="imagem_produto")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)  # Exemplo de um produto padrão com ID 1

