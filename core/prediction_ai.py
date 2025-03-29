from fpdf import FPDF
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import datetime
import tempfile
import os
from matplotlib.dates import AutoDateLocator, DateFormatter

def gerar_texto_analise(df, nome_empresa):
    preco_inicial = df['Close'].iloc[0]
    preco_final = df['Close'].iloc[-1]
    variacao = preco_final - preco_inicial
    variacao_pct = (variacao / preco_inicial) * 100

    media = df['Close'].mean()
    desvio = df['Close'].std()
    volume_medio = df['Volume'].mean()

    direcao = "subida" if variacao > 0 else "queda"
    intensidade = "ligeira" if abs(variacao_pct) < 5 else "acentuada"

    texto = (
        f"A empresa {nome_empresa} apresentou uma {intensidade} {direcao} de aproximadamente "
        f"{variacao_pct:.2f}% durante o período analisado. O preço médio foi de {media:.2f} USD, "
        f"com um desvio padrão de {desvio:.2f}, indicando {'alta' if desvio > 10 else 'baixa'} volatilidade.\n\n"
        f"O volume médio de transações foi de cerca de {volume_medio:,.0f} ações por dia. "
        f"Estes dados sugerem uma tendência {'positiva' if variacao > 0 else 'negativa'} "
        f"a curto prazo, com base na performance recente."
    )

    return texto

def adicionar_previsao_pdf(pdf: FPDF, df: pd.DataFrame, nome_empresa: str):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df['Days'] = (df['Date'] - df['Date'].min()).dt.days

    X = df[['Days']]
    y = df['Close']
    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(df['Days'].max() + 1, df['Days'].max() + 31).reshape(-1, 1)
    future_dates = [df['Date'].max() + datetime.timedelta(days=int(i)) for i in range(1, 31)]
    future_preds = model.predict(future_days)

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df['Date'], df['Close'], label='Histórico', linewidth=2)
    ax.plot(future_dates, future_preds, label='Previsão (30 dias)', linestyle='--', linewidth=2)
    ax.set_title(f'Previsão de Preço - {nome_empresa}')
    ax.set_xlabel('Data')
    ax.set_ylabel('Preço')
    ax.legend()
    ax.grid(True)

    ax.xaxis.set_major_locator(AutoDateLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate(rotation=30)

    fig.tight_layout()

    # Salvar como imagem temporária
    img_buffer = BytesIO()
    fig.savefig(img_buffer, format='PNG', dpi=100)
    plt.close(fig)
    img_buffer.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(img_buffer.getvalue())
        tmp_path = tmp_file.name

    img_buffer.close()

    # Inserir gráfico no PDF
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Previsão para {nome_empresa}", ln=True)
    pdf.image(tmp_path, x=20, w=170)
    os.remove(tmp_path)

    # ↓ Aqui está a magia: move o cursor abaixo da imagem, qualquer que seja a sua altura
    pdf.set_y(pdf.get_y() + 5)

    # Texto explicativo + análise juntos
    pdf.set_font("Arial", '', 11)
    explicacao = (
        "Este gráfico representa uma previsão baseada em regressão linear, utilizando os dados "
        "históricos dos preços da ação selecionada. A linha tracejada estima a evolução dos preços "
        "nos próximos 30 dias. "
    )
    analise = gerar_texto_analise(df, nome_empresa)
    pdf.multi_cell(0, 7, explicacao + analise)

    # Espaço após bloco
    pdf.ln(10)


