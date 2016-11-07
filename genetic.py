'''
******************************************************************************
code name:- genetic algorithm to evaluate a function
function :- x/(1+x**2)


******************************************************************************

'''
from random import random, randint,sample
import math

def calculate(x):
   '''
   input:- a number
   output:- value calculated on based on function
   purpose:- to evaluate the contraint function
   '''
   a=float(x/(1+(x**2)))#constraint for the problem
   return a

def mapping(list):
   '''
   input:-a list of n random integers
   output:-a list of n calculated values
   purpose:- to map the contraint function to the list
   approch :- list comprehension 
   '''

   return [calculate(x) for x in list]#mapping with contraint
   
def individual(length, min, max):
   '''
   input:-range and size of the list to be created
   output:-a list of n random integers
   purpose:- to generate n random numbers based on the range and size of the list provided
   '''
   return [ randint(min,max) for x in range(length) ]#random number generation

def evolution(individual):
   '''
   input:- a population of n numbers
   output:- fitness of population
   purpose:- to evaluate the fitness of the gven population!
   '''
   fitness=mapping(individual)
   return fitness
      
def probability(list):
   '''
   input:-a list of n numbers
   output:-a list containing the probabilities
   purpose:- to evaluate the probability of each member 
   '''
   s=sum(list)#sum of all
   prob=[]
   for z in range(0,len(list)):
         temp=list[z]/s#probability calculation
         prob.append(temp)
   return prob
   
def random_append(size):
   '''
      input:-size of list to generate
      output:-list of size specied containg numbers between 0-1 generated randomally
      purpose:- 
   '''
   r=[]
   for i in range(size):
      r.append(random())#random number generation between 0-1
   return r
   
def roullete_population(rand,population,cum_prob):
   '''
   input:-list of random number,sample population,cummulative probability
   output:-selected population 
   purpose:- perform genetic selection on basis of random list
   '''
   new_pop=[]
   len_cf=len(cum_prob)
   for a in rand:
      if a<=cum_prob[0]:
         new_pop.append(population[0])
      else:
         for i in range(1,len_cf):
            if(i<len_cf):
               if cum_prob[i-1] < a <=cum_prob[i]:
                  new_pop.append(population[i])
            else:
              new_pop.append(x[len_cf])
   return new_pop
   
def cumm(prob):
   '''
   input:-a list containing probability
   output:-a list containing random probability
   purpose:-to calculate cummulative probability from probabilities  
   '''
   cumm=[]
   cumm.append(prob[0])
   for z in range(1, len(prob)):
      #calculating cummulative probability
      cumm.append(cumm[z-1] + prob[z])
   return cumm

def crossover(size,cross_ratio,population,min,max):
   '''
   input:-population of specified size in range min-max and crossover ratio
   output:-crossovered population of same size and in range
   purpose:- to perform crossover and perform genetic mating to generate next generation
   '''
   parent=[]
   parentpos=[]
   parentnumber=0
   ra=random_append(size)
   for i in range(0,size):
      if ra[i]<cross_ratio:
         parentnumber=parentnumber+1
   #crossover possible if more than 1 parents
   # single parent cannot do crossover
   if parentnumber>=2:      
      ba=[]
      temp=math.log2(max)
      bitsize=math.floor(temp)+1
      #converting to binary
      for i in range(0,size):
            temp=binary(population[i],bitsize)
            ba.append(temp)
      #check for crossover possibility
      for i in range(0,size):
         if ra[i]<cross_ratio:  
            parent.append(ba[i])
            parentpos.append(i)

      lengthparent=len(parent)
      #generating cut position
      cut=cutposition(lengthparent,bitsize)
      #mating of even possible
      #1-1 mating only
      if parentnumber%2!=0:
         parentnumber=parentnumber-1
      #performing mating and change in population for new generation
      for i in range(0,parentnumber,2): 
         child=mating(parent[i],parent[i+1],cut[i])
         child1=binarytoint(child[0])
         child2=binarytoint(child[1])
         if (min<=child1 and child1<=max) and (min<=child2 and child2<=max):
            population[parentpos[i]]=child1
            population[parentpos[i+1]]=child2
   return population
   
