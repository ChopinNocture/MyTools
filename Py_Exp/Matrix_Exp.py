import numpy as np

row = 3
col = 4
test_Mat = np.random.randint(row*col, size=row*col)

print(test_Mat.reshape(row, col))
print(test_Mat)


def buildStringFromMatrix(mat, numRows, numColumns):
    return ""