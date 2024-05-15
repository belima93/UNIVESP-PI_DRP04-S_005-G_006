from django.db import models
from django.utils import timezone
from estoque.models import Produto,MateriaPrima
import datetime


class Vendas(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=1)
    quantidade = models.PositiveIntegerField(default=0)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    data_venda = models.DateTimeField(default=timezone.now, blank=True)


    def save(self, *args, **kwargs):
        if self.produto.quantidade >= self.quantidade:
            self.produto.quantidade -= self.quantidade
            self.produto.save()
            self.produto.status_estoque()
            self.valor_total = self.quantidade * self.produto.valor_venda
            super().save(*args, **kwargs)
        else:
            raise ValueError("Quantidade insuficiente no estoque")

class Insumos(models.Model):
    material = models.ForeignKey(MateriaPrima, on_delete=models.CASCADE, default=1)  # Use o ID do registro temporário
    quantidade = models.PositiveIntegerField(default=0)
    data_compra = models.DateTimeField(default=timezone.now, blank=True)
