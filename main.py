import csv
import os
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

valor_contrato = 2000.00

class Imovel:
    def __init__(self, tipo: str, qtd_quarto: int = 1, qtd_vaga: int = 0, crianca: bool = True):
        self.tipo = tipo
        self.qtd_quarto = qtd_quarto
        self.qtd_vaga = qtd_vaga
        self.crianca = crianca

    def valor_base(self) -> float:
        if self.tipo == 'Apartamento':
            return 700.00
        elif self.tipo == 'Casa':
            return 900.00
        elif self.tipo == 'Estudio':
            return 1200.00
        else:
            raise ValueError("Tipo de imóvel inválido")
        
    def valor_extra_quarto(self) -> float:
        if self.tipo == 'Apartamento':
            if self.qtd_quarto == 2:
                return 200.00
            else:
                return 0.00
        elif self.tipo == 'Casa':
            if self.qtd_quarto == 2:
                return 250.00
            else:
                return 0.00
        else:
            return 0.00
        
    def valor_extra_vaga(self) -> float:
        if self.tipo in ('Apartamento', 'Casa'):
            return 300.00 * self.qtd_vaga
        elif self.tipo == 'Estudio':
            vaga = self.qtd_vaga

            if vaga == 0:
                return 0.00
            elif vaga == 1:
                return 60.00
            elif vaga == 2:
                return 250.00
            else:
                return 250.00 + 60.00 * (vaga - 2)
        else:
            return 0.00
        
    def desconto_apto(self, subtotal: float) -> float:
        if self.tipo == 'Apartamento' and not self.crianca:
            return subtotal * 0.05
        return 0.00
    
    def calcular_mensalidade(self) -> float:
        valor_base = self.valor_base()
        quarto_extra = self.valor_extra_quarto()
        vaga_extra = self.valor_extra_vaga()   
        subtotal = valor_base + quarto_extra + vaga_extra
        desconto = self.desconto_apto(subtotal)
        mensalidade = subtotal - desconto

        return round(mensalidade + 1e-9, 2)
    
class Orcamento:
    def __init__(self, imovel: Imovel, valor_contrato: float = valor_contrato, parcelas_contrato: int = 1 ):
        if parcelas_contrato < 1 or parcelas_contrato > 5:
            raise ValueError("Número de parcelas deve ser entre 1 e 5")
        self.imovel = imovel
        self.valor_contrato = valor_contrato
        self.parcelas_contrato = parcelas_contrato

    def valor_parcela(self) -> float:
        return round(self.valor_contrato / self.parcelas_contrato + 1e-9, 2)
    
    def gerar_parcela_12_meses(self):
        mensalidade = self.imovel.calcular_mensalidade()
        parcela = self.valor_parcela()

        parcelas = []

        for mes in range(1, 13):
            if mes <= self.parcelas_contrato:
                parcela_do_contrato = parcela
            else:
                return 0.00
            
            total_mes = round(mensalidade + parcela_do_contrato + 1e-9, 2)

            parcelas.append({
                "mes": mes,
                "mensalidade": mensalidade,
                "parcela_contrato": parcela_do_contrato,
                "total_mes": total_mes
            })
        
        return parcelas