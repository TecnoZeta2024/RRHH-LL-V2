"""
Genetic Algorithm for Lottery Combination Optimization
Evolves combinations through selection, crossover, and mutation
"""
import numpy as np
from typing import List, Tuple, Callable
import logging
from deap import base, creator, tools, algorithms

logger = logging.getLogger(__name__)


class GeneticOptimizer:
    """Optimizes lottery combinations using genetic algorithms"""
    
    def __init__(self,
                 num_range: Tuple[int, int],
                 combination_size: int,
                 population_size: int = 100,
                 generations: int = 50):
        """
        Initialize genetic algorithm optimizer
        
        Args:
            num_range: Tuple of (min_num, max_num)
            combination_size: Number of numbers in a combination
            population_size: Size of the population
            generations: Number of generations to evolve
        """
        self.min_num, self.max_num = num_range
        self.combination_size = combination_size
        self.population_size = population_size
        self.generations = generations
        
        # Setup DEAP framework
        self.setup_deap()
    
    def setup_deap(self):
        """Setup DEAP genetic algorithm framework"""
        # Create fitness and individual classes
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMax)
        
        self.toolbox = base.Toolbox()
        
        # Attribute generator: random number in range
        self.toolbox.register("attr_num", 
                             np.random.randint, 
                             self.min_num, 
                             self.max_num + 1)
        
        # Individual generator: combination of unique numbers
        self.toolbox.register("individual", 
                             self.create_individual)
        
        # Population generator
        self.toolbox.register("population", 
                             tools.initRepeat, 
                             list, 
                             self.toolbox.individual)
    
    def create_individual(self) -> creator.Individual:
        """
        Create a valid individual (combination with unique numbers)
        
        Returns:
            Individual with unique lottery numbers
        """
        numbers = np.random.choice(
            range(self.min_num, self.max_num + 1),
            size=self.combination_size,
            replace=False
        )
        return creator.Individual(sorted(numbers.tolist()))
    
    def evaluate_fitness(self, 
                        individual: List[int],
                        fitness_func: Callable) -> Tuple[float,]:
        """
        Evaluate fitness of an individual
        
        Args:
            individual: Lottery combination
            fitness_func: External fitness function
            
        Returns:
            Tuple containing fitness score
        """
        score = fitness_func(individual)
        return (score,)
    
    def mutate(self, individual: List[int]) -> Tuple[List[int],]:
        """
        Mutate an individual by replacing one number
        
        Args:
            individual: Lottery combination
            
        Returns:
            Tuple containing mutated individual
        """
        if np.random.random() < 0.2:  # 20% mutation rate
            # Replace one random number
            idx = np.random.randint(0, len(individual))
            
            # Find a new number not already in the combination
            available = set(range(self.min_num, self.max_num + 1)) - set(individual)
            if available:
                individual[idx] = np.random.choice(list(available))
                individual[:] = sorted(individual)
        
        return (individual,)
    
    def crossover(self, 
                 ind1: List[int], 
                 ind2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform crossover between two individuals
        
        Args:
            ind1: First parent
            ind2: Second parent
            
        Returns:
            Tuple of two offspring
        """
        if np.random.random() < 0.5:  # 50% crossover rate
            # Two-point crossover with repair
            size = len(ind1)
            cx_point1 = np.random.randint(1, size)
            cx_point2 = np.random.randint(cx_point1 + 1, size + 1)
            
            # Create offspring
            offspring1 = ind1[:cx_point1] + ind2[cx_point1:cx_point2] + ind1[cx_point2:]
            offspring2 = ind2[:cx_point1] + ind1[cx_point1:cx_point2] + ind2[cx_point2:]
            
            # Repair duplicates
            offspring1 = self.repair_individual(offspring1)
            offspring2 = self.repair_individual(offspring2)
            
            return offspring1, offspring2
        
        return ind1, ind2
    
    def repair_individual(self, individual: List[int]) -> List[int]:
        """
        Repair individual by removing duplicates and maintaining size
        
        Args:
            individual: Potentially invalid combination
            
        Returns:
            Valid combination
        """
        # Remove duplicates
        unique_nums = list(set(individual))
        
        # If too few numbers, add random ones
        while len(unique_nums) < self.combination_size:
            available = set(range(self.min_num, self.max_num + 1)) - set(unique_nums)
            if available:
                unique_nums.append(np.random.choice(list(available)))
        
        # If too many, trim
        unique_nums = unique_nums[:self.combination_size]
        
        return sorted(unique_nums)
    
    def optimize(self, fitness_func: Callable) -> List[Dict]:
        """
        Run genetic algorithm optimization
        
        Args:
            fitness_func: Function to evaluate combination quality
            
        Returns:
            List of top combinations with their fitness scores
        """
        # Register genetic operators
        self.toolbox.register("evaluate", self.evaluate_fitness, fitness_func=fitness_func)
        self.toolbox.register("mate", self.crossover)
        self.toolbox.register("mutate", self.mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
        # Create initial population
        population = self.toolbox.population(n=self.population_size)
        
        # Statistics
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("max", np.max)
        
        logger.info(f"Starting genetic algorithm: {self.generations} generations, "
                   f"{self.population_size} population")
        
        # Run evolution
        population, logbook = algorithms.eaSimple(
            population, 
            self.toolbox,
            cxpb=0.5,  # Crossover probability
            mutpb=0.2,  # Mutation probability
            ngen=self.generations,
            stats=stats,
            verbose=False
        )
        
        # Get top individuals
        top_individuals = tools.selBest(population, k=10)
        
        results = []
        for ind in top_individuals:
            results.append({
                'combination': list(ind),
                'fitness_score': ind.fitness.values[0]
            })
        
        logger.info(f"Genetic algorithm complete. Top combination: {results[0]['combination']} "
                   f"(fitness: {results[0]['fitness_score']:.2f})")
        
        return results
