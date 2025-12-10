# Bitcoin Advisor - AI-Powered Trading Signals

> Real-time Bitcoin trading signals using RSI technical analysis and news sentiment powered by OM1 and Next.js

## 🎯 Overview

Bitcoin Advisor is an intelligent trading signal platform that combines:
- **RSI (14-period)** technical analysis from real-time Binance data
- **News sentiment** analysis from CryptoPanic using VADER
- **AI-powered insights** via GPT-4o for signal reasoning
- **Real-time alerts** through WebSocket connections

## 🏗️ Architecture

This is a **monorepo** with two main applications:

```
dogma/
├── apps/
│   ├── web/              # Next.js 15 frontend (React 19 + TypeScript)
│   └── om1-runtime/      # OM1 Python agent runtime
├── packages/             # Shared packages (future)
└── INVESTMENT_ADVISOR_ARCHITECTURE.md  # Detailed architecture doc
```

## 📋 Prerequisites

- **Node.js** 18+ and **pnpm** 8+
- **Python** 3.10+
- **Docker** and **Docker Compose** (for containerized deployment)
- **API Keys**:
  - OpenAI API key (GPT-4o)
  - CryptoPanic API key (free tier)
  - OM1 API key

## 🚀 Quick Start

### 1. Clone and Install

```bash
# Clone the repository
git clone <your-repo-url>
cd dogma

# Environment is already configured with Groq API!
# Check .env file - Groq API key is already set up
cat .env
```

> ✅ **Groq API is pre-configured** - You can start immediately!

### 2. Install Dependencies

#### Next.js App
```bash
# Install all dependencies (root + apps)
pnpm install
```

#### Python OM1 Runtime
```bash
cd apps/om1-runtime

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install OM1 SDK (follow official documentation)
# pip install om1
```

### 3. Run Development

#### Option A: Run Both Apps Separately

**Terminal 1 - Next.js:**
```bash
pnpm dev
```

**Terminal 2 - OM1 Runtime:**
```bash
cd apps/om1-runtime
source venv/bin/activate
python src/run.py start bitcoin_advisor
```

#### Option B: Run with Docker Compose

```bash
docker-compose up -d
```

### 4. Access the Application

- **Web App**: http://localhost:3000
- **OM1 Runtime API**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📦 Project Structure

### Next.js App (`apps/web/`)

```
apps/web/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components (to be added)
│   ├── bitcoin/          # BTC-specific components
│   ├── sentiment/        # Sentiment components
│   └── ui/               # Shared UI components
├── lib/                  # Utilities (to be added)
│   ├── om1/             # OM1 integration
│   ├── bitcoin/         # Bitcoin utilities
│   └── sentiment/       # Sentiment utilities
└── public/              # Static assets
```

### OM1 Runtime (`apps/om1-runtime/`)

```
apps/om1-runtime/
├── config/                    # Agent configurations
│   └── bitcoin_advisor.json5 # Bitcoin agent config
├── src/
│   ├── inputs/               # Custom input plugins
│   │   ├── bitcoin_price_rsi/
│   │   ├── news_sentiment/
│   │   └── portfolio_state/
│   ├── actions/              # Custom action plugins
│   │   ├── analyze_bitcoin/
│   │   ├── generate_signal/
│   │   └── send_alert/
│   └── run.py               # Entry point
├── connectors/              # API connectors
│   ├── binance_connector.py
│   └── cryptopanic_connector.py
└── utils/                   # Utility functions
    ├── rsi.py
    └── sentiment.py
```

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 15 + React 19 | Web framework |
| Styling | Tailwind CSS | Utility-first CSS |
| UI Components | Radix UI + shadcn/ui | Component library |
| AI Runtime | OM1 | Agent orchestration |
| LLM | GPT-4o | Signal reasoning |
| Database | PostgreSQL | Data storage |
| Caching | Redis | Price/RSI caching |
| Crypto Data | Binance API | Free BTC data |
| News | CryptoPanic API | Crypto news |
| Sentiment | VADER | NLP sentiment |
| Charts | Recharts | Visualization |
| Deployment | Docker Compose | Containerization |

## 📝 Available Scripts

