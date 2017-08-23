# A population is an abstraction of a collection of individuals. The population
# class is generally used to perform group-level operations on its individuals,
# such as finding the strongest individuals, collecting stats on the population
# as a whole, and selecting individuals to mutate or crossover.

import random
import individual

class Population:
	def __init__(self, populationSize, chromosomeLength=0):
		self.population = [individual.Individual(chromosomeLength) for i in range(populationSize)]
		self.populationFitness =-1

	def getIndividuals(self):
		return self.population

	# Find an individual in the population by its fitness
	# 
	# This method lets you select an individual in order of its fitness. This
	# can be used to find the single strongest individual (eg, if you're
	# testing for a solution), but it can also be used to find weak individuals
	# (if you're looking to cull the population) or some of the strongest
	# individuals (if you're using "elitism").

	def getFittest(self, offset):
		# Order population by fitness I used insertion sort
		for j in range(1, len(self.population)):
			k = self.population[j]
			i = j - 1
			while i > -1 and self.population[i].getFitness() < k.getFitness():
				self.population[i + 1] = self.population[i]
				i = i - 1
			self.population[i + 1] = k
		return self.population[offset]

	def setPopulationFitness(self, fitness):
		self.populationFitness = fitness

	def getPopulationFitness(self):
		return self.populationFitness

	def size(self):
		return len(self.population)

	def setIndividual(self, offset, ind):
		self.population[offset] = ind

	def getIndividual(self, offset):
		return self.population[offset]

	def shuffle(self):
		for i in range(len(self.population) - 1,-1,-1):
			index = random.randint(0, i)
			self.population[index], self.population[i] = \
			self.population[i], self.population[index]

