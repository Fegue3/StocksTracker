# 📈 STOCKSTRACKER

> _Empower your investments with insightful market analysis and intelligent predictions._

![last commit](https://img.shields.io/badge/last%20commit-today-blue)
![language](https://img.shields.io/badge/python-100%25-blue)
![libraries](https://img.shields.io/badge/libraries-7-important)

**Built with:**

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![CustomTkinter](https://img.shields.io/badge/-CustomTkinter-4B8BBE?style=flat-square)
![Scikit-learn](https://img.shields.io/badge/-Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-11557C?style=flat-square&logo=matplotlib&logoColor=white)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy)
![yFinance](https://img.shields.io/badge/-yFinance-black?style=flat-square)
![FPDF](https://img.shields.io/badge/-FPDF-green?style=flat-square)

---

## 📌 Table of Contents

- [📖 Overview](#-overview)
- [🖼️ Screenshots](#️-screenshots)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Prerequisites](#prerequisites)
  - [💾 Installation](#installation)
- [⚙️ Usage](#️-usage)
- [🤖 Artificial Intelligence](#-artificial-intelligence)
- [🧪 Tests](#-tests)
- [💪 Libraries](#-libraries)
- [👨‍💼 Author](#-author)

---

## 📖 Overview

**StocksTracker** is a Python desktop application that provides financial charts, intelligent stock price predictions using AI, and PDF reports for selected market sectors. It features a modern GUI with light/dark mode, multithreaded PDF generation, and real-time data from Yahoo Finance.

---

## 🖼️ Screenshots

### 🖥️ Application Interface
![GUI](https://github.com/user-attachments/assets/74d9627c-66d6-423f-8855-3d0f1bdf58f7)


### 📄 Generated PDF Report
![pdf](https://github.com/user-attachments/assets/6cf35f3e-54fd-43e6-ac14-0997894142c4)

### 🤖 AI Report
![AI](https://github.com/user-attachments/assets/0f3b7671-7869-4ec4-92ad-665d1e752d0b)


---

## 🚀 Getting Started

### 🔧 Prerequisites

To run StocksTracker, you will need:

- Python 3.7 or higher
- pip (Python package manager)

### 💾 Installation

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage

Run the app with:

```bash
python main.py
```

Then follow the graphical interface:
- Choose one or more sectors
- Set how many days to analyze
- Select a folder to save the report
- Click **"Analisar"** and let the magic happen!

---

## 🤖 Artificial Intelligence

StocksTracker uses **machine learning** to forecast stock price trends.

- The model used is a **Linear Regression** algorithm from `scikit-learn`.
- It processes historical stock data and extrapolates future prices.
- The predictions are optionally included in the final PDF report.
- Users can choose whether to include AI insights in the analysis.

> 📌 Forecasting is based on the past N days selected, and aims to assist—not replace—investment decisions.

---

## 🧪 Tests

StocksTracker includes unit tests to ensure functionality and maintainability.

- All test files are located in the `tests/` directory.
- Run tests with:

```bash
python -m unittest discover tests
```

This allows continuous verification of critical components such as PDF generation, AI prediction logic, and data parsing.

---

## 💪 Libraries

| Library          | Description                             |
|------------------|-----------------------------------------|
| `pandas`         | Data analysis and manipulation          |
| `numpy`          | Numerical operations and data handling  |
| `matplotlib`     | Generating charts and visualizations    |
| `yfinance`       | Fetching stock market data              |
| `scikit-learn`   | AI-based stock price prediction         |
| `fpdf`           | Creating professional PDF reports       |
| `customtkinter`  | Modern and styled desktop GUI           |

---

## 👨‍💼 Author

Developed by [Fegue3](https://github.com/Fegue3)  
🔐 Secure. 📈 Insightful. 🧠 Smart.

