import random
import numpy as np
import copy
from terminaltables import AsciiTable


class GA:
    label = ['box1', 'box2', 'box3', 'box4', 'box5', 'box6', 'box7', 'box8', 'box9', 'box10', 'box11', 'box12']
    weight = [20, 30, 60, 90, 50, 70, 30, 30, 70, 20, 20, 60]
    value = [6, 5, 8, 7, 6, 9, 4, 5, 4, 9, 2, 1]
    fittest = []
    fittest_value = None
    population = []
    new_population = []
    maximum_weight = 250
    number_of_population = None
    cull = 0.5
    probability = []
    generation_number = 0

    def __init__(self, generation_number, number_of_population):
        self.generation_number = generation_number
        self.number_of_population = number_of_population

    def initial_population(self):
        for i in range(self.number_of_population):
            initial = []
            for ii in range(len(self.weight)):
                initial.append(random.choice([True, False]))
            self.population.append([initial, self.compute_fitness(initial)])

        return self.population

    # compute fitness
    def compute_fitness(self, chromosome):
        total_weight = 0
        total_value = 0
        for i in range(len(chromosome)):
            if chromosome[i]:
                total_weight += self.weight[i]
                total_value += self.value[i]

        if total_weight > self.maximum_weight:
            total_value = -1
            return total_value, total_weight
        else:
            return total_value, total_weight

    def fitness_sort(self):
        for i in range(len(self.population)):
            for j in range(i, len(self.population)):
                if self.population[i][1][0] < self.population[j][1][0]:
                    temp = self.population[i]
                    self.population[i] = self.population[j]
                    self.population[j] = temp

        self.population = self.population[:round(self.number_of_population / 2)]

        return self.population

    def get_fittest(self):
        self.fittest = []
        self.fittest_value = 0

        for i in self.population:
            if i[1][0] > self.fittest_value:
                self.fittest_value = i[1][0]
                self.fittest = i

        return self.fittest, self.fittest_value

    #This a math function for selecting chromosome
    # The probability that an individual will be selected for reproduction is based on its fitness score

    def selected_prob(len):
        f = 1 - 1 / (len * len)
        t0 = 0
        for i in range(len):
            t0 += f ** i
        t1 = 1 / t0
        p = []
        for i in range(0, len):
            p.append(t1 * f ** i)
        rnd = np.random.choice(len, 2, p=p)
        return rnd

    # using crossover and mutation to generate new population
    def generate_new_population(self):
        crossover_list = []

        for i in range(self.number_of_population - 1):
            rnd = GA.selected_prob(len(self.population))
            index1 = rnd[0]
            index2 = rnd[1]

            selected_chromosome1 = self.population[index1]
            selected_chromosome2 = self.population[index2]

            crossover_point = random.randint(0, len(selected_chromosome1[0]))

            new_chromosome1 = selected_chromosome1[0][:crossover_point] + selected_chromosome2[0][crossover_point:]
            new_chromosome2 = selected_chromosome2[0][:crossover_point] + selected_chromosome1[0][crossover_point:]
            crossover_list.append(new_chromosome1)
            crossover_list.append(new_chromosome2)

        # In certain new offspring formed,
        # some of their genes can be subjected to a mutation with a low random probability

        mutation_prob = random.uniform(0, 0.5)

        self.population = []
        for i in crossover_list:
            threshold = random.random()
            if threshold < mutation_prob:
                temp_chromosome = i
                index = len(temp_chromosome) - 1
                mutation_start = random.randint(0, index)
                mutation_end = random.randint(mutation_start, index)
                for j in range(mutation_start, mutation_end):
                    temp_chromosome[j] = not temp_chromosome[j]
                self.population.append([temp_chromosome, self.compute_fitness(temp_chromosome)])
            else:
                self.population.append([i, self.compute_fitness(i)])
        self.population.append(self.fittest)

    def chosen_box(self):
        backpack_list = []
        weight_list = []
        value_list = []

        for i in range(len(self.weight)-1):
            if self.fittest[0][i] == True:
                backpack_list.append(self.label[i])
                weight_list.append(self.weight[i])
                value_list.append(self.value[i])



        answer = [backpack_list, weight_list, value_list]

        table = AsciiTable(answer)
        table.inner_row_border = True
        table.title = "Chosen Boxes"
        print(table.table)
        print("Total value is: ", self.fittest_value)
        print("Total weight is: ", self.fittest[1][1])


    def run(self):

        print("We have a set of boxes below: ")
        data = [
            ["Label", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            ["weight", 20, 30, 60, 90, 50, 70, 30, 30, 70, 20, 20, 60],
            ["Value", 6, 5, 8, 7, 6, 9, 4, 5, 4, 9, 2, 1],
        ]
        table = AsciiTable(data)
        table.inner_row_border = True
        table.title = "Boxes Choice"
        print(table.table)

        print("Let's find out the best choice")
        print("-------Genetic Algorithm-------")

        self.initial_population()
        self.get_fittest()
        for i in range(self.generation_number):
            self.fitness_sort()
            self.generate_new_population()
            self.get_fittest()

        self.fitness_sort()

        self.get_fittest()
        self.chosen_box()


if __name__ == "__main__":
    ga = GA(500, 100)
    ga.run()
