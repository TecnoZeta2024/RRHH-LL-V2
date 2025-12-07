# Supabase Database Schema

This document describes the database schema for the Caezam Protocol.

## Tables

### 1. `draws`
Stores historical lottery draw results.

```sql
CREATE TABLE draws (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lottery_name TEXT NOT NULL,
  draw_date TEXT,
  numbers INTEGER[] NOT NULL,
  bonus_numbers INTEGER[],
  jackpot TEXT,
  extraction_method TEXT DEFAULT 'text',
  scraped_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Indexes
  CONSTRAINT draws_lottery_date_unique UNIQUE (lottery_name, draw_date)
);

CREATE INDEX idx_draws_lottery ON draws(lottery_name);
CREATE INDEX idx_draws_date ON draws(draw_date DESC);
```

### 2. `recommendations`
Stores AI-generated lottery combination recommendations.

```sql
CREATE TABLE recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lottery_name TEXT NOT NULL,
  rank INTEGER NOT NULL,
  combination INTEGER[] NOT NULL,
  confidence_score NUMERIC(5, 2),
  genetic_score NUMERIC(5, 2),
  monte_carlo_score NUMERIC(5, 2),
  kelly_fraction NUMERIC(5, 4),
  analysis_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_recommendations_lottery ON recommendations(lottery_name);
CREATE INDEX idx_recommendations_date ON recommendations(analysis_date DESC);
```

### 3. `bankroll`
Tracks bankroll and performance metrics.

```sql
CREATE TABLE bankroll (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  current_amount NUMERIC(12, 2) NOT NULL,
  initial_amount NUMERIC(12, 2) NOT NULL,
  total_invested NUMERIC(12, 2) DEFAULT 0,
  total_won NUMERIC(12, 2) DEFAULT 0,
  roi_percentage NUMERIC(7, 2) DEFAULT 0,
  win_rate NUMERIC(5, 2) DEFAULT 0,
  max_drawdown NUMERIC(7, 2) DEFAULT 0,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 4. `manual_input_flags`
Flags lotteries that need manual data entry.

```sql
CREATE TABLE manual_input_flags (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lottery_name TEXT NOT NULL,
  needs_input BOOLEAN DEFAULT TRUE,
  flagged_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  resolved_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_flags_lottery ON manual_input_flags(lottery_name);
CREATE INDEX idx_flags_needs_input ON manual_input_flags(needs_input);
```

### 5. `bets` (Optional - for tracking actual bets)
Tracks actual lottery ticket purchases.

```sql
CREATE TABLE bets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  lottery_name TEXT NOT NULL,
  combination INTEGER[] NOT NULL,
  amount NUMERIC(10, 2) NOT NULL,
  recommendation_id UUID REFERENCES recommendations(id),
  draw_date TEXT,
  result TEXT, -- 'pending', 'win', 'loss'
  winnings NUMERIC(12, 2) DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bets_lottery ON bets(lottery_name);
CREATE INDEX idx_bets_result ON bets(result);
```

## Row Level Security (RLS)

Enable RLS for all tables and create policies for authenticated users only:

```sql
-- Enable RLS
ALTER TABLE draws ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE bankroll ENABLE ROW LEVEL SECURITY;
ALTER TABLE manual_input_flags ENABLE ROW LEVEL SECURITY;
ALTER TABLE bets ENABLE ROW LEVEL SECURITY;

-- Create policies (allow authenticated users only)
CREATE POLICY "Allow authenticated users" ON draws
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users" ON recommendations
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users" ON bankroll
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users" ON manual_input_flags
  FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users" ON bets
  FOR ALL USING (auth.role() = 'authenticated');
```

## Setup Instructions

1. Create a new Supabase project at https://supabase.com
2. Go to the SQL Editor
3. Run the SQL commands above to create the schema
4. Copy your project URL and API keys to `.env` file
5. Enable Email authentication in Supabase Auth settings
