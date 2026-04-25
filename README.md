# 🧠 RESA — Real-time Economic Strategy Advisor

**RESA** is an AI-powered business strategy web app built for Malaysian online small business owners. Input your inventory, describe your business situation, and RESA generates a tailored, data-grounded strategy — including content plans, pricing recommendations, cash flow actions, and ready-to-use social media assets in Manglish.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the App](#running-the-app)
- [Usage](#-usage)
- [Internal Datasets](#-internal-datasets)
- [Environment Variables](#-environment-variables)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 📊 **Inventory Analysis** — Input items with cost price, selling price, stock quantity, and units sold; RESA computes margins and revenue automatically
- 🤖 **AI Strategy Generation** — Powered by an LLM (via Anthropic-compatible API), RESA generates a personalised, numbered action plan grounded in your actual numbers
- 📁 **Platform Data Upload** — Upload your own Shopee, Lazada, or TikTok Shop export (CSV/XLSX) for deeper analysis
- 📡 **Streaming Support** — Strategy output streams in real-time via Server-Sent Events (SSE)
- 🗂️ **Internal Market Datasets** — Drop any CSV/Excel market data into the `datasets/` folder and RESA uses it as background intelligence automatically
- 📱 **Content & Campaign Assets** — Generates ready-to-use captions, hashtags, bundle mechanics, and a 7-day posting schedule in Manglish tone

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Client | Anthropic Python SDK (`anthropic`) |
| Data Processing | Pandas, OpenPyXL |
| HTTP | HTTPX (custom timeout for slow proxy responses) |
| Frontend | Jinja2 Templates, HTML/CSS |
| Config | python-dotenv |

---

## 📁 Project Structure

```
4flat-main/
├── app.py                  # Flask app — routes and request handling
├── glm_client.py           # Anthropic API client (supports streaming)
├── prompt_engine.py        # System prompt (RESA's persona) and user prompt builder
├── data_handler.py         # CSV/XLSX parsing, inventory summary, dataset loader
├── requirements.txt        # Python dependencies
├── .env                    # API keys and model config (not committed)
├── datasets/               # Internal market datasets (drop CSVs/XLSXs here)
│   └── README.txt
├── static/
│   └── style.css
└── templates/
    ├── index.html          # Main input form
    └── result.html         # Strategy output page
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip
- An Anthropic-compatible API key (supports proxies such as `api.ilmu.ai`)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/4flat.git
cd 4flat
```

2. **Create and activate a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root (copy from the example below):

```env
ANTHROPIC_AUTH_TOKEN=your_api_key_here
ANTHROPIC_BASE_URL=https://api.ilmu.ai/anthropic
ANTHROPIC_MODEL=ilmu-glm-5.1
```

> See [Environment Variables](#-environment-variables) for a full description of each variable.

### Running the App

```bash
python app.py
```

The app will start on `http://localhost:5000` by default.

---

## 📖 Usage

1. Open `http://localhost:5000` in your browser
2. Fill in your **Business Name**, **Business Type**, and a short **Business Context** (e.g. upcoming sale, cash flow pressure, new product launch)
3. Add your **inventory items** — name, cost price, selling price, stock quantity, and units sold
4. *(Optional)* Upload a platform export file (CSV or XLSX) from Shopee, Lazada, or TikTok Shop
5. Click **Analyse** — RESA streams back a full strategy with:
   - Situation analysis
   - Strategic decision rationale
   - Numbered action plan
   - Social media content and campaign assets
   - Cost and margin flags
   - 7–14 day projected impact
   - Plain-language summary in Manglish

---

## 🗂️ Internal Datasets

RESA automatically loads any `.csv` or `.xlsx` files placed inside the `datasets/` folder as background market intelligence. No code changes required.

Suggested datasets to add:
- Shopee / Lazada trending products
- TikTok Shop sales benchmarks
- Malaysian SME sales data
- Fashion, F&B, or beauty market trend data

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_AUTH_TOKEN` | Your API key for the Anthropic-compatible endpoint |
| `ANTHROPIC_BASE_URL` | Base URL of the API proxy (e.g. `https://api.ilmu.ai/anthropic`) |
| `ANTHROPIC_MODEL` | Model identifier to use (e.g. `ilmu-glm-5.1`) |

---

