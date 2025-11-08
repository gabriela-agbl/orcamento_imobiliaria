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