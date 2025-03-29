import unittest
import pandas as pd
from core.indicadores import calcular_sma, calcular_ema, calcular_rsi

class TestIndicadores(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Close": [10, 12, 14, 13, 15, 14, 16, 18, 17, 19]
        })

    def test_calcular_sma(self):
        sma = calcular_sma(self.df, window=3)
        self.assertEqual(len(sma), len(self.df))
        self.assertAlmostEqual(sma.iloc[4], (14 + 13 + 15) / 3)

    def test_calcular_ema(self):
        ema = calcular_ema(self.df, window=3)
        self.assertEqual(len(ema), len(self.df))
        self.assertFalse(ema.isnull().all())

    def test_calcular_rsi(self):
        rsi = calcular_rsi(self.df, window=3)
        rsi_clean = rsi.dropna()
        self.assertTrue(((rsi_clean >= 0) & (rsi_clean <= 100)).all())

if __name__ == '__main__':
    unittest.main()
