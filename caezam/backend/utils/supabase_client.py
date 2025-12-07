"""
Supabase Client Wrapper
Handles all database operations
"""
import os
from typing import List, Dict, Optional
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Wrapper for Supabase database operations"""
    
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        
        self.client: Client = create_client(url, key)
        logger.info("Supabase client initialized")
    
    def insert_draw(self, draw_data: Dict) -> Dict:
        """
        Insert a lottery draw into the database
        
        Args:
            draw_data: Draw data dictionary
            
        Returns:
            Inserted record
        """
        try:
            response = self.client.table('draws').insert(draw_data).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error inserting draw: {str(e)}")
            raise
    
    def get_draws(self, lottery_name: str, limit: int = 500) -> List[Dict]:
        """
        Get historical draws for a lottery
        
        Args:
            lottery_name: Name of the lottery
            limit: Maximum number of draws to fetch
            
        Returns:
            List of draw records
        """
        try:
            response = self.client.table('draws')\
                .select('*')\
                .eq('lottery_name', lottery_name)\
                .order('draw_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error fetching draws: {str(e)}")
            return []
    
    def insert_recommendation(self, recommendation: Dict) -> Dict:
        """
        Insert a recommendation into the database
        
        Args:
            recommendation: Recommendation data
            
        Returns:
            Inserted record
        """
        try:
            response = self.client.table('recommendations').insert(recommendation).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error inserting recommendation: {str(e)}")
            raise
    
    def get_latest_recommendations(self, lottery_name: str, limit: int = 3) -> List[Dict]:
        """
        Get latest recommendations for a lottery
        
        Args:
            lottery_name: Name of the lottery
            limit: Maximum number of recommendations
            
        Returns:
            List of recommendation records
        """
        try:
            response = self.client.table('recommendations')\
                .select('*')\
                .eq('lottery_name', lottery_name)\
                .order('analysis_date', desc=True)\
                .limit(limit)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error fetching recommendations: {str(e)}")
            return []
    
    def flag_manual_input(self, flag_data: Dict) -> Dict:
        """
        Flag that a lottery needs manual input
        
        Args:
            flag_data: Flag information
            
        Returns:
            Inserted record
        """
        try:
            response = self.client.table('manual_input_flags').insert(flag_data).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error flagging manual input: {str(e)}")
            raise
    
    def get_bankroll(self) -> Optional[Dict]:
        """
        Get current bankroll information
        
        Returns:
            Bankroll record or None
        """
        try:
            response = self.client.table('bankroll')\
                .select('*')\
                .order('updated_at', desc=True)\
                .limit(1)\
                .execute()
            
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error fetching bankroll: {str(e)}")
            return None
    
    def update_bankroll(self, bankroll_data: Dict) -> Dict:
        """
        Update bankroll information
        
        Args:
            bankroll_data: Bankroll update data
            
        Returns:
            Updated record
        """
        try:
            current = self.get_bankroll()
            
            if current:
                response = self.client.table('bankroll')\
                    .update(bankroll_data)\
                    .eq('id', current['id'])\
                    .execute()
            else:
                response = self.client.table('bankroll').insert(bankroll_data).execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error updating bankroll: {str(e)}")
            raise
