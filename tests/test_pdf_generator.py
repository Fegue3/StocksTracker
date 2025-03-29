import unittest
from unittest.mock import patch, MagicMock
from core import pdf_generator
import pandas as pd

class TestGerarPDF(unittest.TestCase):

    @patch("core.pdf_generator.os.remove")
    @patch("core.pdf_generator.yf.Ticker")
    @patch("core.pdf_generator.FPDF")
    @patch("core.pdf_generator.plt")
    def test_gerar_pdf_basico(self, mock_plt, mock_fpdf, mock_ticker, mock_remove):
        # Simular dados de input
        setores = ["Tech"]
        dias = 5
        pasta = "./tmp"
        SETORES = {"Tech": ["AAPL"]}
        NOMES_EMPRESAS = {"AAPL": "Apple Inc."}
        indicadores_vars = {
            "SMA": MagicMock(get=lambda: False),
            "EMA": MagicMock(get=lambda: False),
            "RSI": MagicMock(get=lambda: False)
        }

        mock_hist = MagicMock()
        mock_hist.history.return_value = pd.DataFrame({
            "Close": [150, 152, 151, 153, 155]
        }, index=pd.date_range("2023-01-01", periods=5))
        mock_ticker.return_value = mock_hist

        def callback_ui(status, msg=None):
            self.assertIn(status, ["start", "processing", "done"])

        pdf_generator.gerar_pdf(
            setores, dias, pasta, SETORES, NOMES_EMPRESAS,
            indicadores_vars, callback_ui
        )

        mock_fpdf.return_value.output.assert_called_once()

if __name__ == '__main__':
    unittest.main()
