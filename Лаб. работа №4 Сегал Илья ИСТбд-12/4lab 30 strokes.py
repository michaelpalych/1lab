import numpy as np
import matplotlib.pyplot as plt

def load_or_generate_matrix(N):
    try:
        return np.loadtxt("matrix_data.txt", dtype=int)
    except OSError:
        return np.random.randint(-10, 11, (N, N))

def process_matrix(A):
    N, h = A.shape[0], A.shape[0] // 2
    E, B, D, C = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    F = A.copy()
    perimeter_sum = np.sum(C[0]) + np.sum(C[-1]) + np.sum(C[:, 0]) + np.sum(C[:, -1]) - C[0, 0] - C[0, -1] - C[-1, 0] - C[-1, -1]
    if np.count_nonzero(C[:, 1::2] == 0) > perimeter_sum:
        F[:h, h:], F[h:, h:] = F[h:, h:].copy(), F[:h, h:].copy()
    else:
        F[:h, :h], F[h:, h:] = F[h:, h:], F[:h, :h]
    return F

def plot_graphs(F):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(F, cmap='coolwarm', interpolation='none')
    plt.colorbar()
    plt.title("Тепловая карта F")
    plt.subplot(1, 3, 2)
    plt.plot(F.mean(axis=0), marker='o')
    plt.title("Среднее значение по столбцам")
    plt.subplot(1, 3, 3)
    plt.hist(F.flatten(), bins=20, color='skyblue', edgecolor='black')
    plt.title("Гистограмма значений F")
    plt.tight_layout()
    plt.show()

def main():
    K, N = int(input("Введите K: ")), int(input("Введите N: "))
    A, F, G = load_or_generate_matrix(N), None, None
    F, G = process_matrix(A), np.tril(A)
    det_A, det_F = np.linalg.det(A), np.linalg.det(F)
    result = (np.linalg.inv(A) @ A.T - K * np.linalg.inv(F)) if det_A > np.trace(F) + np.trace(np.fliplr(F)) else (A + np.linalg.inv(G) - np.linalg.inv(F)) * K if det_A != 0 and det_F != 0 else "Не удалось вычислить выражение: A или F вырождены"
    print("Матрица A:\n", A, "\nМатрица F:\n", F, "\nРезультат:\n", result)
    plot_graphs(F)

if __name__ == "__main__":
    main()
