import csv
import os
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

valor_fixo = 2000.00

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
                0.00
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