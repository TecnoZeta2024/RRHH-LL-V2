"""
Powerball Lottery Scraper
Scrapes data from the official Powerball website
"""
from typing import Dict, List, Optional
import logging
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class PowerballScraper(BaseScraper):
    """Scraper for Powerball lottery"""
    
    def __init__(self):
        super().__init__(
            lottery_name="Powerball",
            base_url="https://www.powerball.com/previous-results"
        )
    
    def scrape_latest_draw(self) -> Optional[Dict]:
        """Scrape the latest Powerball draw"""
        try:
            self.page.goto(self.base_url, wait_until='domcontentloaded', timeout=30000)
            self.page.wait_for_selector('.item-powerball', timeout=10000)
            
            # Extract draw date
            draw_date_elem = self.page.query_selector('.card-title')
            draw_date = draw_date_elem.inner_text() if draw_date_elem else None
            
            # Extract main numbers
            main_numbers = []
            number_elements = self.page.query_selector_all('.item-powerball .white-balls .item-ball')
            for elem in number_elements[:5]:
                main_numbers.append(int(elem.inner_text()))
            
            # Extract Powerball number
            powerball_elem = self.page.query_selector('.item-powerball .powerball .item-ball')
            powerball = int(powerball_elem.inner_text()) if powerball_elem else None
            
            # Extract jackpot (if available)
            jackpot_elem = self.page.query_selector('.item-powerball .jackpot-amount')
            jackpot = jackpot_elem.inner_text() if jackpot_elem else None
            
            result = {
                'draw_date': draw_date,
                'numbers': main_numbers,
                'bonus_numbers': [powerball] if powerball else [],
                'jackpot': jackpot,
                'lottery_type': 'powerball'
            }
            
            logger.info(f"Powerball scraped successfully: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping Powerball: {str(e)}")
            return None
    
    def scrape_historical_data(self, limit: int = 100) -> List[Dict]:
        """Scrape historical Powerball draws"""
        try:
            self.page.goto(self.base_url, wait_until='domcontentloaded', timeout=30000)
            
            draws = []
            draw_elements = self.page.query_selector_all('.item-powerball')[:limit]
            
            for draw_elem in draw_elements:
                # Extract date
                date_elem = draw_elem.query_selector('.card-title')
                draw_date = date_elem.inner_text() if date_elem else None
                
                # Extract main numbers
                main_numbers = []
                number_elements = draw_elem.query_selector_all('.white-balls .item-ball')
                for elem in number_elements[:5]:
                    main_numbers.append(int(elem.inner_text()))
                
                # Extract Powerball
                powerball_elem = draw_elem.query_selector('.powerball .item-ball')
                powerball = int(powerball_elem.inner_text()) if powerball_elem else None
                
                draws.append({
                    'draw_date': draw_date,
                    'numbers': main_numbers,
                    'bonus_numbers': [powerball] if powerball else [],
                    'lottery_type': 'powerball'
                })
            
            logger.info(f"Scraped {len(draws)} historical Powerball draws")
            return draws
            
        except Exception as e:
            logger.error(f"Error scraping Powerball history: {str(e)}")
            return []
