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
    
    def gerar_csv(self, caminho: str = 'orcamento_imobiliaria.csv'):
        parcelas = self.gerar_parcela_12_meses()

        if not parcelas:
            raise ValueError("Não há parcelas para gerar o CSV")

        with open(caminho, mode='w', newline='', enconding = 'utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Mês', 'Mensalidade', 'Parcela do Contrato', 'Total do Mês'])
            for parcela in parcelas:
                writer.writerow([
                    parcela['mes'],
                    f"{parcela['mensalidade']:.2f}",
                    f"{parcela['parcela_contrato']:.2f}",
                    f"{parcela['total_mes']:.2f}"
                ])

        return caminho
    
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Orçamento de Aluguel - R.M Imobiliária")
        root.geometry("620x420")
        root.resizable(False, False)

        self.frame = ttk.Frame(root, padding=12)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.tipo_var = tk.StringVar(value="Apartamento")
        self.quartos_var = tk.IntVar(value=1)
        self.vagas_var = tk.IntVar(value=0)
        self.criancas_var = tk.BooleanVar(value=True)
        self.contrato_parcelas_var = tk.IntVar(value=1)

        self._build_form()
        self._build_result_area()

    def _build_form(self):
        frm = self.frame

        ttk.Label(frm, text="Tipo de imóvel:").grid(row=0, column=0, sticky="w")
        tipo_cb = ttk.Combobox(frm, textvariable=self.tipo_var, state="readonly",
                               values=["Apartamento", "Casa", "Estudio"])
        tipo_cb.grid(row=0, column=1, sticky="w")
        tipo_cb.bind("<<ComboboxSelected>>", lambda e: self._on_tipo_changed())

        ttk.Label(frm, text="Quartos:").grid(row=1, column=0, sticky="w")
        self.quartos_spin = ttk.Spinbox(frm, from_=1, to=2, textvariable=self.quartos_var, width=5)
        self.quartos_spin.grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Número de vagas:").grid(row=2, column=0, sticky="w")
        self.vagas_spin = ttk.Spinbox(frm, from_=0, to=10, textvariable=self.vagas_var, width=5)
        self.vagas_spin.grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Possui crianças?").grid(row=3, column=0, sticky="w")
        criancas_frame = ttk.Frame(frm)
        criancas_frame.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(criancas_frame, text="Sim", variable=self.criancas_var, value=True).pack(side=tk.LEFT)
        ttk.Radiobutton(criancas_frame, text="Não", variable=self.criancas_var, value=False).pack(side=tk.LEFT)

        ttk.Label(frm, text="Parcelas do contrato (até 5x):").grid(row=4, column=0, sticky="w")
        self.contrato_spin = ttk.Spinbox(frm, from_=1, to=5, textvariable=self.contrato_parcelas_var, width=5)
        self.contrato_spin.grid(row=4, column=1, sticky="w")

        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(12, 8))
        ttk.Button(btn_frame, text="Calcular Orçamento", command=self.calcular).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Gerar CSV (12 parcelas)", command=self.gerar_csv).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Salvar como...", command=self.gerar_csv_com_dialog).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar).pack(side=tk.LEFT, padx=6)

        obs = ("Regras aplicadas automaticamente: valores base por tipo, acréscimos por 2º quarto, "
               "vagas, desconto de 5% para apartamento sem crianças, contrato R$2000 parcelável em até 5x.")
        ttk.Label(frm, text=obs, wraplength=580, foreground="gray").grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self._on_tipo_changed()

    def _build_result_area(self):
        res_frame = ttk.LabelFrame(self.frame, text="Resultado", padding=10)
        res_frame.grid(row=7, column=0, columnspan=2, sticky="we", pady=(12, 0))

        self.lbl_mensalidade = ttk.Label(res_frame, text="Mensalidade: R$ 0.00", font=("TkDefaultFont", 11, "bold"))
        self.lbl_mensalidade.pack(anchor="w", pady=2)

        self.lbl_contrato_info = ttk.Label(res_frame, text=f"Contrato: R$ {valor_contrato:.2f} (parcelas: 1x R$ {valor_contrato:.2f})")
        self.lbl_contrato_info.pack(anchor="w", pady=2)

        self.lbl_total_primeiro_mes = ttk.Label(res_frame, text="Total no 1º mês (incluindo parcela do contrato): R$ 0.00")
        self.lbl_total_primeiro_mes.pack(anchor="w", pady=2)

        self.text_detail = tk.Text(res_frame, height=6, width=72, state="disabled", wrap="word")
        self.text_detail.pack(pady=(6, 0))

    def _on_tipo_changed(self):
        tipo = self.tipo_var.get()

        if tipo == "Estudio":
            self.quartos_spin.configure(state="disabled")
            self.quartos_var.set(1)
        else:
            self.quartos_spin.configure(state="normal")

    def calcular(self):
        tipo = self.tipo_var.get()
        quartos = int(self.quartos_var.get())
        vagas = int(self.vagas_var.get())
        criancas = bool(self.criancas_var.get())
        contrato_parcelas = int(self.contrato_parcelas_var.get())

        imovel = Imovel(tipo=tipo, quartos=quartos, vagas=vagas, crianças=criancas)
        orc = Orcamento(imovel=imovel, contrato_total=valor_contrato, contrato_parcelas=contrato_parcelas)

        mensalidade = imovel.calcular_mensalidade()
        parcela_contrato = orc.valor_parcela()
        total_primeiro_mes = round(mensalidade + parcela_contrato, 2)

        self.lbl_mensalidade.config(text=f"Mensalidade: R$ {mensalidade:,.2f}")
        self.lbl_contrato_info.config(text=f"Contrato: R$ {valor_contrato:,.2f} (parcelas: {contrato_parcelas}x R$ {parcela_contrato:,.2f})")
        self.lbl_total_primeiro_mes.config(text=f"Total no 1º mês (incluindo parcela do contrato): R$ {total_primeiro_mes:,.2f}")

        detalhes = []
        detalhes.append(f"Tipo: {tipo}")
        if tipo != "Estudio":
            detalhes.append(f"Quartos: {quartos}")
        detalhes.append(f"Vagas: {vagas}")
        detalhes.append(f"Possui crianças: {'Sim' if criancas else 'Não'}")
        detalhes.append(f"Mensalidade calculada: R$ {mensalidade:,.2f}")
        detalhes.append(f"Contrato total: R$ {valor_contrato:,.2f} dividido em {contrato_parcelas}x de R$ {parcela_contrato:,.2f}")
        detalhes_text = "\n".join(detalhes)

        self.text_detail.configure(state="normal")
        self.text_detail.delete("1.0", tk.END)
        self.text_detail.insert(tk.END, detalhes_text)
        self.text_detail.configure(state="disabled")

        self._ultima_orcamento = orc

    def gerar_csv(self):
        try:
            orc = getattr(self, "_ultima_orcamento", None)
            if orc is None:
                self.calcular()
                orc = self._ultima_orcamento

            path = os.path.join(os.getcwd(), "orcamento.csv")
            orc.gerar_csv(path)

            messagebox.showinfo("CSV Gerado", f"Arquivo salvo em:\n{path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o CSV:\n{e}")

    def gerar_csv_com_dialog(self):
        try:
            orc = getattr(self, "_ultima_orcamento", None)
            if orc is None:
                self.calcular()
                orc = self._ultima_orcamento

            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv")],
                                                     initialfile="orcamento.csv")
            if file_path:
                orc.gerar_csv(file_path)
                
                messagebox.showinfo("CSV Gerado", f"Arquivo salvo em:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o CSV:\n{e}")