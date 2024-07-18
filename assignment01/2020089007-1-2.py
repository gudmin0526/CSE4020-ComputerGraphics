import numpy as np

np.set_printoptions(linewidth=np.inf)

# A
M = np.arange(2, 27)
print(M, end="\n\n")

# B
M = M.reshape(5, 5)
print(M, end="\n\n")

# C
M[1:4, 1:4] = np.zeros((3, 3))
print(M, end="\n\n")

# D
M = M @ M
print(M, end="\n\n")

# E
v = np.sqrt(M[0] @ M[0])
print(v, end="")
