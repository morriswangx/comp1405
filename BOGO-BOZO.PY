import random
import time
 
def swap(a, b):
    temp = a
    a = b
    b = temp
    return a, b
 
def isSorted(vals):
   for i in range(0, len(vals) - 1):
       if vals[i] > vals[i + 1]:
           return False
   return True
 
# Check if an value is in the list
def inList(vals, val):
   for i in range(len(vals)):
       if vals[i] == val:
           return True
   return False
 
# get a list of unique numbers from 0 to the highest index
# for example: [2,1,3,0]
def getRand(vals):
   listRandoms = []
   while len(listRandoms) < len(vals):
        # generate a random number that is between 0 and the highest index of the given list inclusive
       num = random.randint(0, len(vals) - 1)
       # if the newly generated random number is not in the list, it will be added to the listRandom
       if inList(listRandoms, num) is False:
           listRandoms.append(num)
 
   return listRandoms # finally after the while loop, return the generated random number list
 
def bogosort(vals):
    print("Bogosorting..." , vals)
 
    while isSorted(vals) is False:
 
       listr = getRand(vals)
       # print("Generated unique numbers: ", listr)
     
       # use the new random index list to get a new shuffled list
       listtemp = []
       for i in range(len(listr)):
           listtemp.append(vals[listr[i]])
 
       #print("Attempted sort: ", listtemp)
     
       # reassign the newly sorted list back to the original list before checking if it's sorted
       vals = listtemp
 
    print("Bogosorted: ", vals)
 
def bozosort(vals):
    print("Bozosorting..." , vals)
    while isSorted(vals) is False:
        rand1 = random.randint(0, len(vals) -1)
        rand2 = random.randint(0, len(vals) -1)
        while rand1 == rand2:
            rand2 = random.randint(0, len(vals) -1)
        # print("rand1 and rand2: ", str(rand1), str(rand2))
        # print("There values: ", vals[rand1], vals[rand2])
        listtemp = swap(vals[rand1], vals[rand2])
        vals[rand1] = listtemp[0]
        vals[rand2] = listtemp[1]
        # print("There values after swap: ", vals[rand1], vals[rand2])
    print("Bozosorted: " , vals)
    return vals  
 
def main(runtimes=5):    
    bozotime = time.time()
   
    for i in range(runtimes):
        bozosort(  [3,2,34,65,80,7] )
    print("Time took for bozosort: ", (time.time()-bozotime))
 
    # reset the list for bogosorting
    bogotime = time.time()
    for i in range(runtimes):
        bogosort( [3,2,34,65,80,7] )
 
    print("Time took for bogosort: ", (time.time()-bogotime))
 
 
main()
 


