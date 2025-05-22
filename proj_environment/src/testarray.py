import numpy as np

A = np.array([[0, 1], [1, 1], [2, 1], [3, 1]])
b = np.array([1, 4, 3, 5])
A_T = np.transpose(A)
A_T_A = np.matmul(A_T, A)
A_T_b = np.matmul(A_T, b)
print(A_T_A)
print(A_T_b)
x_hat = np.linalg.solve(A_T_A, A_T_b)
print(x_hat)