def binarytoint(list):
   '''
   input:-a 2d list of n binary numbers
   output:-a 1d list of n integers
   purpose:- to convert binarylist to a integer
   '''
   val=0               
   for i in range(0,len(list)):
      #bitwise transformtion
      val=(list[i]*(2**i))+val
   return val
   
def mating(parent1,parent2,position):
   '''
   input:-2 parents and their mating position
   output:- a list of 2 childs
   purpose:- to perform mating of parents and generation of offsprings
   '''
   #  single point cut
   child=[]
   child.append([])
   child.append([])
   #no swapping before cut positon
   for i in range(0,position):
      child[0].append(parent1[i])
      child[1].append(parent2[i])
   #swapping after cut position
   for i in range(position+1,len(parent1)):
      child[0].append(parent2[i])
      child[1].append(parent1[i])
   return child

def cutposition(size,bitsize):
   '''
   input:-size of population,size of each binary list in one individual
   output:-list of cut positions
   purpose:- to generate cut position depending on population
   '''
   cut=[]
   for i in range(0,size):
      temp=randint(1,bitsize)
      cut.append(temp)
   return cut

def binary(item,no_of_bits):
   '''
   input:-item in integer and no_of_bits in case of padding is required
   output:-binary number with suitable padding
   purpose:- to generate binary list for integer
   '''
   temp=[int(i) for i in str(bin(item))[2:]]
   temp_size=len(temp)
   #padding extra 0 in front if required
   while(temp_size<=no_of_bits):
      temp.insert(0,0)
      temp_size=temp_size+1
   return temp

def mutation(size,population,mutation_ratio,min,max):
   '''
   input:-population and he mutation ratio 
   output:-mutated population
   purpose:- to perform genetic mutation on the population
   '''
   ba=[]
   #calculating bit size to generate at max bits in binary
   alpha=math.log2(max)
   bitsize=math.floor(alpha)+1
   #binary conversion
   for i in range(0,size):
      temp=binary(population[i],bitsize)
      ba.append(temp)
   total=bitsize*size  
   #calculating mutation bits
   mut=int(mutation_ratio*total)      
   mut_bits=sample(range(0,total),mut)
   #converting mutation bits to 2d indexes
   for i in range(0,mut):
      temp=[]
      row=int(mut_bits[i]/bitsize)
      col=mut_bits[i]%bitsize
   #inversion on mutation
      for i in range(0,bitsize):
         if i!=col:
            temp.append(ba[row][i])
         else:
            if ba[row][col]==1:
               temp.append(0)
            elif ba[row][col]==0:
               temp.append(1)
      delta=binarytoint(temp)
      #checking mutation on bounds
      if min<=delta and delta<=max:
         ba[row]=temp
         gamma=binarytoint(ba[row])
         population[row]=gamma
   return population
            
def genetic():
   '''
   input:- genetic parameters from user
   output:- value at which the constraint is maximized
   purpose:-to use genetic algorithm procedure to evaluate the objective
   approch:- use of genetic algorithm to solve complex computational problem
   
   '''
   min=int(input("enter the min value of range :- "))
   max=int(input("enter the max value of range :- "))
   iteration=int(input("enter the no iterations :-"))
   count=int(input("enter population size:-"))
   cross_ratio=float(input("enter cross over ratio in percentage 0.00-1.00 recommended 0.60 :-"))
   mutation_ratio=float(input("enter mutation ratio in percentage 0.00-1.00 recommended 0.10 :-"))
   population=individual(count,min,max)
   objective=0
   check=0
   index=0
   index1=0
   for i in range(0,iteration):
      print("iteration no")
      print(i)
      print ("population")
      print(population)
      fit=evolution(population)
      print("fitness")
      print(fit)
      param=population[index1]     
      prob=probability(fit)
      cummulative=cumm(prob)
      rand=random_append(count)
      nextgen=roullete_population(rand,population,cummulative)
      population=crossover(count,cross_ratio,nextgen,min,max)
      population=mutation(count,population,mutation_ratio,min,max)
   print(population)
   fit=[]
   fit=evolution(population)
   for i in range(0,count):
      if objective<fit[i]:
         objective=fit[i]
         index=i
   print("max value at ")
   print(population[index])

genetic()

