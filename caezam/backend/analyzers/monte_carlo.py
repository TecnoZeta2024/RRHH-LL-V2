"""
Monte Carlo Simulation Engine
Simulates thousands of lottery draws to test combination resilience
"""
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class MonteCarloSimulator:
    """Performs Monte Carlo simulations on lottery combinations"""
    
    def __init__(self, num_simulations: int = 100000):
        """
        Initialize Monte Carlo simulator
        
        Args:
            num_simulations: Number of simulations to run
        """
        self.num_simulations = num_simulations
    
    def simulate_draws(self, 
                      num_range: tuple, 
                      draw_size: int,
                      volatility: float = 1.0) -> np.ndarray:
        """
        Simulate lottery draws based on historical volatility
        
        Args:
            num_range: Tuple of (min_num, max_num)
            draw_size: Number of numbers per draw
            volatility: Volatility factor from historical data
            
        Returns:
            Array of simulated draws
        """
        min_num, max_num = num_range
        draws = []
        
        # Base probability distribution (uniform with volatility adjustment)
        base_probs = np.ones(max_num - min_num + 1)
        
        # Add volatility-based perturbation
        if volatility > 0:
            noise = np.random.normal(0, volatility * 0.01, len(base_probs))
            base_probs = base_probs + noise
            base_probs = np.maximum(base_probs, 0.01)  # Ensure all positive
        
        # Normalize to probabilities
        base_probs = base_probs / base_probs.sum()
        
        for _ in range(self.num_simulations):
            # Draw without replacement
            draw = np.random.choice(
                range(min_num, max_num + 1),
                size=draw_size,
                replace=False,
                p=base_probs
            )
            draws.append(sorted(draw))
        
        return np.array(draws)
    
    def test_combination_performance(self,
                                    combination: List[int],
                                    simulated_draws: np.ndarray) -> Dict[str, float]:
        """
        Test how a combination performs against simulated draws
        
        Args:
            combination: The lottery combination to test
            simulated_draws: Array of simulated draws
            
        Returns:
            Dictionary with performance metrics
        """
        combination_set = set(combination)
        match_counts = []
        
        for draw in simulated_draws:
            matches = len(combination_set.intersection(set(draw)))
            match_counts.append(matches)
        
        match_array = np.array(match_counts)
        
        # Calculate statistics
        metrics = {
            'avg_matches': float(np.mean(match_array)),
            'max_matches': int(np.max(match_array)),
            'min_matches': int(np.min(match_array)),
            'std_matches': float(np.std(match_array)),
            'match_3_probability': float(np.sum(match_array >= 3) / len(match_array)),
            'match_4_probability': float(np.sum(match_array >= 4) / len(match_array)),
            'match_5_probability': float(np.sum(match_array >= 5) / len(match_array)),
            'resilience_score': self.calculate_resilience_score(match_array)
        }
        
        logger.info(f"Combination {combination} performance: {metrics}")
        return metrics
    
    def calculate_resilience_score(self, match_array: np.ndarray) -> float:
        """
        Calculate a resilience score based on match distribution
        Higher score means more consistent performance
        
        Args:
            match_array: Array of match counts
            
        Returns:
            Resilience score (0-100)
        """
        # Base score from average matches
        avg_matches = np.mean(match_array)
        base_score = (avg_matches / len(match_array[0])) * 50
        
        # Bonus for consistency (lower standard deviation is better)
        std_matches = np.std(match_array)
        consistency_bonus = max(0, 25 - std_matches * 5)
        
        # Bonus for higher match probability
        high_match_prob = np.sum(match_array >= 3) / len(match_array)
        probability_bonus = high_match_prob * 25
        
        total_score = base_score + consistency_bonus + probability_bonus
        return min(100.0, total_score)
    
    def rank_combinations(self,
                         combinations: List[List[int]],
                         num_range: tuple,
                         volatility: float = 1.0) -> List[Dict]:
        """
        Rank multiple combinations based on Monte Carlo simulation
        
        Args:
            combinations: List of lottery combinations
            num_range: Tuple of (min_num, max_num)
            volatility: Volatility factor
            
        Returns:
            List of ranked combination results
        """
        logger.info(f"Running Monte Carlo with {self.num_simulations} simulations")
        
        # Generate simulated draws
        draw_size = len(combinations[0]) if combinations else 5
        simulated_draws = self.simulate_draws(num_range, draw_size, volatility)
        
        # Test each combination
        results = []
        for combo in combinations:
            performance = self.test_combination_performance(combo, simulated_draws)
            results.append({
                'combination': combo,
                'performance': performance,
                'overall_score': performance['resilience_score']
            })
        
        # Sort by overall score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        logger.info(f"Top combination: {results[0]['combination']} "
                   f"(score: {results[0]['overall_score']:.2f})")
        
        return results
