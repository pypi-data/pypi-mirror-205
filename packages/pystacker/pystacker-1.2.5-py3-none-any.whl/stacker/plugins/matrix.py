import numpy as np


def matrix_add(mat1, mat2):
    return list(np.add(mat1, mat2))


def matrix_sub(mat1, mat2):
    return list(np.subtract(mat1, mat2))

def matrix_mul(mat1, mat2):
    return list(np.matmul(mat1, mat2))

def matrix_transpose(mat):
    return list(np.transpose(mat))

def matrix_inverse(mat):
    return np.linalg.inv(mat)

def matrix_determinant(mat):
    return np.linalg.det(mat)

def matrix_eigenvalues(mat):
    return np.linalg.eigvals(mat)

def matrix_eigenvectors(mat):
    _, eigenvectors = np.linalg.eig(mat)
    return eigenvectors

def matrix_rank(mat):
    return np.linalg.matrix_rank(mat)

def setup(stacker_core):
    stacker_core.register_plugin("matrix_add", matrix_add)
    stacker_core.register_plugin("matrix_sub", matrix_sub)
    stacker_core.register_plugin("matrix_mul", matrix_mul)
    stacker_core.register_plugin("matrix_transpose", matrix_transpose)
    stacker_core.register_plugin("matrix_inverse", matrix_inverse)
    stacker_core.register_plugin("matrix_determinant", matrix_determinant)
    stacker_core.register_plugin("matrix_eigenvalues", matrix_eigenvalues)
    stacker_core.register_plugin("matrix_eigenvectors", matrix_eigenvectors)
    stacker_core.register_plugin("matrix_rank", matrix_rank)
