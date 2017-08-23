import ga
import population

# Create GA object
g = ga.GA(100, 0.001,0.95,2)
# Initialize population
p = g.initPopulation(50)

# Evaluate population
g.evalPopulation(p)

# Keep track of current generation
generation = 1


# Start the evolution loop
# 
# Every genetic algorithm problem has different criteria for finishing.
# In this case, we know what a perfect solution looks like (we don't
# always!), so our isTerminationConditionMet method is very
# straightforward: if there's a member of the population whose
# chromosome is all ones, we're done!

while g.isTerminationConditionMet(p) == False:
	# Print fittest individual from population
	print('Best solution: {}'.format(p.getFittest(0).toString()))

	#Apply crossover
	p = g.crossoverPopulation(p)

	# Apply mutation
	p = g.mutatePopulation(p)

	# Evaluate population
	g.evalPopulation(p)


	# Increment the current generation
	generation += 1


print('Found solution in {} generations'.format(generation))
print('Best solution: {}'.format(p.getFittest(0).toString()))

# We're out of the loop now, which means we have a perfect solution on
# our hands. Let's print it out to confirm that it is actually all
# ones, as promised.