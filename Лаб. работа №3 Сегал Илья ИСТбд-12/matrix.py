import random

def generate_matrix(n): # генерация случайной квадратной матрицы N x N
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]

def print_matrix(matrix, name): # выводит матрицу в читабельном виде
    print(f"\n{name}:")
    for row in matrix:
        print(" ".join(f"{x:3}" for x in row))

def transpose(matrix): # транспонирование
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def copy_matrix(matrix): # создает копию матрицы
    return [row[:] for row in matrix]

def swap_symmetric_regions(matrix, n): # меняем области 1 и 3 местами симметрично
    for i in range(n // 2):
        for j in range(i + 1, n - i - 1):
            matrix[i][j], matrix[n - i - 1][j] = matrix[n - i - 1][j], matrix[i][j]

def swap_non_symmetric_regions(matrix, n): # меняем области 1 и 2 местами несимметрично
    for i in range(n // 2):
        for j in range(n // 2):
            matrix[i][j], matrix[i][n // 2 + j] = matrix[i][n // 2 + j], matrix[i][j]

def count_even_in_odd_columns(matrix, n): # подсчет четных чисел в нечетных столбцах области 2
    count = 0
    for i in range(n // 2):
        for j in range(n // 2, n):
            if j % 2 == 0 and matrix[i][j] % 2 == 0:
                count += 1
    return count

def perimeter_product(matrix, n): # произведение чисел по периметру области 3
    prod = 1
    for j in range(n // 2, n):
        prod *= matrix[n // 2][j]  # верхняя граница
        prod *= matrix[n - 1][j]  # нижняя граница
    for i in range(n // 2 + 1, n - 1):
        prod *= matrix[i][n // 2]  # левая граница
        prod *= matrix[i][n - 1]  # правая граница
    return prod

def matrix_addition(A, B, n): # Сложение матриц
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def matrix_multiplication(A, B, n): # перемножение матриц
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return result

def matrix_scalar_multiplication(matrix, scalar, n): # умножение матрицы на скаляр
    return [[scalar * matrix[i][j] for j in range(n)] for i in range(n)]

# ввод k и n
K = int(input("Введите K: "))
N = int(input("Введите N (четное число): "))
assert N % 2 == 0, "N должно быть четным"

# генерация случайной матрицы A
A = generate_matrix(N)
print_matrix(A, "Матрица A")

# копируем части A в F
F = copy_matrix(A)

# проверка наших условий
even_count = count_even_in_odd_columns(A, N)
perim_product = perimeter_product(A, N)

if even_count > perim_product:
    swap_symmetric_regions(F, N)
else:
    swap_non_symmetric_regions(F, N)

print_matrix(F, "Матрица F")

# вычисление выражения по тз 
A_T = transpose(A)
F_T = transpose(F)
K_AT = matrix_scalar_multiplication(A_T, K, N)
F_plus_A = matrix_addition(F, A, N)
K_AT_mul_F_plus_A = matrix_multiplication(K_AT, F_plus_A, N)
K_F_T = matrix_scalar_multiplication(F_T, K, N)
result = matrix_addition(K_AT_mul_F_plus_A, matrix_scalar_multiplication(K_F_T, -1, N), N)

print_matrix(result, "Результат выражения")
