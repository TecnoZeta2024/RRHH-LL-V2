"""
Main Analysis Orchestrator
Coordinates statistical analysis, Monte Carlo simulation, and genetic optimization
"""
import os
import sys
import logging
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzers.statistical_analyzer import StatisticalAnalyzer
from analyzers.monte_carlo import MonteCarloSimulator
from analyzers.genetic_optimizer import GeneticOptimizer
from utils.supabase_client import SupabaseClient
from utils.kelly_criterion import KellyCriterion

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    """Orchestrates all analysis modules"""
    
    def __init__(self):
        self.supabase = SupabaseClient()
        self.monte_carlo = MonteCarloSimulator(num_simulations=100000)
    
    def analyze_lottery(self, lottery_name: str) -> List[Dict]:
        """
        Run complete analysis for a specific lottery
        
        Args:
            lottery_name: Name of the lottery to analyze
            
        Returns:
            List of top 3 recommended combinations
        """
        logger.info(f"Starting analysis for {lottery_name}")
        
        # Fetch historical data
        historical_draws = self.supabase.get_draws(lottery_name, limit=500)
        
        if not historical_draws or len(historical_draws) < 50:
            logger.warning(f"Insufficient historical data for {lottery_name}")
            return []
        
        # Step 1: Statistical Analysis
        stat_analyzer = StatisticalAnalyzer(historical_draws)
        volatility = stat_analyzer.calculate_volatility()
        hot_numbers, cold_numbers = stat_analyzer.identify_hot_and_cold_numbers()
        
        # Step 2: Determine number range and combination size
        num_range, combo_size = self.determine_lottery_params(historical_draws)
        
        # Step 3: Genetic Algorithm Optimization
        def fitness_function(combination):
            return stat_analyzer.score_combination(combination)
        
        genetic_optimizer = GeneticOptimizer(
            num_range=num_range,
            combination_size=combo_size,
            population_size=100,
            generations=50
        )
        
        genetic_results = genetic_optimizer.optimize(fitness_function)
        
        # Get top 10 combinations from genetic algorithm
        top_combinations = [r['combination'] for r in genetic_results[:10]]
        
        # Step 4: Monte Carlo Validation
        mc_results = self.monte_carlo.rank_combinations(
            combinations=top_combinations,
            num_range=num_range,
            volatility=volatility
        )
        
        # Step 5: Combined Scoring
        final_recommendations = self.combine_scores(genetic_results, mc_results)
        
        # Get top 3
        top_3 = final_recommendations[:3]
        
        # Step 6: Calculate Kelly Criterion bet sizing
        kelly = KellyCriterion()
        for rec in top_3:
            edge = rec['confidence_score'] / 100.0
            win_prob = rec['monte_carlo']['match_3_probability']
            rec['kelly_fraction'] = kelly.calculate_fraction(win_prob, edge)
        
        # Save recommendations to database
        self.save_recommendations(lottery_name, top_3)
        
        logger.info(f"Analysis complete for {lottery_name}. Top 3 combinations generated.")
        return top_3
    
    def determine_lottery_params(self, draws: List[Dict]) -> tuple:
        """
        Determine lottery parameters from historical data
        
        Args:
            draws: List of historical draws
            
        Returns:
            Tuple of (num_range, combination_size)
        """
        all_numbers = []
        combo_sizes = []
        
        for draw in draws:
            numbers = draw.get('numbers', [])
            if numbers:
                all_numbers.extend(numbers)
                combo_sizes.append(len(numbers))
        
        if all_numbers:
            min_num = min(all_numbers)
            max_num = max(all_numbers)
            avg_size = int(sum(combo_sizes) / len(combo_sizes))
        else:
            # Defaults
            min_num, max_num = 1, 69
            avg_size = 5
        
        return (min_num, max_num), avg_size
    
    def combine_scores(self, 
                      genetic_results: List[Dict],
                      mc_results: List[Dict]) -> List[Dict]:
        """
        Combine genetic algorithm and Monte Carlo scores
        
        Args:
            genetic_results: Results from genetic optimization
            mc_results: Results from Monte Carlo simulation
            
        Returns:
            Combined and ranked results
        """
        combined = []
        
        # Create lookup for Monte Carlo results
        mc_lookup = {str(r['combination']): r for r in mc_results}
        
        for genetic_result in genetic_results:
            combo_key = str(genetic_result['combination'])
            
            if combo_key in mc_lookup:
                mc_result = mc_lookup[combo_key]
                
                # Weighted combination: 40% genetic, 60% Monte Carlo
                genetic_score = genetic_result['fitness_score']
                mc_score = mc_result['overall_score']
                
                confidence_score = (genetic_score * 0.4) + (mc_score * 0.6)
                
                combined.append({
                    'combination': genetic_result['combination'],
                    'confidence_score': confidence_score,
                    'genetic_score': genetic_score,
                    'monte_carlo_score': mc_score,
                    'monte_carlo': mc_result['performance']
                })
        
        # Sort by confidence score
        combined.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return combined
    
    def save_recommendations(self, lottery_name: str, recommendations: List[Dict]):
        """
        Save recommendations to database
        
        Args:
            lottery_name: Name of the lottery
            recommendations: List of recommended combinations
        """
        try:
            for idx, rec in enumerate(recommendations):
                record = {
                    'lottery_name': lottery_name,
                    'rank': idx + 1,
                    'combination': rec['combination'],
                    'confidence_score': rec['confidence_score'],
                    'genetic_score': rec['genetic_score'],
                    'monte_carlo_score': rec['monte_carlo_score'],
                    'kelly_fraction': rec.get('kelly_fraction', 0.0),
                    'analysis_date': datetime.utcnow().isoformat()
                }
                
                self.supabase.insert_recommendation(record)
            
            logger.info(f"Saved {len(recommendations)} recommendations for {lottery_name}")
        
        except Exception as e:
            logger.error(f"Error saving recommendations: {str(e)}")


def main():
    """Main execution function"""
    logger.info("Starting Caezam Analysis Pipeline")
    
    orchestrator = AnalysisOrchestrator()
    
    # Analyze all active lotteries
    lotteries = ['Powerball', 'Lonabol']  # Add more as scrapers are added
    
    for lottery in lotteries:
        try:
            recommendations = orchestrator.analyze_lottery(lottery)
            logger.info(f"Generated {len(recommendations)} recommendations for {lottery}")
        except Exception as e:
            logger.error(f"Error analyzing {lottery}: {str(e)}")
    
    logger.info("Analysis pipeline complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
