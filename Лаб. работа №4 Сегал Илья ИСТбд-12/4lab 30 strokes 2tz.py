import numpy as np
import matplotlib.pyplot as plt

def get_matrix(N):
    while True:
        if input("Способ (1-файл, 2-случайная): ") == "1":
            try:
                A = np.loadtxt("matrix_data.txt", dtype=int)
            except OSError:
                continue
        else:
            A = np.random.randint(-10, 11, (N, N))
        if np.linalg.det(A) != 0:
            return A

def process_matrix(A):
    N = A.shape[0]
    if N % 2 != 0:
        raise ValueError("N должно быть чётным!")
    h, F = N // 2, A.copy()
    E, B, D, C = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    p = np.sum(C[0]) + np.sum(C[-1]) + np.sum(C[:, 0]) + np.sum(C[:, -1]) - C[0, 0] - C[0, -1] - C[-1, 0] - C[-1, -1]
    if np.count_nonzero(C[:, 1::2] == 0) > p:
        F[:h, h:], F[h:, h:] = F[h:, h:].copy(), F[:h, h:].copy()
    else:
        F[:h, :h], F[h:, h:] = F[h:, h:].copy(), F[:h, :h].copy()
    return F

def plot_graphs(F):
    plt.figure(figsize=(12, 4))
    for i, (d, t) in enumerate(zip([F, F.mean(axis=0), F.flatten()], ["Карта", "Среднее", "Гистограмма"])):
        plt.subplot(1, 3, i+1)
        plt.imshow(d, cmap='coolwarm') if i == 0 else plt.plot(d, '-o') if i == 1 else plt.hist(d, bins=20, color='skyblue')
        plt.title(t)
    plt.show()

def main():
    K, N = int(input("Введите K: ")), int(input("Введите N (чётное): "))
    if N % 2 != 0:
        raise ValueError("N должно быть чётным!")
    A = get_matrix(N)
    F, G = process_matrix(A), np.tril(A)
    det_A, det_F = np.linalg.det(A), np.linalg.det(F)
    inv_A, inv_F, inv_G = np.linalg.inv(A), np.linalg.inv(F) if det_F != 0 else None, np.linalg.inv(G) if np.linalg.det(G) != 0 else None
    if det_A > np.trace(F) + np.trace(np.fliplr(F)):
        result = inv_A @ A.T - K * inv_F if inv_F is not None else "Ошибка"
    else:
        result = (A + inv_G - inv_F) * K if inv_G is not None and inv_F is not None else "Ошибка"
    print("A:\n", A, "\nF:\n", F, "\nРезультат:\n", result)
    plot_graphs(F)

if __name__ == "__main__":
    main()
