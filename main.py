import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import json
import threading
from fpdf import FPDF


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

indicadores_vars = {
    "SMA": ctk.BooleanVar(value=True),
    "EMA": ctk.BooleanVar(value=True),
    "RSI": ctk.BooleanVar(value=False),
}

def calcular_sma(df, window=14):
    return df['Close'].rolling(window=window).mean()

def calcular_ema(df, window=14):
    return df['Close'].ewm(span=window, adjust=False).mean()

def calcular_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# === FUNÇÃO GERAR PDF ===
def gerar_pdf(setores, dias, pasta_destino):
    comparacao_df = pd.DataFrame()
    usar_sma = indicadores_vars["SMA"].get()
    usar_ema = indicadores_vars["EMA"].get()
    usar_rsi = indicadores_vars["RSI"].get()
    try:
        tickers = []
        for setor in setores:
            tickers.extend(SETORES.get(setor, []))

        if not tickers:
            raise ValueError("Nenhum ticker encontrado para os setores selecionados.")

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

        app.after(0, lambda: btn_analisar.configure(state="disabled"))
        app.after(0, lambda: progress.set(0))
        app.after(0, lambda: status_label.configure(text="Iniciando análise..."))

        for ticker in tickers:
            try:
                nome_exibir = NOMES_EMPRESAS.get(ticker, ticker)
                app.after(0, lambda nome=nome_exibir: status_label.configure(text=f"Processando: {nome}"))

                data = yf.Ticker(ticker).history(period=f"{dias}d")
                if data.empty:
                    continue

                data['Close'] = data['Close'].fillna(method='ffill')
                comparacao_df[ticker] = data['Close']

                # Cálculos dos indicadores
                if usar_sma:
                    data['SMA'] = calcular_sma(data, window=14)
                if usar_ema:
                    data['EMA'] = calcular_ema(data, window=14)
                if usar_rsi:
                    data['RSI'] = calcular_rsi(data, window=14)

                # Gráfico
                plt.ioff()
                fig, axs = plt.subplots(2 if usar_rsi else 1, 1, figsize=(7, 4 if usar_rsi else 3), sharex=True)
                ax1 = axs[0] if usar_rsi else axs

                # Calcula os limites para o gráfico
                ymin = data['Close'].min() * 0.98
                ymax = data['Close'].max() * 1.02
                ax1.set_ylim(ymin, ymax)

                # Linha de fecho e sombra
                ax1.plot(data.index, data['Close'], label='Fecho', color='red', linewidth=1.8)
                ax1.fill_between(data.index, data['Close'], ymin, color='red', alpha=0.1)

                # Indicadores, se selecionados
                if usar_sma:
                    ax1.plot(data.index, data['SMA'], label='SMA 14', color='deepskyblue')
                if usar_ema:
                    ax1.plot(data.index, data['EMA'], label='EMA 14', color='orange', linewidth=2)

                ax1.set_title(f"{ticker} - {dias} dias")
                ax1.set_ylabel("Preço de Fecho (USD)")
                ax1.legend(loc = 'upper left')
                ax1.set_xlabel("Data")
                ax1.grid(True)

                # RSI (se ativo)
                if usar_rsi:
                    ax2 = axs[1]
                    ax2.plot(data.index, data['RSI'], label='RSI 14', color='purple')
                    ax2.axhline(70, color='red', linestyle='--')
                    ax2.axhline(30, color='green', linestyle='--')
                    ax2.set_ylabel("RSI")
                    ax2.legend()
                    ax2.grid(True)

                plt.xticks(rotation=30)
                plt.tight_layout(pad=1)

                grafico_path = os.path.join(pasta_destino, f"{ticker}_graf.png")
                plt.savefig(grafico_path, bbox_inches='tight')
                plt.close()

                pdf.cell(200, 10, txt=f"Empresa: {nome_exibir}", ln=True)
                pdf.image(grafico_path, x=15, w=180)
                pdf.ln(5)
                os.remove(grafico_path)

            except Exception as e:
                pdf.cell(200, 10, txt=f"Erro ao buscar dados de {ticker}: {str(e)}", ln=True)

        if not comparacao_df.empty:
            plt.ioff()
            plt.figure(figsize=(7, 4 if len(setores) > 1 and len(comparacao_df.columns) > 1 else 3))
            for ticker in comparacao_df.columns:
                plt.plot(comparacao_df.index, comparacao_df[ticker], label=ticker)
            plt.legend(fontsize=8)
            plt.title('Comparação Geral entre Empresas Selecionadas')
            plt.xlabel('Data')
            plt.ylabel('Preço de Fecho (USD)')
            plt.grid(True)
            plt.xticks(rotation=30)
            plt.tight_layout()
            comparacao_path = os.path.join(pasta_destino, "comparacao_geral.png")
            plt.savefig(comparacao_path, bbox_inches='tight')
            plt.close()
            pdf.cell(200, 10, txt="Comparação Geral entre Empresas", ln=True, align='C')
            pdf.image(comparacao_path, x=15, w=180)
            pdf.ln(5)
            os.remove(comparacao_path)

            if len(setores) > 1:
                pdf.cell(200, 10, txt="Comparações por Setor", ln=True, align='C')
                for setor in setores:
                    tickers_setor = SETORES.get(setor, [])
                    tickers_presentes = [t for t in tickers_setor if t in comparacao_df.columns]
                    if len(tickers_presentes) < 2:
                        continue
                    plt.figure(figsize=(7, 3))
                    for t in tickers_presentes:
                        plt.plot(comparacao_df.index, comparacao_df[t], label=t)
                    plt.legend(fontsize=8)
                    plt.title(f'Comparação dentro do setor: {setor}')
                    plt.xlabel('Data')
                    plt.ylabel('Preço de Fecho (USD)')
                    plt.grid(True)
                    plt.xticks(rotation=30)
                    plt.tight_layout()
                    setor_path = os.path.join(pasta_destino, f"comparacao_{setor.replace(' ', '_')}.png")
                    plt.savefig(setor_path, bbox_inches='tight')
                    plt.close()
                    pdf.cell(200, 10, txt=f"Comparação - {setor}", ln=True, align='C')
                    pdf.image(setor_path, x=15, w=180)
                    pdf.ln(5)
                    os.remove(setor_path)

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

