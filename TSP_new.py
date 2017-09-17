
# coding: utf-8

# In[1]:

import os
import time
import numpy as np
import random as rnd
import argparse



# In[2]:

#Instances in each generation
n_population = 100

#Iterations
n_generation = 20000
# Mutation Chance
prob_mutation = 1

# Crossover Chance
prob_crossover = 1


# In[3]:

def get_best(generation,distance_matrix,n_cities):
    
    new_generation = []
    
    prob, fit, dist = fitness(generation,distance_matrix)
    
    gene = (generation[0],dist[0],fit[0])
    
    parents = selection(generation,prob,fit,dist)
    for i in range(n_population):
        
        # print("Creating Instance... ",i)
        #Find Parents
       
        #Get Child
        child = get_child(parents,distance_matrix,n_cities)
    
        # Check if the CHILD formed is better
        if child[2] > gene[2]:
            gene = child
        # print(child[1])
        
        new_generation.append(child[0])
    
    #Generation = [Permutation of Numbers]
    #Gene = [Gene, Distance, Fitness]
    
#     print("new_generation",new_generation)
#     print("Gene : ",gene)
#     print("\n")
    return new_generation, gene
        


# In[4]:

def selection(generation,prob,fitness,distance):
    
    parent = []
    
    rand_prob = rnd.random()

    bprob = prob[0]
    sbprob = prob[1]

    parent.append((generation[0],distance[0],fitness[0]))
    parent.append((generation[1],distance[1],fitness[1]))
    
    parent1=False
    
    # #Iterate over all Population
    # for i in range(0,len(generation)):
        
    #     if prob[i] > rand_prob and parent1 == False:
    #         parent[0] = (generation[i],distance[i],fitness[i])
    #         parent1 = True
            
    #     elif  prob[i] > rand_prob:
    #         parent[1] = (generation[i],distance[i],fitness[i])
    #         break

    #     #Iterate over all Population
    for i in range(1,len(generation)):
        
        if bprob < prob[i]:
            sbprob = bprob
            bprob = prob[i]
            parent[1] = parent[0]
            parent[0] = (generation[i],distance[i],fitness[i])
            
        elif sbprob < prob[i]:
            sbprob = prob[i]
            parent[1] = (generation[i],distance[i],fitness[i])
    #Parent  = [Gene, Distance, Fitness]
    return parent


# In[5]:

def get_child(parent,distance_matrix,n_cities):
    
    x = rnd.random()
    
    m_child = parent[0][0]
    
    if x < prob_crossover:   
        m_child = crossover(parent,n_cities)
    
    y = rnd.random()
    
    if y < prob_mutation:
        m_child = mutate(m_child,n_cities)
    
    
    fit,dist = calc_fitness(m_child,distance_matrix)
    
    child = (m_child,dist, fit)
    
    #Child  = [Gene, Distance, Fitness]
    return child


# In[6]:

def crossover(parent,n_cities):
    
#     n_cities = len(parent[0][0])
    
    child = np.zeros(n_cities)
    city_used = dict()
    
    startx = rnd.randrange(0,n_cities-1)
    endx = rnd.randrange(startx+1,n_cities)
    
    
    for i in range(0,n_cities+1):
        city_used[i] = False
        
    for i in range(startx,endx):
        child[i] = parent[0][0][i]
        city_used[child[i]] = True
    
    end = 0
    
    for i in range(startx):
        for j in range(end,n_cities):
            if city_used[parent[1][0][j]] == False:
                child[i] = parent[1][0][j]
                end = j+1
                break
                
    for i in range(endx,n_cities):
        for j in range(end,n_cities):
            if city_used[parent[1][0][j]] == False:
                child[i] = parent[1][0][j]
                end = j+1
                break
        
#     child  = [Gene]
#     print("Crossover Child = ",child)
    return child


# In[7]:

def mutate(m_child,n_cities):
    
    startx = rnd.randrange(0,n_cities-1)
    endx = rnd.randrange(startx+1,n_cities)
    
    temp = m_child[endx]
    m_child[endx] = m_child[startx]
    m_child[startx] = temp
    
    #m_child  = Gene
