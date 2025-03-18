import random

def generate_matrix(n): return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
def print_matrix(matrix, name): 
    print(f"\n{name}:")
    for row in matrix: print(" ".join(f"{x:3}" for x in row))

def transpose(matrix): return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def get_even_count_odd_columns_region2(A, N):
    return sum(1 for i in range(N//2) for j in range(N//2, N) if j % 2 != 0 and A[i][j] % 2 == 0)

def get_perimeter_product_region3(A, N):
    product = 1
    for i in range(N//2, N): product *= A[i][N-1] if i < N-1 else A[N//2][i]
    for j in range(N//2): product *= A[j][N//2] if j > N//2 else A[N-1][j]
    return product

K, N = int(input("Введите K: ")), int(input("Введите N: "))

A = generate_matrix(N)
print_matrix(A, "Исходная матрица A")
F = [row[:] for row in A]

even_count = get_even_count_odd_columns_region2(A, N)
perimeter_product = get_perimeter_product_region3(A, N)
print(f"\nКоличество четных чисел в области 2: {even_count}")
print(f"Произведение по периметру области 3: {perimeter_product}")

if even_count > perimeter_product:
    F = [[F[N-1-i][N-1-j] for j in range(N)] for i in range(N)]
else:
    F = [[F[i][j-N//2] if j >= N//2 else F[i][j+N//2] for j in range(N)] for i in range(N)]

print_matrix(F, "Измененная матрица F")

A_T = transpose(A)
F_T = transpose(F)
result = [[sum(K * A_T[i][k] * (F[j][k] + A[j][k]) for k in range(N)) - K * F_T[i][j] for j in range(N)] for i in range(N)]
print_matrix(result, "Результат выражения")
