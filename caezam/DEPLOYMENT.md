# 🚀 Caezam Protocol - Deployment Guide

This guide provides step-by-step instructions for deploying the Caezam Protocol platform.

## Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with repository access
- [ ] Vercel account (free tier is sufficient)
- [ ] Supabase account (free tier is sufficient)
- [ ] Telegram Bot Token (optional but recommended)
- [ ] Hostinger account for DNS management (optional)

## Step 1: Supabase Setup

### 1.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Choose an organization and project name (e.g., "caezam-protocol")
4. Set a strong database password
5. Choose a region close to your users
6. Wait for project creation (~2 minutes)

### 1.2 Create Database Schema

1. Navigate to SQL Editor in your Supabase dashboard
2. Open `caezam/backend/SUPABASE_SCHEMA.md`
3. Copy and execute each CREATE TABLE statement
4. Enable Row Level Security for all tables
5. Create authentication policies

### 1.3 Get Supabase Credentials

1. Go to Project Settings → API
2. Copy the following:
   - Project URL (`SUPABASE_URL`)
   - `anon` public key (`NEXT_PUBLIC_SUPABASE_ANON_KEY`)
   - `service_role` key (`SUPABASE_KEY`)
3. Save these for later

## Step 2: Telegram Bot Setup (Optional)

### 2.1 Create Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow prompts to name your bot (e.g., "Caezam Signals Bot")
4. Copy the bot token (`TELEGRAM_BOT_TOKEN`)

### 2.2 Get Chat ID

1. Start a chat with your new bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your `chat_id` in the JSON response
5. Save this as `TELEGRAM_CHAT_ID`

## Step 3: Vercel Deployment

### 3.1 Connect Repository

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the `caezam` directory as the root

### 3.2 Configure Build Settings

- Framework Preset: Next.js
- Root Directory: `caezam`
- Build Command: `npm run build`
- Output Directory: `.next`
- Install Command: `npm install`

### 3.3 Set Environment Variables

Add the following environment variables in Vercel:

```bash
NEXT_PUBLIC_SUPABASE_URL=<your_supabase_url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your_supabase_anon_key>
SUPABASE_SERVICE_ROLE_KEY=<your_supabase_service_role_key>
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
NODE_ENV=production
```

### 3.4 Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Your app will be live at `https://your-project.vercel.app`

### 3.5 Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain (e.g., `app.caezam.online`)
3. Follow DNS configuration instructions
4. Update `NEXT_PUBLIC_APP_URL` environment variable

## Step 4: GitHub Actions Setup

### 4.1 Configure Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following secrets:

```
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_service_role_key>
TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
TELEGRAM_CHAT_ID=<your_telegram_chat_id>
```

### 4.2 Enable Workflow

1. Go to Actions tab in your repository
2. Enable GitHub Actions if not already enabled
3. The workflow is configured to run at 03:00 AM UTC daily
4. You can also trigger it manually:
   - Go to Actions → Caezam Lottery Data Pipeline
   - Click "Run workflow"

### 4.3 Test Workflow

1. Manually trigger the workflow
2. Monitor the execution
3. Check for any errors
4. Verify data appears in Supabase
5. Check if Telegram notification is received

## Step 5: Supabase Authentication Setup

### 5.1 Enable Email Authentication

1. Go to Authentication → Providers in Supabase
2. Enable Email provider
3. Configure email templates (optional)
4. Set up email confirmation (optional)

### 5.2 Create First User

1. Go to Authentication → Users
2. Click "Add user"
3. Enter email and password
4. Confirm email (if required)

## Step 6: DNS Configuration (Optional)

### 6.1 Hostinger Setup

1. Log into Hostinger DNS management
2. Add CNAME record:
   - Name: `app`
   - Points to: `cname.vercel-dns.com`
   - TTL: 14400
3. Wait for DNS propagation (up to 24 hours)

## Step 7: Post-Deployment Verification

### 7.1 Frontend Checks

- [ ] Visit your deployed URL
- [ ] Verify dark theme loads correctly
- [ ] Check all dashboard elements render
- [ ] Test responsiveness on mobile
- [ ] Verify no console errors

### 7.2 Backend Checks

- [ ] Manually trigger GitHub Action
- [ ] Check workflow completes successfully
- [ ] Verify data inserted into Supabase
- [ ] Check Telegram notification received
- [ ] Review logs for any warnings

### 7.3 Database Checks

- [ ] Connect to Supabase
- [ ] Verify tables exist
- [ ] Check sample data in `draws` table
- [ ] Verify `recommendations` table populated
- [ ] Check RLS policies are active

## Step 8: Monitoring & Maintenance

### 8.1 Set Up Monitoring

1. **Vercel Analytics**
   - Enable in Vercel dashboard
   - Monitor page performance

2. **Supabase Logs**
   - Check daily for errors
   - Monitor database size

3. **GitHub Actions**
   - Review workflow runs daily
   - Set up email notifications for failures

### 8.2 Regular Maintenance

- **Weekly:** Review recommendation quality
- **Monthly:** Check bankroll calculations
- **Quarterly:** Update scraper selectors if sites change
- **As needed:** Update Python/Node dependencies

## Step 9: Scaling Considerations

### 9.1 Database Optimization

- Add indexes for frequently queried fields
- Archive old draws (keep last 2 years)
- Implement database backups

### 9.2 Performance Optimization

- Enable Vercel Edge caching
- Optimize images and assets
- Consider CDN for static content

### 9.3 Adding More Lotteries

1. Create new scraper class extending `BaseScraper`
2. Add to `scrapers/main.py`
3. Test scraper independently
4. Deploy and monitor

## Troubleshooting

### Build Fails on Vercel

- Check environment variables are set
- Verify Node.js version (18+)
- Review build logs for specific errors

### GitHub Action Fails

- Check secrets are configured
- Verify Python dependencies install
- Test scrapers locally first
- Check if target websites changed

### No Data in Supabase

- Verify database credentials
- Check RLS policies
- Review GitHub Action logs
- Test Supabase connection locally

### Telegram Notifications Not Working

- Verify bot token is correct
- Check chat ID is accurate
- Test bot responds to `/start`
- Review GitHub Action logs

## Support & Documentation

- **Frontend Issues:** Check Next.js docs
- **Backend Issues:** Review Python/Playwright docs
- **Database Issues:** Supabase documentation
- **Deployment Issues:** Vercel support

## Security Checklist

- [ ] All secrets stored in environment variables
- [ ] No credentials in code
- [ ] RLS enabled on all tables
- [ ] HTTPS enforced on frontend
- [ ] Telegram bot token secured
- [ ] Regular dependency updates

---

**Deployment Status: Ready for Production** ✅

*Last updated: December 2024*
