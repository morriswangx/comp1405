import random

def swap(list, i, j):
    temp = list[i]
    list[i] = list[j]
    list[j] = temp
    return list

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
    listr = []
    while len(listr) < len(vals):
        num = random.randint(0, len(vals) - 1)
        # print("generatee number:", num)
        if inList(listr, num) is False:
            listr.append(num)
    return listr

def bogosort(vals):

    while isSorted(vals) is False:

        listr = getRand(vals)
        print("Generated unique numbers: ", listr)

        # use the new random index list to get a new shuffled list
        listtemp = []
        for i in range(len(listr)):
            listtemp.append(vals[listr[i]])

        print("Attempted sort: ", listtemp)

        # reassign the newly sorted list back to the original list before checking if it's sorted
        vals = listtemp

    print("Finally sorted: ", vals)

def main():
    lista = [9, 2, 8, 1,34,2,9,20]
    bogosort(lista)

main()




