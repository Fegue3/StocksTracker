# 📊 STOCKSTRACKER

> _Empower your investments with insightful market analysis._

![last commit](https://img.shields.io/badge/last%20commit-today-blue) ![language](https://img.shields.io/badge/python-100%25-blue) ![languages](https://img.shields.io/badge/languages-1-brightgreen)

**Built with:**

- ![JSON](https://img.shields.io/badge/-JSON-black?logo=json&style=flat-square)
- ![Python](https://img.shields.io/badge/-Python-blue?logo=python&style=flat-square)

---

## 📌 Table of Contents

- [📖 Overview](#-overview)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [🔑 Alpha Vantage API](#-alpha-vantage-api)
  - [Getting your API Key](#getting-your-api-key)
  - [API Limitations](#api-limitations)
- [⚙️ Usage](#️-usage)
- [🛠 Libraries](#-libraries)
- [👨‍💻 Author](#-author)

---

## 📖 Overview

StocksTracker is a Python project that provides detailed analyses and financial charts of stock market data, utilizing financial APIs such as Alpha Vantage to offer valuable insights to investors.

---

## 🚀 Getting Started

### Prerequisites

To run StocksTracker, you will need:

- Python 3.7 or higher
- pip (Python package manager)

### Installation

Install the required libraries using pip:

```bash
pip install pandas matplotlib requests alpha_vantage
```

---

## 🔑 Alpha Vantage API

StocksTracker uses the Alpha Vantage API to retrieve real-time financial data.

### Getting your API Key

To use Alpha Vantage:

1. Visit the [Alpha Vantage website](https://www.alphavantage.co/support/#api-key).
2. Register for free.
3. Copy the provided API key after registration.
4. Insert this key into your StocksTracker project in the configuration file or directly into the code as instructed.

```python
ALPHA_VANTAGE_KEY = 'YOUR_API_KEY_HERE'
```

### API Limitations

The free version of the Alpha Vantage API has a limit of 5 requests per minute and 500 requests per day. Consider these limitations when using StocksTracker for extensive data fetching.

---

## ⚙️ Usage

Run the main StocksTracker script with:

```bash
python main.py
```

The program interface will guide you in selecting stocks, sectors, and generating detailed financial reports and charts.

---

## 🛠 Libraries

Libraries used:

| Library         | Description                           |
|-----------------|---------------------------------------|
| pandas          | Data manipulation and analysis        |
| matplotlib      | Creation of detailed charts           |
| requests        | HTTP requests for APIs                |
| alpha_vantage   | Direct integration with Alpha Vantage |

---

## 👨‍💻 Author

- Developed by [Fegue3](https://github.com/Fegue3).