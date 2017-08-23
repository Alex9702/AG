
# An "Individual" represents a single candidate solution. The core piece of
# information about an individual is its "chromosome", which is an encoding of
# a possible solution to the problem at hand. A chromosome can be a string, an
# array, a list, etc -- in this class, the chromosome is an integer array. 
# 
# An individual position in the chromosome is called a gene, and these are the
# atomic pieces of the solution that can be manipulated or mutated. When the
# chromosome is a string, as in this case, each character or set of characters
# can be a gene.
# 
# An individual also has a "fitness" score; this is a number that represents
# how good a solution to the problem this individual is. The meaning of the
# fitness score will vary based on the problem at hand.

import random

class Individual:
	# This constructor assumes that the chromosome is made entirely of 0s and
	# 1s, which may not always be the case, so make sure to modify as
	# necessary. This constructor also assumes that a "random" chromosome means
	# simply picking random zeroes and ones, which also may not be the case
	# (for instance, in a traveling salesman problem, this would be an invalid
	# solution).
	def __init__(self, chromosomeLength):
		self.chromosome = []
		self.chromosomeLength = chromosomeLength
		self.fitness = -1

		for i in range(self.chromosomeLength):
			if random.random() > 0.5:
				self.chromosome.append('1')
			else:
				self.chromosome.append('0')

	def getChromosome(self):
		return self.chromosome

	def getChromosomeLength(self):
		return self.chromosomeLength

	def getGene(self, offset):
		return self.chromosome[offset]

	def setGene(self, offset, gene):
		self.chromosome[offset] = str(gene)

	def getFitness(self):
		return self.fitness

	def setFitness(self, fitness):
		self.fitness = fitness

	def getInt(self):
		pass
	def toString(self):
		output = ''
		for i in self.chromosome:
			output += i
		return output