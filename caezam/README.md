# 🎯 CAEZAM PROTOCOL - Quantum Ledger v1.0

> **"We don't play, we operate."**

A statistical arbitrage platform that transforms lottery participation from a game of chance into a data-driven investment operation. Built on the principle of **Arbitrage Estadístico**, Caezam ingests global lottery data, processes patterns through AI and stochastic simulations, and delivers optimized investment signals with professional money management.

## 🌟 Vision

Transform lottery participation into a quantitative trading operation by:
- Analyzing massive lottery datasets with AI
- Running Monte Carlo simulations (100,000+ iterations)
- Using genetic algorithms for combination optimization
- Applying Kelly Criterion for bankroll management
- Delivering confidence-scored recommendations

## 🏗️ Architecture

### **Frontend (Next.js 14)**
- **Framework:** Next.js 14 with TypeScript & App Router
- **Hosting:** Vercel (linked to `app.caezam.online`)
- **UI:** Tailwind CSS + Tremor components + Lucide Icons
- **Auth:** Supabase Authentication
- **Style:** Dark mode Bloomberg Terminal aesthetic

### **Backend (Python 3.10)**
- **Orchestrator:** GitHub Actions (CRON schedule: 03:00 AM daily)
- **Database:** Supabase (PostgreSQL)
- **Scraping:** Playwright + Tesseract OCR (for Bolivia lottery)
- **Algorithms:** NumPy, Pandas, SciPy, Scikit-learn, DEAP
- **Notifications:** Telegram Bot API

### **Infrastructure**
- **Hosting:** Vercel (Frontend) + GitHub Actions (Backend)
- **DNS:** Hostinger (`caezam.online`)
- **Database:** Supabase
- **CI/CD:** GitHub Actions
- **Secrets:** GitHub Secrets + Environment Variables

## 📊 Core Algorithms

### 1. **Data Ingestion (Ninja Scraper)**
- Playwright-based scrapers for global lotteries
- Hybrid OCR extraction for Bolivia's Lonabol
- Automatic fallback to manual input on failure

### 2. **Statistical Analysis**
- Frequency distribution analysis
- Hot/cold number identification
- Volatility calculation (6-month window)
- Extreme combination filtering

### 3. **Monte Carlo Simulation**
- 100,000+ virtual draws per analysis
- Tests combination resilience under volatility
- Calculates match probabilities (3+, 4+, 5+ matches)
- Generates resilience scores

### 4. **Genetic Algorithm Optimization**
- Population-based evolution
- Tournament selection
- Two-point crossover with repair
- Mutation with duplicate prevention
- 50 generations per run

### 5. **Kelly Criterion Money Management**
- Fractional Kelly (25% for safety)
- Calculates optimal bet sizing
- Caps maximum bet at 5% of bankroll
- Dynamic edge calculation from confidence scores

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase account
- Telegram Bot (optional)

### 1. Clone & Install

```bash
cd caezam

# Install frontend dependencies
npm install

# Install backend dependencies
cd backend
pip install -r requirements.txt
playwright install chromium
```

### 2. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
SUPABASE_KEY=your_service_role_key

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. Database Setup

1. Create a Supabase project
2. Run the SQL schema from `backend/SUPABASE_SCHEMA.md`
3. Enable Row Level Security
4. Create auth policies

### 4. Run Locally

**Frontend:**
```bash
npm run dev
# Open http://localhost:3000
```

**Backend (scraper):**
```bash
cd backend
python -m scrapers.main
```

**Backend (analyzer):**
```bash
cd backend
python -m analyzers.main
```

## 📦 Project Structure

```
caezam/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Root layout with dark theme
│   ├── page.tsx             # Main dashboard
│   └── globals.css          # Global styles
├── backend/
│   ├── scrapers/            # Lottery scrapers
│   │   ├── base_scraper.py
│   │   ├── powerball_scraper.py
│   │   ├── lonabol_scraper.py
│   │   └── main.py          # Scraper orchestrator
│   ├── analyzers/           # Analysis engines
│   │   ├── statistical_analyzer.py
│   │   ├── monte_carlo.py
│   │   ├── genetic_optimizer.py
│   │   └── main.py          # Analysis orchestrator
│   ├── utils/               # Utilities
│   │   ├── supabase_client.py
│   │   ├── kelly_criterion.py
│   │   └── telegram_notifier.py
│   ├── requirements.txt     # Python dependencies
│   └── SUPABASE_SCHEMA.md   # Database schema
├── .github/
│   └── workflows/
│       └── caezam-pipeline.yml  # Automated pipeline
├── .env.example             # Environment template
└── README.md               # This file
```

## 🎮 Features (MVP)

### ✅ Implemented
- [x] Dashboard with KPIs (Bankroll, ROI, Win Rate, Drawdown)
- [x] War Room with top 3 signal cards
- [x] Confidence scoring system
- [x] Kelly Criterion bet sizing
- [x] Statistical analysis engine
- [x] Monte Carlo simulator (100k runs)
- [x] Genetic algorithm optimizer
- [x] Base scraper architecture
- [x] Powerball scraper
- [x] Bolivia (Lonabol) scraper with OCR
- [x] Supabase integration
- [x] Telegram notifications
- [x] GitHub Actions automation

### 🔮 Roadmap (v2.0)
- [ ] Interactive backtesting engine
- [ ] Multi-currency support (Bs, USD, EUR)
- [ ] Additional lottery scrapers (Mega Millions, EuroMillions)
- [ ] Real-time bet tracking
- [ ] Performance charts with TradingView
- [ ] Mobile PWA optimization

## 🔐 Security & Secrets

**GitHub Secrets Required:**
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

**Never commit:**
- `.env` files
- API keys
- Database credentials
- Private keys

## 📈 Data Pipeline Flow

1. **TRIGGER** (03:00 AM daily) → GitHub Action starts
2. **SCRAPE** → Playwright extracts lottery data
   - Success: Store in Supabase
   - Failure: Flag for manual input
3. **ANALYZE** → Run statistical analysis + MC + GA
4. **STORE** → Save top 3 recommendations to DB
5. **NOTIFY** → Send Telegram message
6. **VIEW** → User accesses dashboard to see signals

## 🧪 Testing

```bash
# Run Python tests
cd backend
pytest tests/

# Run frontend build check
npm run build
```

## 🚢 Deployment

### Frontend (Vercel)
1. Connect GitHub repo to Vercel
2. Set environment variables
3. Deploy from `caezam` directory
4. Configure custom domain: `app.caezam.online`

### Backend (GitHub Actions)
1. Add secrets to GitHub repository
2. Workflow runs automatically at 03:00 AM
3. Manual trigger: Actions → Caezam Pipeline → Run workflow

## 📊 Supported Lotteries

- ✅ **Powerball** (USA)
- ✅ **Lonabol** (Bolivia) - with OCR support
- 🔜 Mega Millions (USA)
- 🔜 EuroMillions (Europe)
- 🔜 EuroJackpot (Europe)
- 🔜 La Primitiva (Spain)

## 🤝 Contributing

This is a private strategic project. Contact the team for collaboration opportunities.

## 📝 License

Private & Confidential - All Rights Reserved

---

**Built with 🧠 by ViMaRa (Strategy) & Co-Founder (Tech Lead)**

*Caezam Protocol v1.0 - Quantum Ledger*
