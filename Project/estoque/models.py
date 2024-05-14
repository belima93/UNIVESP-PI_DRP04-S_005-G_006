from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator

class Categoria(models.Model):
    titulo = models.CharField(max_length=40)

    def __str__(self):
        return self.titulo
    
class TipoMadeira(models.Model):
    tipo = models.CharField(max_length=40)

    def __str__(self) -> str:
        return self.tipo
    
class LinhaProduto(models.Model):
    linha = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.linha
    

class Fornecedores(models.Model):
    cnpj = models.CharField(max_length=14, default='00000000000100', validators=[RegexValidator(regex='^\d{14}$', message='CNPJ deve conter 14 dígitos')])
    razao_social = models.CharField(max_length=255, default='')
    endereco = models.CharField(max_length=255, default='')
    contato = models.CharField(max_length=11, default='99999999999', validators=[RegexValidator(regex='^\d{11}$', message='Contato deve conter 11 dígitos')])
    lista_insumos = models.ManyToManyField('MateriaPrima', related_name='fornecedores_rel', blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.razao_social
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.razao_social)
        return super().save(*args, **kwargs)    

class MateriaPrima(models.Model):
    id_material = models.CharField(max_length=7, default='')
    descricao = models.CharField(max_length=255, default='')  
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fornecedores = models.ManyToManyField(Fornecedores, related_name='materias_primas')
    quantidade = models.IntegerField()
    estoque_min = models.IntegerField(default=0)
    largura = models.DecimalField(max_digits=10, decimal_places=2)
    comprimento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_peca = models.DecimalField(max_digits=10, decimal_places=2)    
    slug = models.SlugField(unique=True, blank=True, null=True)
    imagens_MP = models.ImageField(upload_to='imagem_materiaprima/', blank=True)

    def status_estoque(self):
        if self.quantidade == 0:
            return "Sem Estoque"
        elif self.quantidade < 0.8 * self.estoque_min:
            return "Estoque Crítico"
        elif 0.8 * self.estoque_min <= self.quantidade < 1.2 * self.estoque_min:
            return "Estoque Baixo"
        elif 1.2 * self.estoque_min <= self.quantidade <= 1.5 * self.estoque_min:
            return "Estoque Médio"
        else: # self.quantidade > 1.5 * self.estoque_min
            return "Estoque Alto"  


    def __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.descricao)
        return super().save(*args, **kwargs)

class Produto(models.Model):
    id_produto = models.CharField(max_length=7, default='')
    nomenclatura = models.CharField(max_length=255, default='')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    tipo_madeira = models.ForeignKey(TipoMadeira, on_delete=models.SET_NULL, null=True)
    linha_produto = models.ForeignKey(LinhaProduto, on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField()
    estoque_min = models.IntegerField(default=0)
    comprimento_M = models.DecimalField(max_digits=10, decimal_places=2)
    altura_M = models.DecimalField(max_digits=10, decimal_places=2)      
    valor_m2 = models.DecimalField(max_digits=10, decimal_places=2)     
    fundo = models.DecimalField(max_digits=10, decimal_places=2)  
    custo_MDF = models.DecimalField(max_digits=10, decimal_places=2)  
    tercerizacao = models.DecimalField(max_digits=10, decimal_places=2)
    corte = models.DecimalField(max_digits=10, decimal_places=2)  
    montagem = models.DecimalField(max_digits=10, decimal_places=2)  
    lixa = models.DecimalField(max_digits=10, decimal_places=2)  
    acabamento_pintura = models.DecimalField(max_digits=10, decimal_places=2) 
    slug = models.SlugField(unique=True, blank=True, null=True)
    imagens_produto = models.ImageField(upload_to='imagem_produto/', blank=True)
    
    custo_final = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lucro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    custo_da_madeira = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    P_V_Madeira_x4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fundo_total_x4 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    P_V_MDF_x2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    P_V_Terc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def atualizar_lucro(self):
        if self.valor_venda:
            self.lucro = round(float(self.valor_venda) - float(self.custo_final), 2)
            self.save()

    def status_estoque(self):
        if self.quantidade == 0:
            return "Sem Estoque"
        elif self.quantidade < 0.8 * self.estoque_min:
            return "Estoque Crítico"
        elif 0.8 * self.estoque_min <= self.quantidade < 1.2 * self.estoque_min:
            return "Estoque Baixo"
        elif 1.2 * self.estoque_min <= self.quantidade <= 1.5 * self.estoque_min:
            return "Estoque Médio"
        else: # self.quantidade > 1.5 * self.estoque_min
            return "Estoque Alto"       

        


    def __str__(self) -> str:
        return self.nomenclatura
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nomenclatura)
        return super().save(*args, **kwargs)             
    
class Imagem_MP(models.Model):
    imagem = models.ImageField(upload_to="imagem_materiaprima")
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, default=1)


class Imagem_Produto(models.Model):
    imagem = models.ImageField(upload_to="imagem_produto")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE,default=1)