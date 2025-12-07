"""
Base Scraper Class for Lottery Data Extraction
Provides common functionality for all lottery scrapers
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime
import logging
from playwright.sync_api import sync_playwright, Page, Browser
from fake_useragent import UserAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for lottery scrapers"""
    
    def __init__(self, lottery_name: str, base_url: str):
        self.lottery_name = lottery_name
        self.base_url = base_url
        self.ua = UserAgent()
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    def setup_browser(self) -> None:
        """Initialize Playwright browser with stealth settings"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        context = self.browser.new_context(
            user_agent=self.ua.random,
            viewport={'width': 1920, 'height': 1080},
            locale='es-ES'
        )
        
        self.page = context.new_page()
        logger.info(f"Browser initialized for {self.lottery_name}")
    
    def close_browser(self) -> None:
        """Clean up browser resources"""
        if self.browser:
            self.browser.close()
            logger.info(f"Browser closed for {self.lottery_name}")
    
    @abstractmethod
    def scrape_latest_draw(self) -> Optional[Dict]:
        """
        Scrape the latest lottery draw results
        Must be implemented by each lottery scraper
        
        Returns:
            Dict with keys: 'draw_date', 'numbers', 'bonus_numbers', 'jackpot', etc.
        """
        pass
    
    @abstractmethod
    def scrape_historical_data(self, limit: int = 100) -> List[Dict]:
        """
        Scrape historical lottery draws
        Must be implemented by each lottery scraper
        
        Args:
            limit: Maximum number of historical draws to fetch
            
        Returns:
            List of draw dictionaries
        """
        pass
    
    def run(self) -> Dict[str, any]:
        """
        Main execution method
        
        Returns:
            Dictionary with 'success', 'data', and 'error' keys
        """
        try:
            self.setup_browser()
            latest = self.scrape_latest_draw()
            
            return {
                'success': True,
                'lottery': self.lottery_name,
                'data': latest,
                'timestamp': datetime.utcnow().isoformat(),
                'error': None
            }
        except Exception as e:
            logger.error(f"Error scraping {self.lottery_name}: {str(e)}")
            return {
                'success': False,
                'lottery': self.lottery_name,
                'data': None,
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }
        finally:
            self.close_browser()