scroll_frame = ctk.CTkScrollableFrame(app, corner_radius=20, fg_color="transparent")
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

top_frame = ctk.CTkFrame(scroll_frame, corner_radius=15)
top_frame.pack(pady=10, padx=20, fill='x')

titulo = ctk.CTkLabel(top_frame, text="📈 StocksTracker", font=ctk.CTkFont(size=22, weight="bold"))
titulo.pack(side="left", padx=15, pady=10)

tema_switch = ctk.CTkSwitch(top_frame, text="Modo Claro", command=alternar_tema)
tema_switch.pack(side="right", padx=15)

lbl_instrucao = ctk.CTkLabel(scroll_frame, text="Gere um PDF com a variação dos setores econômicos nas últimas semanas", font=ctk.CTkFont(size=14), justify="center")
lbl_instrucao.pack(pady=10)

main_frame = ctk.CTkFrame(scroll_frame, corner_radius=15)
main_frame.pack(pady=10, padx=20)

ctk.CTkLabel(main_frame, text="📂 Setores:").grid(row=0, column=0, padx=5, pady=5, sticky='ne')

dropdown_container = ctk.CTkFrame(main_frame, fg_color=main_frame.cget("fg_color"))
dropdown_container.grid(row=0, column=1, padx=5, pady=5, sticky='nw')

setores_btn = ctk.CTkButton(dropdown_container, text="Selecionar Setores", command=toggle_dropdown)
setores_btn.pack(anchor='w')

dropdown_frame = ctk.CTkFrame(dropdown_container, fg_color=main_frame.cget("fg_color"))
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

# Indicadores Técnicos - Centralizado e compacto
indicadores_frame = ctk.CTkFrame(scroll_frame, corner_radius=15, fg_color="transparent")
indicadores_frame.pack(pady=(5, 10))

linha_indicadores = ctk.CTkFrame(indicadores_frame, fg_color="transparent")
linha_indicadores.pack(anchor='center', padx=10, pady=10)

# Label + checkboxes lado a lado
ctk.CTkLabel(linha_indicadores, text="📈 Indicadores Técnicos:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))

for nome, var in indicadores_vars.items():
    chk = ctk.CTkCheckBox(linha_indicadores, text=nome, variable=var)
    chk.pack(side="left", padx=8)

ctk.CTkLabel(scroll_frame, text="📀 Escolha uma pasta para salvar o PDF:").pack(pady=(10, 0))
frame_pasta = ctk.CTkFrame(scroll_frame)
frame_pasta.pack(pady=5)

entry_pasta = ctk.CTkEntry(frame_pasta, width=400)
entry_pasta.pack(side="left", padx=5)

btn_browse = ctk.CTkButton(frame_pasta, text="📁 Browse", command=lambda: entry_pasta.insert(0, filedialog.askdirectory()))
btn_browse.pack(side="left")

btn_analisar = ctk.CTkButton(scroll_frame, text="✔ Analisar", command=analisar)
btn_analisar.pack(pady=(10, 5))

progress = ctk.CTkProgressBar(scroll_frame, width=400)
progress.set(0)
progress.pack(pady=(5, 10))

status_label = ctk.CTkLabel(scroll_frame, text="")
status_label.pack()

def fechar_dropdown(event):
    if not dropdown_frame.winfo_containing(event.x_root, event.y_root):
        dropdown_frame.pack_forget()

app.bind('<Button-1>', fechar_dropdown)

app.mainloop()