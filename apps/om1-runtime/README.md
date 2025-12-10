# OM1 Runtime - Bitcoin Advisor Agent

AI agent runtime for Bitcoin trading signal generation using OM1 framework.

## Prerequisites

- Python 3.10+
- OM1 SDK (install following [official documentation](https://github.com/openmind/om1))

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install OM1 SDK:
```bash
# Follow OM1 installation instructions
pip install om1  # Or as per official docs
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

The agent configuration is in `config/bitcoin_advisor.json5`.

## Running the Agent

```bash
python src/run.py start bitcoin_advisor
```

## Project Structure

```
om1-runtime/
├── config/                     # Agent configurations
│   └── bitcoin_advisor.json5
├── src/
│   ├── inputs/                 # Custom input plugins
│   │   ├── bitcoin_price_rsi/
│   │   ├── news_sentiment/
│   │   └── portfolio_state/
│   ├── actions/                # Custom action plugins
│   │   ├── analyze_bitcoin/
│   │   ├── generate_signal/
│   │   └── send_alert/
│   └── run.py                  # Entry point
├── connectors/                 # API connectors
│   ├── binance_connector.py
│   ├── coingecko_connector.py
│   └── cryptopanic_connector.py
└── utils/                      # Utility functions
    ├── rsi.py
    └── sentiment.py
```

## Development

This runtime is part of a monorepo. See root README for full project setup.
