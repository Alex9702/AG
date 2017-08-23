# The GeneticAlgorithm class is our main abstraction for managing the
# operations of the genetic algorithm. This class is meant to be
# problem-specific, meaning that (for instance) the "calcFitness" method may
# need to change from problem to problem.
# 
# This class concerns itself mostly with population-level operations, but also
# problem-specific operations such as calculating fitness, testing for
# termination criteria, and managing mutation and crossover operations (which
# generally need to be problem-specific as well).
# 
# Generally, GeneticAlgorithm might be better suited as an abstract class or an
# interface, rather than a concrete class as below. A GeneticAlgorithm
# interface would require implementation of methods such as
# "isTerminationConditionMet", "calcFitness", "mutatePopulation", etc, and a
# concrete class would be defined to solve a particular problem domain. For
# instance, the concrete class "TravelingSalesmanGeneticAlgorithm" would
# implement the "GeneticAlgorithm" interface. This is not the approach we've
# chosen, however, so that we can keep each chapter's examples as simple and
# concrete as possible.

import population
import individual
import random

class GA:
	def __init__(self, populationSize, mutationRate, crossoverRate, elitismCount):
		self.populationSize = populationSize
		
		# Mutation rate is the fractional probability than an individual gene will
		# mutate randomly in a given generation. The range is 0.0-1.0, but is
		# generally small (on the order of 0.1 or less).
		self.mutationRate = mutationRate

		# Crossover rate is the fractional probability that two individuals will
		# "mate" with each other, sharing genetic information, and creating
		# offspring with traits of each of the parents. Like mutation rate the
		# rance is 0.0-1.0 but small.
		self.crossoverRate = crossoverRate

		# Elitism is the concept that the strongest members of the population
		# should be preserved from generation to generation. If an individual is
		# one of the elite, it will not be mutated or crossover.
		self.elitismCount = elitismCount

	def initPopulation(self, chromosomeLength):
		return population.Population(self.populationSize, chromosomeLength)


	# In this case, the fitness score is very simple: it's the number of ones
	# in the chromosome. Don't forget that this method, and this whole
	# GeneticAlgorithm class, is meant to solve the problem in the "GA"
	# class and example. For different problems, you'll need to create a
	# different version of this method to appropriately calculate the fitness
	# of an individual.
	def calcFitness(self, indi):
		# Track number of correct fitness
		correctGene = 0

		# loop individual's genes
		for gene in indi.getChromosome():
			if gene == '1':
				correctGene += 1
		# calculate fitness

		if correctGene == 0: return 0
		fitness = correctGene/indi.getChromosomeLength()
		
		#store fitness
		indi.setFitness(fitness)
		return fitness

	# Evaluate the whole population
	# 
	# Essentially, loop over the individuals in the population, calculate the
	# fitness for each, and then calculate the entire population's fitness. The
	# population's fitness may or may not be important, but what is important
	# here is making sure that each individual gets evaluated.
	def evalPopulation(self, pop):
		popFitness = 0
		
		# Loop over population evaluating individuals and suming population
		# fitness
		for i in pop.getIndividuals():
			popFitness += self.calcFitness(i)
		pop.setPopulationFitness(popFitness)

	# Check if population has met termination condition
	# 
	# For this simple problem, we know what a perfect solution looks like, so
	# we can simply stop evolving once we've reached a fitness of one.
	def isTerminationConditionMet(self, pop):
		for i in pop.getIndividuals():
			if i.getFitness() == 1:
				return True

		return False

	def selectParent(self, pop):
		# Get individuals
		individuals = pop.getIndividuals()

		# Spin roulette wheel
		popFitness = pop.getPopulationFitness()
		roulleteWheelPosition = random.random() # popFitness

		# Find parent
		spinWheel = 0
		for i in individuals:
			spinWheel += i.getFitness()
			if spinWheel > roulleteWheelPosition:
				return i
		return individuals[pop.size() - 1]

	# Apply crossover to population
	# 
	# Crossover, more colloquially considered "mating", takes the population
	# and blends individuals to create new offspring. It is hoped that when two
	# individuals crossover that their offspring will have the strongest
	# qualities of each of the parents. Of course, it's possible that an
	# offspring will end up with the weakest qualities of each parent.
	# 
	# This method considers both the GeneticAlgorithm instance's crossoverRate
	# and the elitismCount.
	# 
	# The type of crossover we perform depends on the problem domain. We don't
	# want to create invalid solutions with crossover, so this method will need
	# to be changed for different types of problems.
	# 
	# This particular crossover method selects random genes from each parent.
	def crossoverPopulation(self, pop):
		# Create new population
		newpop = population.Population(pop.size())

		# Loop over current population by fitness
		for popIndex in range(pop.size()):
			parent1 = pop.getFittest(popIndex)
			# Apply crossover to this individual?
			if self.crossoverRate > random.random():# and popIndex >= self.elitismCount:
				# Initialize offspring
				offspring = individual.Individual(parent1.getChromosomeLength())

				# Find second parent
				parent2 = self.selectParent(pop)

				# Loop over genome
				for geneIndex in range(parent1.getChromosomeLength()):
					# Use half of parent1's genes and half of parent2's genes
					if 0.5 > random.random():
						offspring.setGene(geneIndex, parent1.getGene(geneIndex))
					else:
						offspring.setGene(geneIndex, parent2.getGene(geneIndex))
				# Add offspring to new population
				newpop.setIndividual(popIndex, offspring)
			
			else:
				# Add individual to new population without applying crossover
				newpop.setIndividual(popIndex, parent1)

		return newpop



	
	 # Apply mutation to population
	 # 
	 # Mutation affects individuals rather than the population. We look at each
	 # individual in the population, and if they're lucky enough (or unlucky, as
	 # it were), apply some randomness to their chromosome. Like crossover, the
	 # type of mutation applied depends on the specific problem we're solving.
	 # In this case, we simply randomly flip 0s to 1s and vice versa.
	 # 
	 # This method will consider the GeneticAlgorithm instance's mutationRate
	 # and elitismCount
	def mutatePopulation(self, pop):
		# Initialize new population
		newpop = population.Population(self.populationSize)

		# Loop over current population by fitness
		for popIndex in range(self.populationSize):
			indi = pop.getFittest(popIndex)

			# Loop over individual's genes
			for geneIndex in range(indi.getChromosomeLength()):
				# Skip mutation if this is an elite individual
				if popIndex > self.elitismCount:
					# Does this gene need mutation?
					if self.mutationRate > random.random():
						# Get new gene
						newGene = 1
						if indi.getGene(geneIndex) == 1:
							newgne = 0

						# Mutate gene
						indi.setGene(geneIndex, newGene)

			# Add individual to population
			newpop.setIndividual(popIndex, indi)

		# Return mutated population
		return newpop

