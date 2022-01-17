import numpy as np
import itertools
import sys

# Generate a list of possible codewords based upon the length of
# the codeword and the size q of the finite field (F_q) it is over.
def generateCodewords(n, q):
    # Generate the 2D array storing the possible range of values for
    # each index in the codeword.
    vecRangesOfValues = []
    for i in range(n):
        vecRangesOfValues.append([0, q - 1])
        
    # Generate all possible codewords
    allCodewords = list(itertools.product(*(range(low, high+1) for low, high in vecRangesOfValues)))

    return allCodewords

# Find all the syndromes from the complete list of code words, and
# also the corresponding coset leaders for those syndromes, given
# a list of all the codewords, the parity check matrix, and the size
# of the finite field.
def findSyndromeAndCosetLeaders(codewords, parityCheckMatrix, q):
    # Convert the provided parity check matrix into a numpy matrix.
    npParityCheckMatrix = np.matrix(parityCheckMatrix)

    # Mapping of syndrome to its corresponding list of codewords.
    syndromeToCodewords = {}
    
    # Mapping of syndrome to its coset leader.
    syndromeToCosetLeader = {} 

    # Iterate through every possible codeword.
    for codeword in codewords:
        # Determine the resulting parity check from that codeword.
        parityCheck = np.matmul(parityCheckMatrix, np.transpose(codeword))

        # We can't use a matrix as a key in the dictionary, so we convert it
        # into a string.
        parityCheckKey = str(convertCodeToField(parityCheck, q))

        # Case 1: the parity check result doesn't already exist in our mappings.
        if parityCheckKey not in syndromeToCodewords:
            syndromeToCodewords[parityCheckKey] = [codeword]
            syndromeToCosetLeader[parityCheckKey] = codeword
        # Case 2: the parity check result already exists in our mappings.
        else:
            parityCheckKeyCoset = syndromeToCodewords[parityCheckKey]
            parityCheckKeyCoset.append(codeword)
            syndromeToCodewords[parityCheckKey] = parityCheckKeyCoset

            # If the Hamming weight of the current codeword is less than the stored
            # coset leader of the syndrome, update the syndrome's coset leader to
            # be the current codeword.
            if getHammingWeight(codeword) < getHammingWeight(syndromeToCosetLeader[parityCheckKey]):
                syndromeToCosetLeader[parityCheckKey] = codeword

    for syndrome, cosetLeader in syndromeToCosetLeader.items():
        print("Syndrome = " + syndrome + "\nCoset Leader = " + str(cosetLeader) + " | weight(Coset Leader) = " +
              str(getHammingWeight(cosetLeader)) + " | Coset = " + str(syndromeToCodewords[syndrome]) + "\n")
    #print("str(syndromeToCodewords) = " + str(syndromeToCodewords))
    #print("str(syndromeToCosetLeader) = " + str(syndromeToCosetLeader))

# Converts an element to be in a finite field.
def convertElementToField(element, order):
    while (element >= order):
        element = element % order

    return element

# Converts a matrix to be in a finite field.
def convertCodeToField(code, order):
    for i in range(len(code)):
        code[i] = convertElementToField(code[i], order)

    return code

# Get the Hamming weight from a vector.
def getHammingWeight(vector):
    #print("vector = " + str(vector))
    hammingWeight = 0
    
    for element in vector:
        #print("element = " + str(type(element)))
        if element != 0:
            hammingWeight += 1

    #print("hammingWeight = " + str(hammingWeight))
    return hammingWeight

allCodewords = generateCodewords(4, 2)
parityCheckMatrix = [
        [1, 0, 0, 1],
        [0, 1, 1, 0]
    ]
findSyndromeAndCosetLeaders(allCodewords, parityCheckMatrix, 2)
#print(len(generateCodewords(4, 2)))
