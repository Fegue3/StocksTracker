# core/pdf_generator.py
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from fpdf import FPDF
from core.indicadores import calcular_sma, calcular_ema, calcular_rsi
from core.prediction_ai import adicionar_previsao_pdf

def gerar_pdf(setores, dias, pasta_destino, SETORES, NOMES_EMPRESAS, indicadores_vars, callback_ui):
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

        callback_ui("start")

        for ticker in tickers:
            try:
                nome_exibir = NOMES_EMPRESAS.get(ticker, ticker)
                callback_ui("processing", nome_exibir)

                data = yf.Ticker(ticker).history(period=f"{dias}d")
                if data.empty:
                    continue

                data['Close'] = data['Close'].ffill()
                comparacao_df[ticker] = data['Close']

                if usar_sma:
                    data['SMA'] = calcular_sma(data, window=14)
                if usar_ema:
                    data['EMA'] = calcular_ema(data, window=14)
                if usar_rsi:
                    data['RSI'] = calcular_rsi(data, window=14)

                plt.ioff()
                fig, axs = plt.subplots(2 if usar_rsi else 1, 1, figsize=(7, 4 if usar_rsi else 3), sharex=True)
                ax1 = axs[0] if usar_rsi else axs

                ymin = data['Close'].min() * 0.98
                ymax = data['Close'].max() * 1.02
                ax1.set_ylim(ymin, ymax)

                ax1.plot(data.index, data['Close'], label='Fecho', color='red', linewidth=1.8)
                ax1.fill_between(data.index, data['Close'], ymin, color='red', alpha=0.1)

                if usar_sma:
                    ax1.plot(data.index, data['SMA'], label='SMA 14', color='deepskyblue')
                if usar_ema:
                    ax1.plot(data.index, data['EMA'], label='EMA 14', color='orange', linewidth=2)

                ax1.set_title(f"{ticker} - {dias} dias")
                ax1.set_ylabel("Preço de Fecho (USD)")
                ax1.legend(loc='upper left')
                ax1.set_xlabel("Data")
                ax1.grid(True)

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
                pdf.ln(10)
                os.remove(grafico_path)
                if indicadores_vars.get("IA") and indicadores_vars["IA"].get():
                     adicionar_previsao_pdf(pdf, data.reset_index(), nome_exibir)

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
        callback_ui("done", caminho_completo)

    except Exception as e:
        callback_ui("error", str(e))