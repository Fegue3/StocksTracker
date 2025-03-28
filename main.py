import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from fpdf import FPDF
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import time
import json
import threading

# === INICIALIZA A JANELA ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📊 StocksTracker")
app.geometry("750x600")

# === CARREGAMENTO DE DADOS ===
with open("data/setores.json", "r", encoding="utf-8") as f:
    SETORES = json.load(f)

with open("data/enterprises_name.json", "r", encoding="utf-8") as f:
    NOMES_EMPRESAS = json.load(f)


# ALPHA_VANTAGE_API_KEY não é mais necessário com yfinance

# === FUNÇÃO GERAR PDF ===
def gerar_pdf(setores, dias, pasta_destino):
    comparacao_df = pd.DataFrame()  # armazenar médias por setor
    try:
        tickers = []
        for setor in setores:
            tickers.extend(SETORES.get(setor, []))

        if not tickers:
            raise ValueError("Nenhum ticker encontrado para os setores selecionados.")

        # yfinance não precisa de API key
        data_hoje = datetime.date.today().strftime('%d-%m-%Y')
        nome_arquivo = f"Relatorio_{'_'.join(setores)}_{data_hoje}.pdf"
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório Econômico - Setores: {', '.join(setores)}", ln=True, align='C')
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
                setor_atual = next((s for s in setores if ticker in SETORES[s]), None)
                nome_exibir = NOMES_EMPRESAS.get(ticker, ticker)
                app.after(0, lambda nome=nome_exibir: status_label.configure(text=f"Processando: {nome}"))

                outputsize = 'full' if dias > 100 else 'compact'
                data = yf.Ticker(ticker).history(period=f"{dias}d")

                progresso += 1
                data = data[['Close']]
                data.columns = ['4. close']
                comparacao_df[ticker] = data['4. close']
                if data.empty:
                    continue

                plt.figure(figsize=(7, 3))
                plt.plot(data.index, data['4. close'], color='red', linewidth=1.8)
                plt.fill_between(data.index, data['4. close'], color='red', alpha=0.1)
                plt.ylim(data['4. close'].min() * 0.98, data['4. close'].max() * 1.02)
                plt.title(f"{ticker} - {dias} dias")
                plt.xlabel("Data")
                plt.ylabel("Preço de Fecho (USD)")
                plt.grid(True)
                plt.xticks(rotation=30)
                plt.tight_layout(pad=1)

                grafico_path = os.path.join(pasta_destino, f"{ticker}_graf.png")
                plt.savefig(grafico_path, bbox_inches='tight')
                plt.close()

                pdf.cell(200, 10, txt=f"Empresa: {nome_exibir}", ln=True)
                pdf.image(grafico_path, x=15, w=180)
                os.remove(grafico_path)
                pdf.ln(5)

            except Exception as e:
                pdf.cell(200, 10, txt=f"Erro ao buscar dados de {ticker}: {str(e)}", ln=True)

        if not comparacao_df.empty:
            media_por_data = comparacao_df.mean(axis=1)
            plt.figure(figsize=(7, 3))
            for ticker in comparacao_df.columns:
                plt.plot(comparacao_df.index, comparacao_df[ticker], label=ticker)
            plt.legend(fontsize=8)
            plt.title('Comparação de Preço Médio entre Setores')
            plt.xlabel('Data')
            plt.ylabel('Preço Médio (USD)')
            plt.grid(True)
            plt.xticks(rotation=30)
            plt.tight_layout()
            comparacao_path = os.path.join(pasta_destino, "comparacao_setores.png")
            plt.savefig(comparacao_path, bbox_inches='tight')
            plt.close()
            pdf.add_page()
            pdf.cell(200, 10, txt="Comparação Geral entre Setores", ln=True, align='C')
            pdf.image(comparacao_path, x=15, w=180)

        # Exibir gráfico na interface antes de exportar
        if 'comparacao_path' in locals() and os.path.exists(comparacao_path):
            import tkinter as tk
            preview_window = Toplevel()
            preview_window.title("Pré-visualização: Comparação entre Setores")
            img = Image.open(comparacao_path)
            img = img.resize((700, 300))
            photo = ImageTk.PhotoImage(img)
            label_img = tk.Label(preview_window, image=photo)
            label_img.image = photo
            label_img.pack(padx=10, pady=10)
            preview_window.after(5000, preview_window.destroy)  # auto fecha após 5s

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

