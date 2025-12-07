"""
Bolivia Lottery (Lonabol) Scraper with OCR Support
Handles both text and image-based data extraction
"""
from typing import Dict, List, Optional
import logging
from io import BytesIO
from PIL import Image
import pytesseract
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class LonabolScraper(BaseScraper):
    """Scraper for Bolivia National Lottery (Lonabol)"""
    
    def __init__(self):
        super().__init__(
            lottery_name="Lonabol",
            base_url="https://www.lonabol.com.bo/resultados"
        )
        self.needs_manual_input = False
    
    def extract_text_from_image(self, image_bytes: bytes) -> Optional[str]:
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image_bytes: Image data in bytes
            
        Returns:
            Extracted text or None if failed
        """
        try:
            image = Image.open(BytesIO(image_bytes))
            # Configure Tesseract for Spanish and numbers
            text = pytesseract.image_to_string(
                image,
                lang='spa',
                config='--psm 6 -c tessedit_char_whitelist=0123456789 '
            )
            return text.strip()
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return None
    
    def parse_numbers_from_text(self, text: str) -> List[int]:
        """
        Parse lottery numbers from extracted text
        
        Args:
            text: Extracted text containing numbers
            
        Returns:
            List of lottery numbers
        """
        numbers = []
        # Extract all numbers from text
        import re
        found_numbers = re.findall(r'\d+', text)
        
        for num_str in found_numbers:
            try:
                num = int(num_str)
                if 1 <= num <= 99:  # Typical range for Bolivia lottery
                    numbers.append(num)
            except ValueError:
                continue
        
        return numbers[:5]  # Return first 5 valid numbers
    
    def scrape_latest_draw(self) -> Optional[Dict]:
        """Scrape the latest Lonabol draw"""
        try:
            self.page.goto(self.base_url, wait_until='domcontentloaded', timeout=30000)
            
            # Try text-based extraction first
            try:
                # Look for text-based results
                result_container = self.page.wait_for_selector('.resultado-container', timeout=5000)
                
                if result_container:
                    # Extract date
                    date_elem = self.page.query_selector('.fecha-sorteo')
                    draw_date = date_elem.inner_text() if date_elem else None
                    
                    # Extract numbers
                    number_elements = self.page.query_selector_all('.numero-sorteo')
                    numbers = [int(elem.inner_text()) for elem in number_elements]
                    
                    result = {
                        'draw_date': draw_date,
                        'numbers': numbers,
                        'bonus_numbers': [],
                        'lottery_type': 'lonabol',
                        'extraction_method': 'text'
                    }
                    
                    logger.info(f"Lonabol scraped successfully (text): {result}")
                    return result
            
            except Exception as text_error:
                logger.warning(f"Text extraction failed, trying OCR: {str(text_error)}")
                
                # Try OCR extraction on images
                try:
                    # Look for result images
                    image_elem = self.page.query_selector('.resultado-imagen img')
                    
                    if image_elem:
                        image_url = image_elem.get_attribute('src')
                        
                        # Download image
                        response = self.page.request.get(image_url)
                        image_bytes = response.body()
                        
                        # Extract text with OCR
                        extracted_text = self.extract_text_from_image(image_bytes)
                        
                        if extracted_text:
                            numbers = self.parse_numbers_from_text(extracted_text)
                            
                            if len(numbers) >= 3:  # Minimum valid result
                                result = {
                                    'draw_date': None,  # Cannot extract from image
                                    'numbers': numbers,
                                    'bonus_numbers': [],
                                    'lottery_type': 'lonabol',
                                    'extraction_method': 'ocr'
                                }
                                
                                logger.info(f"Lonabol scraped with OCR: {result}")
                                return result
                        
                        # OCR failed, mark for manual input
                        self.needs_manual_input = True
                        logger.error("OCR extraction insufficient, manual input required")
                        return None
                
                except Exception as ocr_error:
                    logger.error(f"OCR extraction failed: {str(ocr_error)}")
                    self.needs_manual_input = True
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error scraping Lonabol: {str(e)}")
            self.needs_manual_input = True
            return None
    
    def scrape_historical_data(self, limit: int = 100) -> List[Dict]:
        """Scrape historical Lonabol draws"""
        # For MVP, historical data for Lonabol can be manually imported
        logger.info("Historical data for Lonabol requires manual import")
        return []
