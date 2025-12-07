# Project Quantum Ledger - Caezam Protocol

## Overview

This repository now contains **two distinct projects**:

1. **RRHH-LL** - Human Resources Management System (Original)
2. **Caezam Protocol** - Lottery Statistical Arbitrage Platform (New)

---

## 🎯 Caezam Protocol

**Location:** `/caezam/`

A sophisticated statistical arbitrage platform that transforms lottery participation into a quantitative trading operation.

### Key Features

- **AI-Driven Analysis:** Statistical modeling, Monte Carlo simulations, and genetic algorithms
- **Automated Pipeline:** GitHub Actions workflow running daily at 03:00 AM
- **Professional UI:** Dark-mode Bloomberg Terminal-style dashboard
- **Smart Money Management:** Kelly Criterion-based bet sizing
- **Real-time Notifications:** Telegram bot integration
- **Global Coverage:** Supports multiple international lotteries

### Technology Stack

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + Tremor
- Lucide Icons

**Backend:**
- Python 3.10
- Playwright (web scraping)
- Tesseract OCR
- NumPy, Pandas, SciPy
- DEAP (genetic algorithms)

**Infrastructure:**
- Vercel (hosting)
- Supabase (database)
- GitHub Actions (automation)
- Telegram Bot API

### Quick Links

- [Caezam README](./caezam/README.md) - Complete project documentation
- [Deployment Guide](./caezam/DEPLOYMENT.md) - Step-by-step deployment instructions
- [Database Schema](./caezam/backend/SUPABASE_SCHEMA.md) - Supabase setup
- [GitHub Workflow](./.github/workflows/caezam-pipeline.yml) - Automation pipeline

### Getting Started

```bash
# Navigate to project
cd caezam

# Install dependencies
npm install
cd backend && pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run development server
npm run dev
```

### Project Structure

```
caezam/
├── app/                    # Next.js frontend
├── backend/
│   ├── scrapers/          # Lottery data scrapers
│   ├── analyzers/         # Statistical engines
│   └── utils/             # Helper modules
├── .github/workflows/     # Automation
└── Documentation files
```

---

## 📋 RRHH-LL (Original Project)

**Location:** `/web/`, `/mobile/`, `/docs/`

Human Resources management system for tracking personnel, work logs, and payroll.

### Structure

- **web/** - Web application frontend
- **mobile/** - Mobile application
- **docs/** - Project documentation
- **documents/** - Requirements and planning

---

## Repository Navigation

```
RRHH-LL-V2/
├── caezam/                 # NEW: Lottery Arbitrage Platform
├── web/                    # RRHH web app
├── mobile/                 # RRHH mobile app
├── docs/                   # RRHH documentation
├── documents/              # RRHH planning docs
└── .github/workflows/      # CI/CD pipelines
```

---

## Development

### Caezam Protocol Development

```bash
# Frontend development
cd caezam
npm run dev

# Backend testing
cd caezam/backend
python -m scrapers.main
python -m analyzers.main
```

### RRHH Development

```bash
# Web development
cd web
npm start

# Run tests
npm test
```

---

## License

- **Caezam Protocol:** Private & Confidential - All Rights Reserved
- **RRHH-LL:** ISC License

---

## Contact

For questions about either project, please contact the development team.

**Caezam Protocol:** Built by ViMaRa (Strategy) & Co-Founder (Tech Lead)  
**RRHH-LL:** TecnoZeta2024 Team
