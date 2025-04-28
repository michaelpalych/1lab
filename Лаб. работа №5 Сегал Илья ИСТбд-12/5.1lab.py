import timeit
from itertools import product

def algorithmic_method(P, B, U, Pl): #алгоритмический способ
    groups = [(P, B, U), (P, Pl), (B, Pl), (P, U), (B, U)]
    return ([t for g in groups for t in ([(p, b, u) for p in g[0] for b in g[1] for u in g[2]] if len(g) == 3 else [(x, y) for x in g[0] for y in g[1]])] +
            [(pl,) for pl in Pl])

def python_method(P, B, U, Pl): #метод через itertools
    groups = [(P, B, U), (P, Pl), (B, Pl), (P, U), (B, U)]
    outfits = [outfit for group in groups for outfit in product(*group)]
    outfits += [(pl,) for pl in Pl]
    return outfits

# данные на вход
P, B, U, Pl = ['Пиджак1'], ['Блузка1', 'Блузка2'], ['Юбка1', 'Юбка2'], ['Платье1', 'Платье2', 'Платье3']

# 5.1 вывод всех нарядов
all_outfits = algorithmic_method(P, B, U, Pl)
print(f"5.1 Алгоритмический метод: всего {len(all_outfits)} нарядов")
for i, outfit in enumerate(all_outfits[:12], 1):
    print(f"{i}) {' + '.join(outfit)}")

all_outfits_itertools = python_method(P, B, U, Pl)
print(f"\n5.1 Метод с itertools: всего {len(all_outfits_itertools)} нарядов")
for i, outfit in enumerate(all_outfits_itertools[:12], 1):
    print(f"{i}) {' + '.join(outfit)}")

# сравнение скорости
time_algo = timeit.timeit(lambda: algorithmic_method(P, B, U, Pl), number=10)
time_py = timeit.timeit(lambda: python_method(P, B, U, Pl), number=10)
print(f"Алгоритмический метод: {time_algo:.6f} секунд")
print(f"Метод с itertools: {time_py:.6f} секунд")
print("Быстрее:", "алгоритмический метод" if time_algo < time_py else "метод itertools")

# 5.2 усложнение: не более одного элемента одежды верха
def optimized_method(P, B, U, Pl): 
    outfits = python_method(P, B, U, Pl)
    return [o for o in outfits if sum('Пиджак' in item or 'Блузка' in item for item in o) <= 1]

optimal_outfits = optimized_method(P, B, U, Pl)
print(f"\n5.2 Оптимизированные наряды (не более 1 предмета верха): {len(optimal_outfits)} нарядов")
for i, outfit in enumerate(optimal_outfits, 1):
    print(f"{i}) {' + '.join(outfit)}")
