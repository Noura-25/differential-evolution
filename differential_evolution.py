import random

######## Parameters #########

N = 100       # population size
F = 0.5       # mutation factor
CR = 0.1      # probability of allele mutation
G = 10000     # number of generations/iterations
eps = 0.01    # tolerated error
bounds = ((0, 1), (5, 10), (0.1, 0.2), (0, 100), (-5, 5))    # upper and lower bounds for each sample parameter

######## Methods ############

def create_first_generation(bounds, population_size=4):
    """ Method creates the first generation. """
    parameters = len(bounds)
    first_generation = [[random.uniform(bounds[y][0], bounds[y][1]) for y in xrange(parameters)] for x in
                        xrange(population_size)]

    return first_generation


def print_data(M):
    """ Prints out the matrix. """
    for m in M:
        print m
    print


def mutation(target, F):
    """ Method creates a mutation on a random sample, based on alleles of two other samples. """
    mixed_samples = range(len(target))
    random.shuffle(mixed_samples)

    donor = target[mixed_samples[0]]

    for i in xrange(len(target[mixed_samples[0]])):
        donor[i] = donor[i] + F * (target[mixed_samples[1]][i] - target[mixed_samples[2]][i])

    return donor


def recombination(target, donor, CR):
    """ Target samples sequence recombination. Target sample gets a donor sequence with	probability CR. """
    trial = [[] for x in xrange(len(target))]

    for i in xrange(len(target)):
        random_seq = random.randint(0, len(target[0]))
        for j in xrange(len(target[0])):
            if random.uniform(0, 1) <= CR or random_seq == j:
                trial[i].append(donor[j])
            else:
                trial[i].append(target[i][j])

    return trial


def selection(target_generation, trial_generation, f):
    """ Survival of the fittest based on a fitness function. """
    next_generation = []

    for sample in xrange(len(trial_generation)):
        if f(target_generation[sample]) <= f(trial_generation[sample]):
            next_generation.append(target_generation[sample])
        else:
            next_generation.append(trial_generation[sample])

    return next_generation


def fitness_function_1(sample):
    """ L_1 distance between a given sample and instance 'top_of_the_food_chain'. """
    top_of_the_food_chain = [0.7, 6, 0.15, 39.5, -2.2]

    score = 0
    for i in xrange(len(sample)):
        score += abs(top_of_the_food_chain[i] - sample[i])

    return score


def god_among_men(next_generation, f):
    """ Method returns a sample that has the best score. """
    best_sample = [9000, 9000, 9000, 9000, 9000]

    for sample in next_generation:
        if f(sample) < f(best_sample):
            best_sample = sample

    return best_sample


if __name__ == "__main__":
    f = fitness_function_1
    target = create_first_generation(bounds, N)    # current generation
    print_data(target)

    while G > 0:
        mutant = mutation(target, F)
        #print_data(mutant)
        trial = recombination(target, mutant, CR)
        #print_data(trial)
        next_generation = selection(target, trial, f)

        best = god_among_men(next_generation, f)      # choose the fittest sample

        if fitness_function_1(best) <= 0.01:
            print '#' * len(str(best))
            print '#', best
            print '#' * len(str(best))
            print 'G', G
            break

        target = next_generation
        G -= 1