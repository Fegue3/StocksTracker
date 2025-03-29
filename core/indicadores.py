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
