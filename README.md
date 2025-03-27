# 📈 STOCKSTRACKER

> _Empower your investments with insightful market analysis._

![last commit](https://img.shields.io/badge/last%20commit-today-blue)
![language](https://img.shields.io/badge/python-100%25-blue)
![libraries](https://img.shields.io/badge/libraries-5-important)

**Built with:**

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square)
![JSON](https://img.shields.io/badge/-JSON-black?logo=json&style=flat-square)
![Tkinter](https://img.shields.io/badge/-CustomTkinter-4B8BBE?style=flat-square)
![AlphaVantage](https://img.shields.io/badge/-Alpha%20Vantage-003366?style=flat-square)
![FPDF](https://img.shields.io/badge/-FPDF-green?style=flat-square)

---

## 📌 Table of Contents

- [📖 Overview](#-overview)
- [🖼️ Screenshots](#️-screenshots)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Prerequisites](#prerequisites)
  - [💾 Installation](#installation)
- [🔑 Alpha Vantage API](#-alpha-vantage-api)
  - [📝 Getting your API Key](#getting-your-api-key)
  - [⚠️ API Limitations](#api-limitations)
- [⚙️ Usage](#️-usage)
- [💪 Libraries](#-libraries)
- [👨‍💼 Author](#-author)

---

## 📖 Overview

**StocksTracker** is a Python desktop application that provides financial charts and PDF reports of stock market sectors. It utilizes the Alpha Vantage API and features a modern GUI with light/dark mode, custom visual themes, and multithreaded PDF generation.

---

## 🖼️ Screenshots

### 🖥️ Application Interface
![appinterface](https://github.com/user-attachments/assets/b86b1d12-06ce-4f25-a54f-f9d7b490527a)


### 📄 Generated PDF Report
![pdf](https://github.com/user-attachments/assets/2e2671f4-d178-4d54-9cc6-aa90ea671932)


---

## 🚀 Getting Started

### 🔧 Prerequisites

To run StocksTracker, you will need:

- Python 3.7 or higher
- pip (Python package manager)

### 💾 Installation

Install the required libraries using pip:

```bash
pip install pandas matplotlib requests alpha_vantage customtkinter fpdf cryptography
```

---

## 🔑 Alpha Vantage API

StocksTracker uses the [Alpha Vantage API](https://www.alphavantage.co) to retrieve real-time stock market data.

### 📝 Getting your API Key

1. Go to [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
2. Sign up for a free account
3. Copy your API key
4. Encrypt and store it using the provided `secret.key` and `api.enc` system

> The app uses encrypted credentials to keep your key secure.

### ⚠️ API Limitations

Free plan:
- ⏱️ Max 5 requests per minute  
- 📊 Max 500 requests per day

---

## ⚙️ Usage

Run the app with:

```bash
python main.py
```

Then follow the graphical interface:
- Choose a sector
- Set how many days to analyze
- Select a folder to save the report
- Click **"Analisar"** and let the magic happen!

---

## 💪 Libraries

| Library         | Description                             |
|-----------------|-----------------------------------------|
| `pandas`        | Data analysis and manipulation          |
| `matplotlib`    | Generating charts and figures           |
| `alpha_vantage` | Financial data via API                  |
| `customtkinter` | Modern desktop GUI                      |
| `cryptography`  | API key encryption                      |
| `fpdf`          | Generating custom PDF reports           |

---

## 👨‍💼 Author

Developed by [Fegue3](https://github.com/Fegue3)  
🔐 Secure. 📈 Insightful. 🧠 Smart.
