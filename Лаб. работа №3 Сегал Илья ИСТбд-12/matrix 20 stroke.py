import random

def generate_matrix(n): return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
def print_matrix(matrix, name): 
    print(f"\n{name}:")
    for row in matrix: print(" ".join(f"{x:3}" for x in row))

def transpose(matrix): return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
def swap_symmetric_regions(matrix, n):
    for i in range(n // 2):
        for j in range(i + 1, n - i - 1): matrix[i][j], matrix[n - i - 1][j] = matrix[n - i - 1][j], matrix[i][j]

K, N = int(input("Введите K: ")), int(input("Введите N (четное число): "))
assert N % 2 == 0, "N должно быть четным"

A = generate_matrix(N)
F = [row[:] for row in A]

if sum(1 for i in range(N//2) for j in range(N//2, N) if j % 2 == 0 and A[i][j] % 2 == 0) > sum(A[N//2][j] * 2 for j in range(N//2, N)):
    swap_symmetric_regions(F, N)

print_matrix(A, "Матрица A")
print_matrix(F, "Матрица F")

A_T, F_T = transpose(A), transpose(F)
result = [[K * A_T[i][j] + K * F_T[i][j] for j in range(N)] for i in range(N)]

print_matrix(result, "Результат выражения")