#     print("mutate_child",m_child)
    return m_child


# In[8]:

def encoding(n_cities):
    
    generation = []
    gene = []
    
    gene =  np.random.permutation(n_cities)
    generation.append(gene)
   
    for i in range(1,n_population):
        gene =  np.random.permutation(n_cities)
        # while(city_search(gene,generation,i)==True):
            # gene =  np.random.permutation(n_cities)
        generation.append(gene)       
            
    #Generation = [Permutation of Numbers]
    return generation


# In[9]:

def city_search(gene, generation, end):

    for i in range(0,end):
        if (generation[i] == gene).all():
            return True
        
    return False


# In[10]:

def calc_fitness(gene,distance_matrix):
    
    dist = 0.0
    
    for i in range(len(gene)-1):
        dist += distance_matrix[int(gene[i])][int(gene[i+1])]
    
    fitness = 1/dist
    
    #Return Fitness and Distance of a Gene
    return fitness,dist


# In[11]:

def fitness(generation,distance_matrix):
    
    s_fitness = 0
    
    prob = dict()  
    distance = dict()
    fitness=dict()
    
    i=0
    
    for gene in generation:
        fit,dist = calc_fitness(gene,distance_matrix)
        s_fitness += fit
        #prob[i] = fit
        fitness[i] = fit
        distance[i] = dist
        i+=1
    
    i=0
    
    for gene in generation:
        prob[i] = fitness[i]/s_fitness
        i+=1
    
    #Return Probability, Fitness, Distance of full generation
    return prob,fitness,distance


# In[12]:

def read_data(filename):
    
    file = open(filename,"r")
    lines = file.readlines()
    
    data_type = lines[0]
    n_cities = int(lines[1])
    
    cities = dict()

    for i in range(2,n_cities+2): 
        x = lines[i].split("\n")
        y = x[0].split(" ")

        #cities[i-2].append((i-1,y))
        cities[i-2] = y

    distance_matrix = np.zeros((n_cities,n_cities))

    for i in range(n_cities+2,2*n_cities+2):
        x = lines[i].split("\n")
        y = x[0].split(" ")

        for j in range(0,n_cities):
            distance_matrix[i-n_cities-2][j] = float(y[j])



    print("Data Loaded... ")
    return n_cities, cities, distance_matrix   

    


# In[13]:

def main():
    
    path = "./TestCases/"

    global n_generation
    global n_population

    DATASET={

            "euc_100":path + "euc_100",
            "euc_250":path + "euc_250",
            "euc_500":path + "euc_500",
            "noneuc_100":path + "noneuc_100",
            "noneuc_250":path + "noneuc_250",
            "noneuc_500":path + "noneuc_500"
    }
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True,
        help="File name")
    ap.add_argument("-g", "--generation",type=int, required=False,
        help="Generation")
    ap.add_argument("-p", "--population",type=int,required=False,
        help="Population")
    args = vars(ap.parse_args())


    if args["file"] not in DATASET.keys():
        raise AssertionError("File Not Found")
    if args["generation"] is not None:
        if (args["generation"] < 1):
            raise AssertionError("Minimum number of generations is 1")
        n_generation = args["generation"]
    if args["population"] is not None:
        if (args["population"] < 2):
            raise AssertionError("Minimum population is 2")
        n_population = args["population"]

    file = DATASET[args["file"]]
  

    print(" Loading Data... ")
    n_cities, cities, distance_matrix = read_data(file)
    
    #First Generation
    print(" Generating Generation... 1 ")
    generation = encoding(n_cities)
    print(" Formed Generation... 1 ")
    best_gene = (generation[0],0.0,0.0)
    
    for i in range(n_generation):
        
        print("Running Generation... ",i)
        generation, gene =  get_best(generation,distance_matrix,n_cities)
        if gene[2] > best_gene[2]:
            best_gene = gene
            # print(best_gene)
        
        print("Distance = ",best_gene[1])
        print("\n")
    
    print("Distance = ",best_gene[1])


# In[14]:

if __name__ == "__main__":
    main()