### Root (Monorepo)
- `pnpm dev` - Run Next.js dev server
- `pnpm build` - Build Next.js app
- `pnpm lint` - Lint Next.js app
- `pnpm typecheck` - TypeScript type checking

### OM1 Runtime
```bash
cd apps/om1-runtime
python src/run.py start bitcoin_advisor   # Start agent
python src/run.py stop bitcoin_advisor    # Stop agent
python src/run.py status                  # Check status
```

## 🔑 Environment Variables

See `.env.example` for all required environment variables.

### Required API Keys

1. **Groq API** (Recommended): https://console.groq.com/keys - **FREE tier available!**
   - Ultra-fast LLM inference (10x faster than OpenAI)
   - 80% cost savings vs OpenAI
   - OpenAI-compatible API
2. **News API**: https://api-production-729e.up.railway.app/news (no key required)
3. **OM1 Runtime**: https://openmind.org (check pricing)

### Optional API Keys

- **OpenAI API**: https://platform.openai.com/api-keys (alternative to Groq)
- **CryptoPanic**: https://cryptopanic.com/developers/api/ (alternative news source)

### Cost Breakdown (Monthly)

**Option 1: With Groq (Recommended)**
- Binance API: **$0** (free)
- News API: **$0** (free)
- Groq API: **~$20-30** (with free tier)
- OM1 Runtime: **TBD**
- Infrastructure: **~$20** (if self-hosted)
- **Total**: **~$40-50/month** 💰

**Option 2: With OpenAI**
- Binance API: **$0** (free)
- News API: **$0** (free)
- OpenAI GPT-4o: **~$100-150** (usage-based)
- OM1 Runtime: **TBD**
- Infrastructure: **~$20** (if self-hosted)
- **Total**: **~$120-170/month**

**Savings with Groq: ~$80-120/month!** 🎉

## 🐳 Docker Deployment

### Build and Run
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Individual Services
```bash
# Start only web app
docker-compose up web

# Start only OM1 runtime
docker-compose up om1-runtime

# Restart a service
docker-compose restart web
```

## 🔍 Development

### Adding New Features

This is a **framework setup only**. No features are implemented yet. When ready to add features:

1. **Bitcoin Price Tracking**: Implement `lib/bitcoin/connectors.ts`
2. **RSI Calculation**: Implement `lib/bitcoin/rsi.ts`
3. **Sentiment Analysis**: Implement `lib/sentiment/analyzer.ts`
4. **OM1 Integration**: Implement `lib/om1/client.ts`
5. **UI Components**: Add components in `components/bitcoin/`, `components/sentiment/`

### Next Steps

See `INVESTMENT_ADVISOR_ARCHITECTURE.md` for detailed implementation phases.

**Phase 1: Foundation** (Current)
- ✅ Monorepo setup
- ✅ Next.js app scaffolding
- ✅ OM1 runtime structure
- ✅ Docker configuration
- ⏳ Authentication system

**Phase 2: Data Integration**
- ⏳ Bitcoin price connector
- ⏳ RSI calculator
- ⏳ News sentiment analyzer

**Phase 3: Agent Development**
- ⏳ OM1 agent configuration
- ⏳ Input plugins
- ⏳ Action plugins

**Phase 4: UI/UX**
- ⏳ Dashboard components
- ⏳ Real-time WebSocket
- ⏳ Charts and visualizations

**Phase 5: Testing & Deployment**
- ⏳ Integration tests
- ⏳ Production deployment

## 📚 Documentation

- **Architecture**: `INVESTMENT_ADVISOR_ARCHITECTURE.md`
- **OM1 Runtime**: `apps/om1-runtime/README.md`
- **OM1 Docs**: https://github.com/openmind/om1

## 🤝 Contributing

This is a hackathon project. Contributions are welcome after the initial implementation phase.

## 📄 License

MIT

## 🔗 Links

- **OM1 Framework**: https://github.com/openmind/om1
- **Next.js**: https://nextjs.org
- **Binance API**: https://binance-docs.github.io/apidocs/spot/en
- **CryptoPanic**: https://cryptopanic.com/developers/api/
- **OpenAI**: https://platform.openai.com

---

**Status**: 🏗️ Framework Setup Complete - Ready for Feature Implementation

Built with ❤️ for the hackathon
