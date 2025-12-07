"""
Kelly Criterion Calculator
Calculates optimal bet sizing based on edge and probability
"""
import logging

logger = logging.getLogger(__name__)


class KellyCriterion:
    """Implements Kelly Criterion for money management"""
    
    def __init__(self, fraction: float = 0.25):
        """
        Initialize Kelly Criterion calculator
        
        Args:
            fraction: Fractional Kelly (0.25 = Quarter Kelly, conservative)
        """
        self.fraction = fraction
    
    def calculate_fraction(self, 
                          win_probability: float,
                          edge: float,
                          odds: float = 2.0) -> float:
        """
        Calculate Kelly fraction for bet sizing
        
        Args:
            win_probability: Probability of winning (0-1)
            edge: Statistical edge/advantage (0-1)
            odds: Payout odds (default 2.0 = even money)
            
        Returns:
            Recommended fraction of bankroll to bet
        """
        if win_probability <= 0 or win_probability >= 1:
            logger.warning(f"Invalid win probability: {win_probability}")
            return 0.0
        
        if edge <= 0:
            logger.warning(f"No positive edge: {edge}")
            return 0.0
        
        # Kelly formula: f = (bp - q) / b
        # where:
        #   f = fraction of bankroll to bet
        #   b = odds received (b to 1)
        #   p = probability of winning
        #   q = probability of losing (1 - p)
        
        b = odds - 1
        p = win_probability
        q = 1 - p
        
        kelly_fraction = ((b * p) - q) / b
        
        # Apply fractional Kelly (more conservative)
        adjusted_fraction = kelly_fraction * self.fraction
        
        # Ensure non-negative and cap at maximum
        adjusted_fraction = max(0.0, min(adjusted_fraction, 0.05))  # Cap at 5%
        
        logger.info(f"Kelly Criterion: win_prob={p:.3f}, edge={edge:.3f}, "
                   f"kelly={kelly_fraction:.3f}, adjusted={adjusted_fraction:.3f}")
        
        return adjusted_fraction
    
    def calculate_bet_amount(self,
                            bankroll: float,
                            win_probability: float,
                            edge: float,
                            odds: float = 2.0) -> float:
        """
        Calculate recommended bet amount
        
        Args:
            bankroll: Current bankroll
            win_probability: Probability of winning
            edge: Statistical edge
            odds: Payout odds
            
        Returns:
            Recommended bet amount in currency
        """
        fraction = self.calculate_fraction(win_probability, edge, odds)
        bet_amount = bankroll * fraction
        
        logger.info(f"Recommended bet: ${bet_amount:.2f} "
                   f"({fraction * 100:.2f}% of ${bankroll:.2f})")
        
        return bet_amount
    
    def calculate_edge(self, 
                      confidence_score: float,
                      base_probability: float = 0.0000001) -> float:
        """
        Estimate edge from confidence score
        
        Args:
            confidence_score: Confidence score (0-100)
            base_probability: Base winning probability for lottery
            
        Returns:
            Estimated edge
        """
        # Convert confidence to edge multiplier
        # Higher confidence = higher perceived edge
        edge_multiplier = 1 + (confidence_score / 100)
        edge = base_probability * edge_multiplier
        
        return min(edge, 0.1)  # Cap at 10% edge


# Example usage for documentation
if __name__ == "__main__":
    kelly = KellyCriterion(fraction=0.25)
    
    # Example: 60% confidence score, $10,000 bankroll
    bankroll = 10000
    confidence = 60
    win_prob = 0.01  # 1% chance (lottery)
    edge = kelly.calculate_edge(confidence)
    
    bet = kelly.calculate_bet_amount(bankroll, win_prob, edge)
    print(f"With {confidence}% confidence and ${bankroll} bankroll:")
    print(f"Recommended bet: ${bet:.2f}")
