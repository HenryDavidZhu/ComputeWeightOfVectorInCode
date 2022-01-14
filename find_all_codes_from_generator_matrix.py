import numpy as np
import itertools
import sys

# Codes are generated using the formula: sG
# s is input vector, G is the generator matrix.
def codeMinWeightFromGenMatrix(generatorMatrix, order):
    minCodeWeight = sys.maxsize
    minCodeWord = []
    minCodeVector = []
    
    # Convert the provided generator matrix into a numpy matrix.
    npGeneratorMatrix = np.matrix(generatorMatrix)

    # Generate an array storing the range of possible values in
    # the finite field.
    possibleValues = [i for i in range(order)]
    print("possibleValues = " + str(possibleValues))

    # Generate the 2D array storing the possible range of values for each
    # index in to the input vector.
    vecRangesOfValues = []
    for i in range(len(generatorMatrix)):
        vecRangesOfValues.append([0, order-1])

    # Generate all possible input vectors.
    inputVectors = list(itertools.product(*(range(low, high+1) for low, high in vecRangesOfValues)))

    # Iterate through all possible input vectors (s).
    for inputVector in inputVectors:
        # Compute sG
        sG = np.matmul(inputVector, generatorMatrix)

        # Convert code = sG to be in the finite field F(order), and figure out
        # its weight.
        codeInField = convertCodeToField(sG, order)
        codeWeight = findCodeWeight(codeInField)

        print("weight(" + str(codeInField) + ") = " + str(codeWeight))

        if codeWeight < minCodeWeight:
            if codeWeight != 0:
                minCodeWeight = codeWeight
                minCodeWord = codeInField
                minCodeVector = inputVector

    print("\nFinal Result:")
    print("minCodeWeight = " + str(inputVector) + " * " + str(generatorMatrix))
    print("(minCodeWeight, minCodeWord) = (" + str(minCodeWeight) + ", " + str(minCodeWord) + ")")
    return (minCodeWeight, minCodeWord)

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

# Determines the weight of a code.
def findCodeWeight(code):
    codeWeight = 0

    for element in code:
        if element != 0:
            codeWeight += 1

    return codeWeight

generatorMatrix = [[1, 0, 0, 2, 1, 0],[0, 1, 0, 3, 3, 4],[0, 0, 1, 0, 1, 4]]
codeMinWeightFromGenMatrix(generatorMatrix, 5)
