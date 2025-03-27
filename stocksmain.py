import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from fpdf import FPDF
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import time
import json

# SUA API KEY AQUI:
ALPHA_VANTAGE_API_KEY = 'Your API Key'


with open("nomes_empresas.json", "r") as f:
    NOMES_EMPRESAS = json.load(f)

with open("setores.json", "r") as f:
    SETORES = json.load(f)

def gerar_pdf(setor, dias, pasta_destino):
    try:
        tickers = SETORES.get(setor, [])
        if not tickers:
            raise ValueError("Setor não encontrado.")

        ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
        data_hoje = datetime.date.today().strftime('%d-%m-%Y')
        nome_arquivo = f"Relatorio_{setor.replace(' ', '_')}_{data_hoje}.pdf"
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório Econômico - Setor: {setor}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Dias analisados: {dias}", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Data do Relatório: {data_hoje}", ln=True, align='C')
        pdf.ln(10)

        total = len(tickers)
        progress['value'] = 0
        progress.update()
        progresso = 0

        for ticker in tickers:
            try:
                data, meta = ts.get_daily(symbol=ticker, outputsize='compact')

                # Progressivo delay de 12 segundos com barra animada
                for i in range(12):
                    time.sleep(1)
                    progress['value'] = ((progresso + (i+1)/12) / total) * 100
                    progress.update()

                progresso += 1
                data = data.sort_index().tail(dias)
                if data.empty:
                    continue

                # Gráfico com preenchimento
                plt.figure(figsize=(6, 2.5))
                plt.plot(data.index, data['4. close'], color='red')
                plt.fill_between(data.index, data['4. close'], color='red', alpha=0.1)
                plt.ylim(data['4. close'].min() * 0.98, data['4. close'].max() * 1.02)
                plt.title(f"{ticker} - {dias} dias")
                plt.xlabel("Data")
                plt.ylabel("Preço de Fecho (USD)")
                plt.grid(True)
                grafico_path = os.path.join(pasta_destino, f"{ticker}_graf.png")
                plt.tight_layout()
                plt.savefig(grafico_path)
                plt.close()

                nome_exibir = NOMES_EMPRESAS.get(ticker, ticker)
                plt.title(f"{nome_exibir} - {dias} dias")
                pdf.cell(200, 10, txt=f"Empresa: {nome_exibir}", ln=True)
                pdf.image(grafico_path, x=15, w=180)
                os.remove(grafico_path)
                pdf.ln(5)

            except Exception as e:
                pdf.cell(200, 10, txt=f"Erro ao buscar dados de {ticker}: {str(e)}", ln=True)

        pdf.output(caminho_completo)
        progress['value'] = 100
        progress.update()
        messagebox.showinfo("Sucesso", f"PDF salvo em:\n{caminho_completo}")

    except Exception as e:
        messagebox.showerror("Erro ao gerar PDF", str(e))



# Função chamada ao clicar no botão Analisar
def analisar():
    setor = combo_setor.get()
    dias = entry_dias.get()
    pasta = entry_pasta.get()

    if not setor or not dias or not pasta:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    try:
        dias = int(dias)
    except ValueError:
        messagebox.showwarning("Valor inválido", "O campo 'dias' deve ser um número inteiro!")
        return

    gerar_pdf(setor, dias, pasta)


# Interface gráfica
root = tk.Tk()
root.title("Google Finance BOT")
root.geometry("560x300")
root.configure(bg="#B0B6E0")
root.resizable(False, False)

# Centralizar janela
root.update_idletasks()
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
w = 560
h = 300
x = (sw - w) // 2
y = (sh - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

# Instrução
lbl_instrucao = tk.Label(
    root,
    text="Utilize esta janela para gerar um ficheiro pdf com a variação\n"
         "de um sector de Economia na última semana e nos índices da\n"
         "Bolsa de Valores",
    bg="#B0B6E0",
    font=("Segoe UI", 10),
    justify="center"
)
lbl_instrucao.pack(pady=10)

# Frame de entradas
frame = tk.Frame(root, bg="#B0B6E0")
frame.pack(pady=5)

#Setor
tk.Label(frame, text="Selecione o setor de economia que pretende analisar:", bg="#B0B6E0", font=("Segoe UI", 10)).grid(row=0, column=0, sticky='e', padx=5, pady=5)
combo_setor = ttk.Combobox(frame, values=list(SETORES.keys()), width=25)
combo_setor.grid(row=0, column=1, padx=5, pady=5, sticky='w')


# Linha 2: Dias
tk.Label(frame, text="Escolha quantos dias quer analisar:", bg="#B0B6E0", font=("Segoe UI", 10)).grid(row=1, column=0, sticky='e', padx=5, pady=2)
entry_dias = tk.Entry(frame, width=8, font=("Segoe UI", 10))
entry_dias.grid(row=1, column=1, padx=5, pady=2, sticky='w')

# Texto centralizado para pasta destino
tk.Label(root, text="Por favor, escolha uma pasta para guardar o seu ficheiro pdf:", bg="#B0B6E0", font=("Segoe UI", 10)).pack(pady=(10, 0))

# Frame pasta com botão Browse
frame_pasta = tk.Frame(root, bg="#B0B6E0")
frame_pasta.pack(pady=5)


entry_pasta = tk.Entry(frame_pasta, width=35, font=("Segoe UI", 15))
entry_pasta.pack(side='left', padx=5)

def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)
        entry_pasta.insert(0, pasta)

btn_browse = tk.Button(frame_pasta, text="Browse", font=("Segoe UI", 10), command=escolher_pasta)
btn_browse.pack(side='left')

# Botão Analisar
btn_analisar = tk.Button(root, text="Analisar", font=("Segoe UI", 10), command=analisar)
btn_analisar.pack(pady=(10, 5))

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=(5, 15))


root.mainloop()