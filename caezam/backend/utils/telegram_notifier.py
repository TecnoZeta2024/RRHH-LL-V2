"""
Telegram Bot Notifier
Sends notifications about scraping and analysis results
"""
import os
import logging
from typing import Optional
from telegram import Bot
from telegram.constants import ParseMode
import asyncio

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles Telegram notifications"""
    
    def __init__(self):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not token or not chat_id:
            logger.warning("Telegram credentials not configured")
            self.bot = None
            self.chat_id = None
        else:
            self.bot = Bot(token=token)
            self.chat_id = chat_id
            logger.info("Telegram notifier initialized")
    
    async def send_message(self, message: str, parse_mode: str = ParseMode.MARKDOWN) -> bool:
        """
        Send a message via Telegram
        
        Args:
            message: Message text (supports Markdown)
            parse_mode: Parse mode for formatting
            
        Returns:
            True if successful, False otherwise
        """
        if not self.bot or not self.chat_id:
            logger.warning("Telegram not configured, skipping notification")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            logger.info("Telegram notification sent successfully")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram message: {str(e)}")
            return False
    
    async def notify_scraping_complete(self, 
                                      successful: int,
                                      failed: int,
                                      lotteries: list) -> bool:
        """
        Send scraping completion notification
        
        Args:
            successful: Number of successful scrapes
            failed: Number of failed scrapes
            lotteries: List of lottery names
            
        Returns:
            True if successful
        """
        message = f"""
🎰 *Caezam Scraping Report*

✅ Successful: {successful}
❌ Failed: {failed}

Lotteries processed:
{chr(10).join(['• ' + name for name in lotteries])}

Check dashboard for details.
"""
        return await self.send_message(message)
    
    async def notify_analysis_complete(self, 
                                     lottery_name: str,
                                     recommendations: list) -> bool:
        """
        Send analysis completion notification with top recommendations
        
        Args:
            lottery_name: Name of the lottery
            recommendations: List of top recommendations
            
        Returns:
            True if successful
        """
        if not recommendations:
            return False
        
        # Format recommendations
        rec_text = []
        for idx, rec in enumerate(recommendations[:3], 1):
            combo = rec.get('combination', [])
            score = rec.get('confidence_score', 0)
            kelly = rec.get('kelly_fraction', 0)
            
            rec_text.append(
                f"{idx}. `{' - '.join(map(str, combo))}`\n"
                f"   Confidence: *{score:.1f}%* | Kelly: *{kelly*100:.2f}%*"
            )
        
        message = f"""
🔮 *{lottery_name} Analysis Complete*

📊 *Top 3 Recommendations:*

{chr(10).join(rec_text)}

💰 View full details at: app.caezam.online
"""
        return await self.send_message(message)
    
    async def notify_manual_input_needed(self, lottery_name: str) -> bool:
        """
        Notify that manual input is needed for a lottery
        
        Args:
            lottery_name: Name of the lottery
            
        Returns:
            True if successful
        """
        message = f"""
⚠️ *Manual Input Required*

Lottery: *{lottery_name}*

OCR extraction failed. Please enter results manually via dashboard.
"""
        return await self.send_message(message)
    
    async def notify_error(self, error_message: str, context: Optional[str] = None) -> bool:
        """
        Send error notification
        
        Args:
            error_message: Error description
            context: Additional context
            
        Returns:
            True if successful
        """
        message = f"""
🚨 *Caezam Error Alert*

Error: {error_message}

{f"Context: {context}" if context else ""}

Check logs for details.
"""
        return await self.send_message(message)


def send_notification_sync(message: str):
    """
    Synchronous wrapper for sending notifications
    Used by GitHub Actions
    
    Args:
        message: Message to send
    """
    notifier = TelegramNotifier()
    asyncio.run(notifier.send_message(message))


# Main function for GitHub Actions
if __name__ == "__main__":
    import sys
    
    # Send a completion notification
    notifier = TelegramNotifier()
    
    message = """
✅ *Caezam Pipeline Complete*

Process finished at 03:00 AM BOT.
3 new signals ready.

Visit *app.caezam.online* to view.
"""
    
    asyncio.run(notifier.send_message(message))
    sys.exit(0)
