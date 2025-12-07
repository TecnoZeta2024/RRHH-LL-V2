"""
Main Scraper Orchestrator
Coordinates all lottery scrapers and saves results to Supabase
"""
import os
import sys
import logging
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.powerball_scraper import PowerballScraper
from scrapers.lonabol_scraper import LonabolScraper
from utils.supabase_client import SupabaseClient

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperOrchestrator:
    """Orchestrates all lottery scrapers"""
    
    def __init__(self):
        self.scrapers = [
            PowerballScraper(),
            LonabolScraper(),
            # Add more scrapers here:
            # MegaMillionsScraper(),
            # EuroMillionsScraper(),
            # etc.
        ]
        self.supabase = SupabaseClient()
    
    def run_all_scrapers(self) -> List[Dict]:
        """
        Run all lottery scrapers
        
        Returns:
            List of scraping results
        """
        results = []
        
        for scraper in self.scrapers:
            logger.info(f"Running scraper for {scraper.lottery_name}")
            result = scraper.run()
            results.append(result)
            
            # Save to database if successful
            if result['success'] and result['data']:
                self.save_draw_to_database(result)
            else:
                # Check if manual input is needed (for Lonabol)
                if hasattr(scraper, 'needs_manual_input') and scraper.needs_manual_input:
                    self.flag_manual_input_needed(scraper.lottery_name)
        
        return results
    
    def save_draw_to_database(self, result: Dict) -> None:
        """
        Save lottery draw result to Supabase
        
        Args:
            result: Scraping result dictionary
        """
        try:
            draw_data = result['data']
            
            record = {
                'lottery_name': result['lottery'],
                'draw_date': draw_data.get('draw_date'),
                'numbers': draw_data.get('numbers', []),
                'bonus_numbers': draw_data.get('bonus_numbers', []),
                'jackpot': draw_data.get('jackpot'),
                'extraction_method': draw_data.get('extraction_method', 'text'),
                'scraped_at': result['timestamp'],
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.supabase.insert_draw(record)
            logger.info(f"Saved {result['lottery']} draw to database: {response}")
            
        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
    
    def flag_manual_input_needed(self, lottery_name: str) -> None:
        """
        Flag that a lottery needs manual input
        
        Args:
            lottery_name: Name of the lottery
        """
        try:
            flag_record = {
                'lottery_name': lottery_name,
                'needs_input': True,
                'flagged_at': datetime.utcnow().isoformat()
            }
            
            self.supabase.flag_manual_input(flag_record)
            logger.warning(f"Flagged {lottery_name} for manual input")
            
        except Exception as e:
            logger.error(f"Error flagging manual input: {str(e)}")


def main():
    """Main execution function"""
    logger.info("Starting Caezam Lottery Scraper Pipeline")
    
    orchestrator = ScraperOrchestrator()
    results = orchestrator.run_all_scrapers()
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    logger.info(f"Scraping complete. Successful: {successful}, Failed: {failed}")
    
    # Return exit code
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
