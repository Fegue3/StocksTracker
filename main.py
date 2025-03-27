import customtkinter as ctk
from tkinter import filedialog, messagebox
from fpdf import FPDF
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import time
import json
from cryptography.fernet import Fernet
import threading

# === INICIALIZA A JANELA ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📊 StocksTracker")
app.geometry("700x500")

# === CARREGAMENTO DE DADOS ===
with open("data/setores.json", "r", encoding="utf-8") as f:
    SETORES = json.load(f)

with open("data/enterprises_name.json", "r", encoding="utf-8") as f:
    NOMES_EMPRESAS = json.load(f)

with open("secret.key", "rb") as key_file:
    key = key_file.read()

with open("api.enc", "rb") as f:
    encrypted_api = f.read()

fernet = Fernet(key)
ALPHA_VANTAGE_API_KEY = fernet.decrypt(encrypted_api).decode()

# === FUNÇÃO GERAR PDF ===
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
        progresso = 0

        app.after(0, lambda: btn_analisar.configure(state="disabled"))
        app.after(0, lambda: progress.set(0))
        app.after(0, lambda: status_label.configure(text="Iniciando análise..."))

        for ticker in tickers:
            try:
                nome_exibir = NOMES_EMPRESAS.get(ticker, ticker)
                app.after(0, lambda nome=nome_exibir: status_label.configure(text=f"Processando: {nome}"))

                outputsize = 'full' if dias > 100 else 'compact'
                data, meta = ts.get_daily(symbol=ticker, outputsize=outputsize)

                for i in range(12):
                    time.sleep(0.5)
                    progresso_local = progresso / total * 100 + (i + 1) / 12 * (100 / total)
                    app.after(0, lambda v=progresso_local: progress.set(v))

                progresso += 1
                data = data.sort_index().tail(dias)
                if data.empty:
                    continue

                plt.figure(figsize=(6, 2.5))
                plt.plot(data.index, data['4. close'], color='red')
                plt.fill_between(data.index, data['4. close'], color='red', alpha=0.1)
                plt.ylim(data['4. close'].min() * 0.98, data['4. close'].max() * 1.02)
                plt.title(f"{ticker} - {dias} dias")
                plt.xlabel("Data")
                plt.ylabel("Preço de Fecho (USD)")
                plt.grid(True)
                plt.xticks(rotation=45)

                grafico_path = os.path.join(pasta_destino, f"{ticker}_graf.png")
                plt.tight_layout()
                plt.gcf().autofmt_xdate()
                plt.savefig(grafico_path)
                plt.close()

                pdf.cell(200, 10, txt=f"Empresa: {nome_exibir}", ln=True)
                pdf.image(grafico_path, x=15, w=180)
                os.remove(grafico_path)
                pdf.ln(5)

            except Exception as e:
                pdf.cell(200, 10, txt=f"Erro ao buscar dados de {ticker}: {str(e)}", ln=True)

        pdf.output(caminho_completo)
        app.after(0, lambda: progress.set(100))
        app.after(0, lambda: status_label.configure(text="Análise concluída!"))
        app.after(0, lambda: messagebox.showinfo("Sucesso", f"PDF salvo em:\n{caminho_completo}"))

    except Exception as e:
        app.after(0, lambda: messagebox.showerror("Erro ao gerar PDF", str(e)))
        app.after(0, lambda: status_label.configure(text="Erro durante análise"))

    finally:
        app.after(0, lambda: btn_analisar.configure(state="normal"))

# === FUNÇÕES AUXILIARES ===
def alternar_tema():
    modo = "light" if tema_switch.get() == 1 else "dark"
    tema_switch.configure(text="Modo Escuro" if modo == "light" else "Modo Claro")
    ctk.set_appearance_mode(modo)

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

    threading.Thread(target=gerar_pdf, args=(setor, dias, pasta), daemon=True).start()

# === INTERFACE ===
top_frame = ctk.CTkFrame(app, corner_radius=15)
top_frame.pack(pady=10, padx=20, fill='x')

titulo = ctk.CTkLabel(top_frame, text="📈 StocksTracker", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(side="left", padx=15, pady=10)

tema_switch = ctk.CTkSwitch(top_frame, text="Modo Claro", command=alternar_tema)
tema_switch.pack(side="right", padx=15)

lbl_instrucao = ctk.CTkLabel(app, text="Gere um PDF com a variação do setor econômico nas últimas semanas", font=ctk.CTkFont(size=14), justify="center")
lbl_instrucao.pack(pady=10)

main_frame = ctk.CTkFrame(app, corner_radius=15)
main_frame.pack(pady=10, padx=20)

ctk.CTkLabel(main_frame, text="📂 Setor:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
combo_setor = ctk.CTkOptionMenu(main_frame, values=list(SETORES.keys()))
combo_setor.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(main_frame, text="📅 Dias:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_dias = ctk.CTkEntry(main_frame, width=100)
entry_dias.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(app, text="💾 Escolha uma pasta para salvar o PDF:").pack(pady=(10, 0))
frame_pasta = ctk.CTkFrame(app)
frame_pasta.pack(pady=5)

entry_pasta = ctk.CTkEntry(frame_pasta, width=400)
entry_pasta.pack(side="left", padx=5)

btn_browse = ctk.CTkButton(frame_pasta, text="📁 Browse", command=lambda: entry_pasta.insert(0, filedialog.askdirectory()))
btn_browse.pack(side="left")

btn_analisar = ctk.CTkButton(app, text="✔ Analisar", command=analisar)
btn_analisar.pack(pady=(10, 5))

progress = ctk.CTkProgressBar(app, width=400)
progress.set(0)
progress.pack(pady=(5, 10))

status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()
