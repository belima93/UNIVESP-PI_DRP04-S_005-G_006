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

    def __str__(self) -> str:
        return self.razao_social

class MateriaPrima(models.Model):
    id_material = models.CharField(max_length=7, default='')
    descricao = models.CharField(max_length=255, default='')  
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fornecedores = models.ManyToManyField(Fornecedores, related_name='materias_primas')
    quantidade = models.IntegerField()
    largura = models.DecimalField(max_digits=10, decimal_places=2)
    comprimento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_peca = models.DecimalField(max_digits=10, decimal_places=2)
    valor_m2 = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True, null=True)
    imagens = models.ImageField(upload_to='materiasprimas/', blank=True)

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
    comprimento_M = models.DecimalField(max_digits=10, decimal_places=2)
    altura_M = models.DecimalField(max_digits=10, decimal_places=2)
    m2 = models.DecimalField(max_digits=10, decimal_places=3)  
    valor_m2 = models.DecimalField(max_digits=10, decimal_places=2)  
    custo_madeira = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    P_V_madeira_4x = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    fundo = models.DecimalField(max_digits=10, decimal_places=2)  
    fundo_total_x4 = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    custo_MDF = models.DecimalField(max_digits=10, decimal_places=2)  
    P_V_MDF = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    tercerizacao = models.DecimalField(max_digits=10, decimal_places=2)  
    P_V_Terc = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    corte = models.DecimalField(max_digits=10, decimal_places=2)  
    montagem = models.DecimalField(max_digits=10, decimal_places=2)  
    lixa = models.DecimalField(max_digits=10, decimal_places=2)  
    acabamento_pintura = models.DecimalField(max_digits=10, decimal_places=2)  
    custo_final = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    valor_sugerido = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lucro = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return self.nomenclatura

    def save(self, *args, **kwargs):
        # Arredondar os valores
        self.valor_m2 = round(self.valor_m2, 2) if self.valor_m2 is not None else 0
        self.custo_madeira = round(self.custo_madeira, 2) if self.custo_madeira is not None else 0
        self.P_V_madeira_4x = round(self.P_V_madeira_4x, 2) if self.P_V_madeira_4x is not None else 0
        self.fundo = round(self.fundo, 2) if self.fundo is not None else 0
        self.fundo_total_x4 = round(self.fundo_total_x4, 2) if self.fundo_total_x4 is not None else 0
        self.custo_MDF = round(self.custo_MDF, 2) if self.custo_MDF is not None else 0
        self.P_V_MDF = round(self.P_V_MDF, 2) if self.P_V_MDF is not None else 0
        self.tercerizacao = round(self.tercerizacao, 2) if self.tercerizacao is not None else 0
        self.P_V_Terc = round(self.P_V_Terc, 2) if self.P_V_Terc is not None else 0
        self.corte = round(self.corte, 2) if self.corte is not None else 0
        self.montagem = round(self.montagem, 2) if self.montagem is not None else 0
        self.lixa = round(self.lixa, 2) if self.lixa is not None else 0
        self.acabamento_pintura = round(self.acabamento_pintura, 2) if self.acabamento_pintura is not None else 0
        self.custo_final = round(self.custo_final, 2) if self.custo_final is not None else 0
        self.valor_sugerido = round(self.valor_sugerido, 2) if self.valor_sugerido is not None else 0
        self.lucro = round(self.lucro, 2) if self.lucro is not None else 0

        # Calcular custo da madeira
        if self.m2 is not None and self.valor_m2 is not None:
            self.custo_madeira = round(self.m2 * self.valor_m2, 2)
        else:
            self.custo_madeira = 0

        # Calcular preço de venda da madeira (4x) apenas se self.custo_madeira não for None
        if self.custo_madeira is not None:
            self.P_V_madeira_4x = round(self.custo_madeira * 4, 2)
        else:
            self.P_V_madeira_4x = 0
        
        # Calcular preço de venda do MDF
        self.P_V_MDF = self.custo_MDF * 2
        
        # Calcular preço de venda da tercerização
        self.P_V_Terc = self.tercerizacao * 2
        
        # Calcular fundo total (4x)
        self.fundo_total_x4 = self.fundo * 4
        
        # Calcular custo final
        self.custo_final = (self.acabamento_pintura + self.lixa + self.montagem +
                            self.corte + self.tercerizacao + self.custo_MDF +
                            self.fundo + self.custo_madeira)
        
        # Calcular valor sugerido
        self.valor_sugerido = (self.P_V_madeira_4x + self.fundo_total_x4 + self.P_V_MDF +
                            self.P_V_Terc + self.corte + self.P_V_Terc +
                            self.montagem + self.lixa + self.acabamento_pintura)
        
        # Calcular lucro
        if self.valor_venda is not None and self.valor_venda != '':
            valor_venda = round(self.valor_venda, 2)
            self.lucro = round(valor_venda - self.custo_final if self.custo_final is not None else 0, 2)
        else:
            # Se valor_venda estiver vazio, assumir valor_sugerido
            if self.valor_sugerido is not None:
                self.lucro = round(self.valor_sugerido - self.custo_final if self.custo_final is not None else 0, 2)
            else:
                # Se valor_sugerido também estiver vazio, assumir custo_final
                self.lucro = round(-self.custo_final if self.custo_final is not None else 0, 2)


        # Gerar slug se não existir
        if not self.slug:
            self.slug = slugify(self.nomenclatura)
        
        super().save(*args, **kwargs)
    
class Imagem_MP(models.Model):
    imagem = models.ImageField(upload_to="imagem_materiaprima")
    materia_prima = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, default=1)


class Imagem_Produto(models.Model):
    imagem = models.ImageField(upload_to="imagem_produto")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE,default=1)