def toggle_dropdown():
    if dropdown_frame.winfo_ismapped():
        dropdown_frame.pack_forget()
    else:
        dropdown_frame.configure(fg_color=dropdown_container.cget("fg_color"))
        dropdown_frame.pack(pady=(5, 0), anchor='w')
        empresa_label.pack(anchor='w', pady=(5, 5))
        

def atualizar_botao_setores():
    count = sum(var.get() for var in check_vars.values())
    texto = f"Selecionar Setores ({count})" if count else "Selecionar Setores"
    setores_btn.configure(text=texto)

    total_empresas = sum(len(SETORES[setor]) for setor, var in check_vars.items() if var.get())
    empresa_label.configure(text=f"Total de empresas selecionadas: {total_empresas}")

def analisar():
    setores_selecionados = [setor for setor, var in check_vars.items() if var.get()]
    dias = entry_dias.get()
    pasta = entry_pasta.get()

    if not setores_selecionados or not dias or not pasta:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return

    try:
        dias = int(dias)
    except ValueError:
        messagebox.showwarning("Valor inválido", "O campo 'dias' deve ser um número inteiro!")
        return

    threading.Thread(target=gerar_pdf, args=(setores_selecionados, dias, pasta), daemon=True).start()

# === INTERFACE ===
top_frame = ctk.CTkFrame(app, corner_radius=15)
top_frame.pack(pady=10, padx=20, fill='x')

titulo = ctk.CTkLabel(top_frame, text="📈 StocksTracker", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(side="left", padx=15, pady=10)

tema_switch = ctk.CTkSwitch(top_frame, text="Modo Claro", command=alternar_tema)
tema_switch.pack(side="right", padx=15)

lbl_instrucao = ctk.CTkLabel(app, text="Gere um PDF com a variação dos setores econômicos nas últimas semanas", font=ctk.CTkFont(size=14), justify="center")
lbl_instrucao.pack(pady=10)

main_frame = ctk.CTkFrame(app, corner_radius=15)
main_frame.pack(pady=10, padx=20)

ctk.CTkLabel(main_frame, text="📂 Setores:").grid(row=0, column=0, padx=5, pady=5, sticky='ne')

dropdown_container = ctk.CTkFrame(main_frame, fg_color=main_frame.cget("fg_color"))
dropdown_container.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

setores_btn = ctk.CTkButton(dropdown_container, text="Selecionar Setores", command=toggle_dropdown)
setores_btn.pack(anchor='w')

dropdown_frame = ctk.CTkFrame(dropdown_container, fg_color=main_frame.cget("fg_color"))
empresa_label = ctk.CTkLabel(dropdown_frame, text="Total de empresas selecionadas: 0")
empresa_label = ctk.CTkLabel(dropdown_frame, text="Total de empresas selecionadas: 0", anchor='w', font=ctk.CTkFont(size=13, weight="bold"))
empresa_label.pack(anchor='w', padx=10, pady=(5, 5))
dropdown_frame.pack_forget()

check_vars = {}
for setor in SETORES:
    var = ctk.BooleanVar()
    var.trace_add("write", lambda *_, v=var: atualizar_botao_setores())
    chk = ctk.CTkCheckBox(dropdown_frame, text=setor, variable=var)
    chk.pack(anchor='w', padx=10)
    check_vars[setor] = var

ctk.CTkLabel(main_frame, text="📅 Dias:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_dias = ctk.CTkEntry(main_frame, width=100)
entry_dias.grid(row=1, column=1, padx=5, pady=5, sticky='w')

ctk.CTkLabel(app, text="📀 Escolha uma pasta para salvar o PDF:").pack(pady=(10, 0))
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

def fechar_dropdown(event):
    if not dropdown_frame.winfo_containing(event.x_root, event.y_root):
        dropdown_frame.pack_forget()

app.bind('<Button-1>', fechar_dropdown)

app.mainloop()
