# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 09:39:02 2023

@author: sathv
"""

import numpy as np
import networkx as nx
import statistics
from collections import Counter
import matplotlib.pyplot as plt
import math
import seaborn as sns

class Threshold_Response:
    def __init__(self, locations, agents, neighbours, sd, iterations, thresh_fun, intercept, connectivity):
        self.number_of_locations = locations
        self.options = []
        self.sd = sd
        self.number_of_agents = agents
        self.number_of_neighbours = neighbours
        self.threshold_function = thresh_fun
        self.intercept = intercept
        self.connectivity = connectivity
        self.number_of_iterations = iterations
        self.iterations = 0
        self.initial_choices = dict()
        self.new_choices = dict()
        self.updated_qualities = dict()
        self.converged = False
        self.best_option = None
        self.second_option = None
        self.best_quality_agents = []
        self.best_quality_overall = []
        self.best_quality_array = np.empty((0, self.number_of_iterations))
        self.next_quality = []
        self.next_quality_overall = []
        self.next_quality_array = np.empty((0, self.number_of_iterations))
        self.normalised_avg_values = []
        self.average_qualities = []
        self.average_qualities_overall = []
        self.average_qualities_array = np.empty((0, self.number_of_iterations))
        self.second_best = None
        self.third_best = None
        self.fourth_best = None
        self.fifth_best = None
        self.sixth_best = None
        self.sevent_best = None
        self.eighth_best = None
        self.ninth_best = None
        self.worst = None
        self.best_option = None
        self.best_mean = None
        self.second_option = None
        self.third_option = None
        self.fourth_option = None
        self.fifth_option = None
        self.sixth_option = None
        self.seventh_option = None
        self.eighth_option = None
        self.ninth_option = None
        self.worst_option = None
        self.third_quality_agents = []
        self.third_quality_overall = []
        self.third_quality_array = np.empty((0, self.number_of_iterations))
        self.fourth_quality_agents = []
        self.fourth_quality_overall = []
        self.fourth_quality_array = np.empty((0, self.number_of_iterations))
        self.fifth_quality_agents = []
        self.fifth_quality_overall = []
        self.fifth_quality_array = np.empty((0, self.number_of_iterations))
        self.sixth_quality_agents = []
        self.sixth_quality_overall = []
        self.sixth_quality_array = np.empty((0, self.number_of_iterations))
        self.seventh_quality_agents = []
        self.seventh_quality_overall = []
        self.seventh_quality_array = np.empty((0, self.number_of_iterations))
        self.eighth_quality_agents = []
        self.eighth_quality_overall = []
        self.eighth_quality_array = np.empty((0, self.number_of_iterations))
        self.ninth_quality_agents = []
        self.ninth_quality_overall = []
        self.ninth_quality_array = np.empty((0, self.number_of_iterations))
        self.worst_quality_agents = []
        self.worst_quality_overall = []
        self.worst_quality_array = np.empty((0, self.number_of_iterations))
        self.count_list = []
        self.alignment = 0
        self.align_percent = None
        # Other attributes initialized as None or empty collections

    def generate_means(self):
        self.quality_samples = [
            0.09090909090909091, 0.18181818181818182, 0.2727272727272727,
            0.36363636363636365, 0.45454545454545453, 0.5454545454545454,
            0.6363636363636364, 0.7272727272727273, 0.8181818181818182,
            0.9090909090909091
        ]
        self.best_mean = max(self.quality_samples)
        sorted_list = sorted(self.quality_samples, reverse=True)
        self.second_best = sorted_list[1]
        self.third_best = sorted_list[2]
        self.fourth_best = sorted_list[3]
        self.fifth_best = sorted_list[4]
        self.sixth_best = sorted_list[5]
        self.sevent_best = sorted_list[6]
        self.eighth_best = sorted_list[7]
        self.ninth_best = sorted_list[8]
        self.worst = sorted_list[9]

    @staticmethod
    def threshold(quality):
        threshold = quality
        return threshold

    @staticmethod
    def threshold_a(quality, a):
        if quality < a:
            threshold = quality
        elif quality >= a:
            threshold = a
        return threshold

    @staticmethod
    def threshold_2(quality):
        threshold = 1 / (1 + math.exp(-quality))
        return threshold

    def create_network(self):
        self.network = nx.newman_watts_strogatz_graph(
            self.number_of_agents, k=self.number_of_neighbours, p=self.connectivity)

    def sample_qualities(self):
        self.options = list(range(1, self.number_of_locations + 1))
        self.options_dc = dict(zip(self.options, self.quality_samples))

        for key, value in self.options_dc.items():
            if value == self.best_mean:
                self.best_option = key
            elif value == self.second_best:
                self.second_option = key
            elif value == self.third_best:
                self.third_option = key
            elif value == self.fourth_best:
                self.fourth_option = key
            elif value == self.fifth_best:
                self.fifth_option = key
            elif value == self.sixth_best:
                self.sixth_option = key
            elif value == self.sevent_best:
                self.seventh_option = key
            elif value == self.eighth_best:
                self.eighth_option = key
            elif value == self.ninth_best:
                self.ninth_option = key
            else:
                self.worst_option = key


        for agent in self.network.nodes:
            location = np.random.choice(self.options)
            quality = np.clip(np.random.normal(self.options_dc[location], self.sd), 0, 1)

            threshold_functions = [self.threshold, self.threshold_a, self.threshold_2]

            if self.threshold_function == 1:
                threshold = threshold_functions[self.threshold_function](quality, self.intercept)
            else:
                threshold = threshold_functions[self.threshold_function](quality)


            self.initial_choices[agent] = [location, quality, threshold]


        for agent in self.network.nodes:
            opinion = self.initial_choices[agent]
            self.updated_qualities[agent] = opinion[0]

        count = 0
        for value in self.updated_qualities.values():
            if value == self.best_option:
                count += 1

        self.best_quality_agents.append(count)

        count_2 = 0
        for value in self.updated_qualities.values():
            if value == self.second_option:
                count_2 += 1

        self.next_quality.append(count_2)

        avg = []
        for agent in self.network.nodes:
            loc = self.initial_choices[agent]
            avg.append(loc[1])

        self.average_quality = statistics.mean(avg)
        # min_max_range = [self.worst , self.best_mean]
        # self.average_quality = (self.average_quality - min_max_range[0])/(min_max_range[1] - min_max_range[0])
        self.average_qualities.append(self.average_quality)
        
        count_3 = 0
        for value in self.updated_qualities.values():
            if value == self.third_option:
                count_3 += 1

        self.third_quality_agents.append(count_3)

        count_4 = 0
        for value in self.updated_qualities.values():
            if value == self.fourth_option:
                count_4 += 1

        self.fourth_quality_agents.append(count_4)

        count_5 = 0
        for value in self.updated_qualities.values():
            if value == self.fifth_option:
                count_5 += 1

        self.fifth_quality_agents.append(count_5)

        count_6 = 0
        for value in self.updated_qualities.values():
            if value == self.sixth_option:
                count_6 += 1

        self.sixth_quality_agents.append(count_6)

        count_7 = 0
        for value in self.updated_qualities.values():
            if value == self.seventh_option:
                count_7 += 1

        self.seventh_quality_agents.append(count_7)

        count_8 = 0
        for value in self.updated_qualities.values():
            if value == self.eighth_option:
                count_8 += 1

        self.eighth_quality_agents.append(count_8)

        count_9 = 0
        for value in self.updated_qualities.values():
            if value == self.ninth_option:
                count_9 += 1

        self.ninth_quality_agents.append(count_9)

        count_10 = 0
        for value in self.updated_qualities.values():
            if value == self.worst_option:
                count_10 += 1

        self.worst_quality_agents.append(count_10)

    def communication(self, number_of_iterations):
        self.new_choices = self.initial_choices.copy()
        most_list = dict()

        for _ in range(number_of_iterations):
            
            count = 0
            count_2 = 0
     
            for agent in self.network.nodes:
                neighbours = list(self.network.neighbors(agent))
                neighbours.append(agent)
                qualities_compare, locations_compare, thresh = [], [], self.new_choices[agent][2]

                for i in neighbours:
                    qualities_assign = self.new_choices[i]
                    qualities_compare.append(qualities_assign[1])
                    locations_compare.append(qualities_assign[0])

                local_dict = dict(zip(qualities_compare, locations_compare))

                comp = Counter(locations_compare)
                major_value = max(comp.values())

                # this below code gives out the majorly chosen option from the given locations
                majority = [element for element, count in comp.items() if count == major_value]
                majority = int(majority[0])

                gamma = []

                for key, value in local_dict.items():
                    if value == majority:
                        gamma.append(key)

                # gamma_avg = len(gamma) / self.number_of_neighbours
                gamma_avg = len(gamma) / len(neighbours)
                # gamma_avg = statistics.mean(gamma)
                if gamma == []:
                    alpha = self.new_choices[agent]
                    self.updated_qualities[agent] = alpha[0]

                elif gamma != []:
                    if thresh > gamma_avg:
                        alpha = self.new_choices[agent]
                        self.updated_qualities[agent] = alpha[0]


                    elif thresh <= gamma_avg:
                        # quality = np.random.normal(self.options_dc[majority], self.sd)
                        # quality = np.clip(quality, 0, 1)
                        quality = max(gamma)
                        beta = [majority, quality, thresh]
                        self.new_choices[agent] = beta
                        self.updated_qualities[agent] = beta[0]

            avg = []
            for agent in self.network.nodes:
                loc = self.new_choices[agent]
                avg.append(loc[1])

            self.average_quality = statistics.mean(avg)
            # min_max_range = [self.worst , self.best_mean]
            # self.average_quality = (self.average_quality - min_max_range[0])/(min_max_range[1] - min_max_range[0])
            self.average_qualities.append(self.average_quality)


            for value in self.updated_qualities.values():
                if value == self.best_option:
                    count += 1

            self.best_quality_agents.append(count)
            most_list["count"] = count

            for value in self.updated_qualities.values():
                if value == self.second_option:
                    count_2 += 1

            self.next_quality.append(count_2)
            most_list["count_2"] = count_2
            # self.average_qualities[self.iterations] = avg_quality
            
            count_3 = 0
            for value in self.updated_qualities.values():
                if value == self.third_option:
                    count_3 += 1

            self.third_quality_agents.append(count_3)
            most_list["count_3"] = count_3

            count_4 = 0
            for value in self.updated_qualities.values():
                if value == self.fourth_option:
                    count_4 += 1

            self.fourth_quality_agents.append(count_4)
            most_list["count_4"] = count_4

            count_5 = 0
            for value in self.updated_qualities.values():
                if value == self.fifth_option:
                    count_5 += 1

            self.fifth_quality_agents.append(count_5)
            most_list["count_5"] = count_5

            count_6 = 0
            for value in self.updated_qualities.values():
                if value == self.sixth_option:
                    count_6 += 1

            self.sixth_quality_agents.append(count_6)
            most_list["count_6"] = count_6

            count_7 = 0
            for value in self.updated_qualities.values():
                if value == self.seventh_option:
                    count_7 += 1

            self.seventh_quality_agents.append(count_7)
            most_list["count_7"] = count_7

            count_8 = 0
            for value in self.updated_qualities.values():
                if value == self.eighth_option:
                    count_8 += 1

            self.eighth_quality_agents.append(count_8)
            most_list["count_8"] = count_8

            count_9 = 0
            for value in self.updated_qualities.values():
                if value == self.ninth_option:
                    count_9 += 1

            self.ninth_quality_agents.append(count_9)
            most_list["count_9"] = count_9

            count_10 = 0
            for value in self.updated_qualities.values():
                if value == self.worst_option:
                    count_10 += 1

            self.worst_quality_agents.append(count_10)
            most_list["count_10"] = count_10
        
        max_key = max(most_list, key=most_list.get)
        # print(max_key)
        self.count_list.append(max_key)

    def multi_runs(self, runs):
        for run_i in range(runs):
            self.sample_qualities()
            self.communication(self.number_of_iterations)

            self.average_qualities_array = np.vstack(
                (self.average_qualities_array, self.average_qualities[0:self.number_of_iterations]))
            self.best_quality_array = np.vstack(
                (self.best_quality_array, self.best_quality_agents[0:self.number_of_iterations]))
            self.next_quality_array = np.vstack(
                (self.next_quality_array, self.next_quality[0:self.number_of_iterations]))


            if run_i != runs - 1:
                self.average_qualities = []
                self.best_quality_agents = []
                self.next_quality = []
        
        self.alignment = 0 
        for i in self.count_list:
            if i == "count":
                self.alignment += 1
        
        self.align_percent = self.alignment / runs
                
        self.list_a = np.mean(self.average_qualities_array, axis=0)
        self.list_b = np.mean(self.best_quality_array, axis=0)
        self.list_n = np.mean(self.next_quality_array, axis=0)

        self.list_a_max = np.max(self.average_qualities_array, axis=0)
        self.list_b_max = np.max(self.best_quality_array, axis=0)
        self.list_n_max = np.max(self.next_quality_array, axis=0)

        self.list_a_min = np.min(self.average_qualities_array, axis=0)
        self.list_b_min = np.min(self.best_quality_array, axis=0)
        self.list_n_min = np.min(self.next_quality_array, axis=0)

    def plot_qualities(self):
        # Plotting the number of agents choosing the best quality over time
        plt.figure(figsize=(10, 8))
        plt.plot(self.list_b, label="Best Qualities", color="green")
        plt.xlabel("Iterations")
        plt.ylabel("Best Quality")
        plt.title("Best Qualities Over Time")
        plt.legend()
        plt.show()


        # Plotting the average quality of the agents at each time step
        plt.figure(figsize=(10, 8))
        plt.plot(self.list_a, label="Average Qualities", color="blue")
        plt.xlabel("Iterations")
        plt.ylabel("Average Quality")
        plt.title("Average Qualities Over Time")
        plt.legend()
        plt.show()

    def heatmap_simulation(self, index_1, index_2):
        connectivity = [ 0.15, 0.20, 0.25, 0.30]
        standard_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
        neighbours = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        intercept = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
        lists = [connectivity,standard_list, neighbours, intercept]

        number_of_iterations = 100
        avg_quality_array = np.zeros((len(lists[index_1]), len(lists[index_2])))
        best_agents_array = np.zeros((len(lists[index_1]), len(lists[index_2])))
        avg_list_array_standard = np.zeros((0, number_of_iterations))
        # best_quality_list_array = np.zeros((0, number_of_iterations))

        for i, n in enumerate(lists[index_1]):
            for j, s in enumerate(lists[index_2]):
                print(i, j, "avgqual")
                number_of_locations = 10
                number_of_agents = 200
                number_of_neighbours = n
                number_of_runs = 100
                standard_deviation = 0.06
                threshold_function = 1
                intercept = j
                connectivity = 0.15

                v4 = Threshold_Response(number_of_locations, number_of_agents, number_of_neighbours,
                                       standard_deviation, number_of_iterations, threshold_function, intercept, connectivity)

                v4.generate_means()
                v4.create_network()
                v4.multi_runs(number_of_runs)

                avg_quality_array[i, j] = v4.list_a[-1]
                best_agents_array[i, j] = v4.list_b[-1] # store the last average quality value
                avg_list_array_standard = np.vstack((avg_list_array_standard, v4.list_a))


        ax = sns.heatmap(avg_quality_array, cmap='YlGnBu')
        plt.xlabel('{}'.format(lists[index_2]))
        plt.ylabel('{}'.format(lists[index_1]))
        plt.title('Heatmap of Average Quality Values')
        plt.show()

        ax_1= sns.heatmap(best_agents_array, cmap='YlGnBu')
        plt.xlabel('{}'.format(lists[index_2]))
        plt.ylabel('{}'.format(lists[index_1]))
        plt.title('Heatmap of Best Quality Agents')
        plt.show()



    def heatmap_bestagents(self, index_1, index_2):
        connectivity = [ 0.15, 0.20, 0.25, 0.30]
        standard_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
        neighbours = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        intercept = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        lists = [connectivity,standard_list, neighbours, intercept]

        number_of_iterations = 100
        avg_quality_array = np.zeros((len(lists[index_1]), len(lists[index_2])))
        avg_list_array_standard = np.zeros((0, number_of_iterations))
        # best_quality_list_array = np.zeros((0, number_of_iterations))

        for i, n in enumerate(lists[index_1]):
            for j, s in enumerate(lists[index_2]):
                print(i, j, "agents")
                number_of_locations = 10
                number_of_agents = 200
                number_of_neighbours = n
                number_of_runs = 100
                standard_deviation = 0.06
                threshold_function = 1
                intercept = j
                connectivity = 0.15

                v4 = Threshold_Response(number_of_locations, number_of_agents, number_of_neighbours,
                                       standard_deviation, number_of_iterations, threshold_function, intercept, connectivity)

                v4.generate_means()
                v4.create_network()
                v4.multi_runs(number_of_runs)

                avg_quality_array[i, j] = v4.list_b[-1]  # store the last average quality value
                avg_list_array_standard = np.vstack((avg_list_array_standard, v4.list_b))


        ax = sns.heatmap(avg_quality_array, cmap='YlGnBu')
        plt.xlabel('{}'.format(lists[index_2]))
        plt.ylabel('{}'.format(lists[index_1]))
        plt.title('Heatmap of Best Quality Agents')
        plt.show()

    def multi_graphs(self, graph_num):

        random_colmuns = self.best_quality_array.shape[1]
        random_indices = np.random.choice(random_colmuns, size=3, replace=False)
        # best_quality_list_array = np.zeros((0, self.number_of_iterations))

        if graph_num == 1:
            percentiles= np.percentile(self.best_quality_array[:, random_indices], q= [5, 50, 95], axis=0)

            plt.plot(range(len(self.list_b)), self.list_b, label='Best Quality')
            plt.errorbar(random_indices, percentiles[1], yerr=[percentiles[1] - percentiles[0], percentiles[2] - percentiles[1]],
                         fmt='o', capsize=2)
            plt.legend()
            plt.title("Best - No. of Agents")

        elif graph_num == 2:
            percentilesavg= np.percentile(self.average_qualities_array[:, random_indices], q= [5, 50, 95], axis=0)

            plt.plot(range(len(self.list_a)), self.list_a, label="Average Qualities", color="blue")
            plt.errorbar(random_indices, percentilesavg[1], yerr=[percentilesavg[1] - percentilesavg[0], percentilesavg[2] - percentilesavg[1]],
                         fmt='o', capsize=2)
            plt.legend()
            plt.title("Average Quality")



if __name__ == '__main__':
    # Create an instance of the Version4Optimized class with appropriate parameters
    # def __init__(self, locations, agents, neighbours, sd, iterations, thresh_fun, intercept, connectivity)

    # neighbours = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
    neighbours = [2, 3, 5, 7, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    
    v4_optimized = Threshold_Response(10, 200, 40, 0.06, 100, 0, 0, 0.15)
    
        # Generate means, create network, and run the simulation
    v4_optimized.generate_means()
    v4_optimized.create_network()
    v4_optimized.multi_runs(100)
    
    #         # Plot the qualities
    v4_optimized.plot_qualities()
    v4_optimized.heatmap_simulation(2, 1)
    v4_optimized.heatmap_bestagents(2, 1)
    
    plt.figure(figsize=(10, 8))
    runs = 100
    best_quality_columns = np.zeros((runs, 0))
    avg_quality_columns = np.zeros((runs, 0))
    best_agents = []
    avg_quality = []
    alignments = []
    for i in neighbours:
        v4_optimized = Threshold_Response(10, 200, i, 0.06, 100, 0, 0, 0.15)
    
        # Generate means, create network, and run the simulation
        v4_optimized.generate_means()
        v4_optimized.create_network()
        v4_optimized.multi_runs(runs)
    
        # Plot the qualities
        # v4_optimized.plot_qualities()
        # v4_optimized.heatmap_simulation(2, 1)
    
        column = v4_optimized.best_quality_array[:, -1].reshape(runs, 1)
        best_quality_columns = np.hstack((best_quality_columns, column))
    
        avg_column = v4_optimized.average_qualities_array[:, -1].reshape(runs, 1)
        avg_quality_columns = np.hstack((avg_quality_columns, avg_column))
    
        random_colmuns = v4_optimized.best_quality_array.shape[1]
        random_indices = np.random.choice(random_colmuns, size=3, replace=False)
        percentiles= np.percentile(v4_optimized.best_quality_array[:, random_indices], q= [5, 50, 95], axis=0)
    
        best_agents.append(v4_optimized.list_b[-1])
        avg_quality.append(v4_optimized.list_a[-1])
        alignments.append(v4_optimized.align_percent)
        plt.ylim(15, 30)
        plt.plot(range(len(v4_optimized.list_b)), v4_optimized.list_b, label='Best Quality {}'.format(i))
        #                   , color="green")
        plt.errorbar(random_indices, percentiles[1], yerr=[percentiles[1] - percentiles[0], percentiles[2] - percentiles[1]],
                      fmt='o', capsize=1, label = "{}".format(i))
        plt.legend()
        plt.title("Best - No. of Agents")
    
    
    plt.figure(figsize=(10, 8))
    ptiles_best = np.percentile(best_quality_columns, q=[10, 50, 90], axis=0)
    plt.plot(neighbours, best_agents, marker='o', color='black', linestyle='-')
    
    random_colmuns = best_quality_columns.shape[1]
    random_indices = np.random.choice(random_colmuns, size=len(neighbours), replace=False)
    
    plt.errorbar(neighbours, ptiles_best[1], yerr=[ptiles_best[1] - ptiles_best[0], ptiles_best[2] - ptiles_best[1]],
                  fmt='.', capsize=1, label = "{}".format(i), color="lightgray")
    plt.xlabel('Neighbours')
    plt.ylabel('Agents')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    
    plt.show()
    
    plt.figure(figsize=(10, 8))
    ptiles_avg = np.percentile(avg_quality_columns, q=[10, 50, 90], axis=0)
    plt.plot(neighbours, avg_quality, marker='o', color='black', linestyle='-')
    
    random_colmun_a = avg_quality_columns.shape[1]
    random_indice_a = np.random.choice(random_colmun_a, size=len(neighbours), replace=False)
    
    plt.errorbar(neighbours, ptiles_avg[1], yerr=[ptiles_avg[1] - ptiles_avg[0], ptiles_avg[2] - ptiles_avg[1]],
                  fmt='.', capsize=1, label = "{}".format(i), color="lightgray")
    plt.xlabel('Neighbours')
    plt.ylabel('Average Quality')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(10, 8))
    ptiles_avg = np.percentile(avg_quality_columns, q=[5, 50, 95], axis=0)
    plt.plot(neighbours, alignments, marker='o', color='black', linestyle='-')
    
    plt.xlabel('Neighbours')
    plt.ylabel('Alignment with Best Quality')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
        
