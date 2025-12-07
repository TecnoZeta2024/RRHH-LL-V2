"""
Statistical Analyzer for Lottery Data
Implements statistical filtering and pattern analysis
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Performs statistical analysis on lottery data"""
    
    def __init__(self, historical_draws: List[Dict]):
        """
        Initialize with historical lottery draws
        
        Args:
            historical_draws: List of historical draw dictionaries
        """
        self.draws = historical_draws
        self.df = self.prepare_dataframe()
    
    def prepare_dataframe(self) -> pd.DataFrame:
        """Convert draw data to pandas DataFrame for analysis"""
        if not self.draws:
            return pd.DataFrame()
        
        data = []
        for draw in self.draws:
            numbers = draw.get('numbers', [])
            if numbers:
                data.append({
                    'draw_date': draw.get('draw_date'),
                    'numbers': numbers,
                    'sum': sum(numbers),
                    'mean': np.mean(numbers),
                    'std': np.std(numbers),
                    'range': max(numbers) - min(numbers)
                })
        
        return pd.DataFrame(data)
    
    def calculate_frequency_distribution(self) -> Dict[int, int]:
        """
        Calculate frequency distribution of all numbers
        
        Returns:
            Dictionary mapping number to frequency count
        """
        frequency = {}
        
        for draw in self.draws:
            for number in draw.get('numbers', []):
                frequency[number] = frequency.get(number, 0) + 1
        
        return frequency
    
    def identify_hot_and_cold_numbers(self, window: int = 50) -> Tuple[List[int], List[int]]:
        """
        Identify hot (frequently drawn) and cold (rarely drawn) numbers
        
        Args:
            window: Number of recent draws to analyze
            
        Returns:
            Tuple of (hot_numbers, cold_numbers)
        """
        recent_draws = self.draws[-window:] if len(self.draws) > window else self.draws
        frequency = {}
        
        for draw in recent_draws:
            for number in draw.get('numbers', []):
                frequency[number] = frequency.get(number, 0) + 1
        
        # Sort by frequency
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        # Top 20% are hot, bottom 20% are cold
        hot_count = max(1, len(sorted_freq) // 5)
        hot_numbers = [num for num, _ in sorted_freq[:hot_count]]
        cold_numbers = [num for num, _ in sorted_freq[-hot_count:]]
        
        logger.info(f"Hot numbers: {hot_numbers}")
        logger.info(f"Cold numbers: {cold_numbers}")
        
        return hot_numbers, cold_numbers
    
    def calculate_volatility(self) -> float:
        """
        Calculate volatility (standard deviation) of recent draws
        
        Returns:
            Volatility measure
        """
        if self.df.empty:
            return 0.0
        
        # Use last 6 months of data
        recent_df = self.df.tail(180)  # Approximately 6 months
        volatility = recent_df['sum'].std()
        
        logger.info(f"Calculated volatility: {volatility}")
        return volatility
    
    def filter_extreme_combinations(self, combination: List[int]) -> bool:
        """
        Filter out combinations with extremely low probability
        
        Args:
            combination: List of lottery numbers
            
        Returns:
            True if combination passes filter, False otherwise
        """
        # Check for all consecutive numbers
        sorted_combo = sorted(combination)
        is_consecutive = all(sorted_combo[i] + 1 == sorted_combo[i + 1] 
                            for i in range(len(sorted_combo) - 1))
        
        if is_consecutive:
            logger.info(f"Filtered out consecutive combination: {combination}")
            return False
        
        # Check for all even or all odd
        all_even = all(num % 2 == 0 for num in combination)
        all_odd = all(num % 2 == 1 for num in combination)
        
        if all_even or all_odd:
            logger.info(f"Filtered out all-even/odd combination: {combination}")
            return False
        
        # Check for extreme sum values
        combo_sum = sum(combination)
        if not self.df.empty:
            mean_sum = self.df['sum'].mean()
            std_sum = self.df['sum'].std()
            
            # Filter if more than 3 standard deviations from mean
            if abs(combo_sum - mean_sum) > 3 * std_sum:
                logger.info(f"Filtered out extreme sum combination: {combination}")
                return False
        
        return True
    
    def score_combination(self, combination: List[int]) -> float:
        """
        Score a combination based on statistical properties
        
        Args:
            combination: List of lottery numbers
            
        Returns:
            Score between 0 and 100
        """
        if not self.filter_extreme_combinations(combination):
            return 0.0
        
        score = 50.0  # Base score
        
        # Bonus for balanced odd/even
        even_count = sum(1 for num in combination if num % 2 == 0)
        odd_count = len(combination) - even_count
        if 2 <= even_count <= 3:  # Good balance
            score += 10
        
        # Bonus for good distribution across ranges
        ranges = [0] * 5  # Divide into 5 ranges
        max_num = max(combination)
        for num in combination:
            range_idx = min(4, int((num / (max_num + 1)) * 5))
            ranges[range_idx] += 1
        
        # Good if numbers spread across ranges
        if all(r <= 2 for r in ranges):
            score += 15
        
        # Bonus for sum within normal range
        if not self.df.empty:
            combo_sum = sum(combination)
            mean_sum = self.df['sum'].mean()
            std_sum = self.df['sum'].std()
            
            z_score = abs((combo_sum - mean_sum) / std_sum) if std_sum > 0 else 0
            if z_score < 1:  # Within 1 standard deviation
                score += 15
            elif z_score < 2:  # Within 2 standard deviations
                score += 5
        
        return min(100.0, score)
