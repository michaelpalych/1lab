import tkinter as tk
from itertools import product

def generate_all_outfits(P, B, U, Pl):
    groups = [(P, B, U), (P, Pl), (B, Pl), (P, U), (B, U)]
    outfits = [outfit for group in groups for outfit in product(*group)]
    outfits += [(pl,) for pl in Pl]
    return outfits

def optimized_outfits(P, B, U, Pl, max_tops):
    outfits = generate_all_outfits(P, B, U, Pl)
    return [o for o in outfits if sum('Пиджак' in item or 'Блузка' in item for item in o) <= max_tops]

# Функция обработки кнопки
def generate():
    try:
        num_ubok = int(entry_ubok.get())
        num_pidjakov = int(entry_pidjakov.get())
        max_tops = int(entry_tops.get())
        if num_ubok <= 0 or num_pidjakov <= 0 or max_tops <= 0:
            raise ValueError
    except ValueError:
        result_label.config(text="Введите корректные положительные числа!")
        return

    # формируем новые списки
    P = [f'Пиджак{i+1}' for i in range(num_pidjakov)]
    B = ['Блузка1', 'Блузка2']  # блузки константа
    U = [f'Юбка{i+1}' for i in range(num_ubok)]
    Pl = ['Платье1', 'Платье2', 'Платье3']  # платья константа

    outfits = optimized_outfits(P, B, U, Pl, max_tops)

    output_text.delete(1.0, tk.END)
    for i, outfit in enumerate(outfits, 1):
        output_text.insert(tk.END, f"{i}) {' + '.join(outfit)}\n")
    result_label.config(text=f"Найдено нарядов: {len(outfits)}")

### НАЧАЛО TKINTER

# интерфейс
root = tk.Tk()
root.title("Оптимизированный генератор нарядов (5.2)")

# блок ввода
frame_input = tk.Frame(root)
frame_input.pack(pady=5)

# поле для количества юбок
tk.Label(frame_input, text="Количество юбок:").grid(row=0, column=0, padx=5, pady=5)
entry_ubok = tk.Entry(frame_input, width=5)
entry_ubok.grid(row=0, column=1, padx=5)

# поле для количества пиджаков
tk.Label(frame_input, text="Количество пиджаков:").grid(row=1, column=0, padx=5, pady=5)
entry_pidjakov = tk.Entry(frame_input, width=5)
entry_pidjakov.grid(row=1, column=1, padx=5)

# поле для ограничения на предметы верха
tk.Label(frame_input, text="Макс. предметов верха:").grid(row=2, column=0, padx=5, pady=5)
entry_tops = tk.Entry(frame_input, width=5)
entry_tops.grid(row=2, column=1, padx=5)

# кнопка генерации
generate_button = tk.Button(root, text="Сгенерировать наряды", command=generate)
generate_button.pack(pady=5)

# вывод со скроллингом
frame_output = tk.Frame(root)
frame_output.pack(pady=5, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame_output)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text = tk.Text(frame_output, height=15, width=60, yscrollcommand=scrollbar.set)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=output_text.yview)

# текстовое поле снизу для результата
result_label = tk.Label(root, text="Найдено нарядов: 0")
result_label.pack(pady=5)

root.mainloop()
