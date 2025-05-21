import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from collections import Counter
import math

class Booking:
    def __init__(self, guest_name, room_type, days):
        self.guest_name = guest_name
        self.room_type = room_type
        self.days = int(days)

    @staticmethod
    def from_list(data):
        try:
            guest_name, room_type, days = data
            days = int(days)
            if days < 1:
                raise ValueError
            return Booking(guest_name, room_type, days)
        except Exception:
            raise ValueError('Неправильная запись: ' + str(data))

class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление бронями")
        self.bookings = []
        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        btn_load = tk.Button(frame, text="Загрузить из файла", command=self.load_bookings)
        btn_load.grid(row=0, column=0, padx=5, pady=5)
        
        btn_save = tk.Button(frame, text="Сохранить в файл", command=self.save_bookings)
        btn_save.grid(row=0, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(frame, columns=("ФИО", "Тип номера", "Дней"), show='headings')
        self.tree.heading("ФИО", text="ФИО")
        self.tree.heading("Тип номера", text="Тип номера")
        self.tree.heading("Дней", text="Дней")
        self.tree.grid(row=1, column=0, columnspan=2, pady=10)

        btn_seg1 = tk.Button(frame, text="Сегментация по сроку", command=self.segment_by_days)
        btn_seg1.grid(row=2, column=0, pady=5)
        btn_seg2 = tk.Button(frame, text="Сегментация по типу", command=self.segment_by_room)
        btn_seg2.grid(row=2, column=1, pady=5)

        self.canvas = tk.Canvas(self.root, width=320, height=320, bg="white")
        self.canvas.pack(pady=10)

    def load_bookings(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"),("All files", "*.*")])
        if not file: return
        bookings = []
        with open(file, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    booking = Booking.from_list(row)
                    bookings.append(booking)
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                    return
        self.bookings = bookings
        self.refresh_tree()

    def save_bookings(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file: return
        with open(file, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for b in self.bookings:
                writer.writerow([b.guest_name, b.room_type, b.days])
        messagebox.showinfo("Сохранено", "Данные сохранены!")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.bookings:
            self.tree.insert("", "end", values=(b.guest_name, b.room_type, b.days))

    def segment_by_days(self):
        if not self.bookings:
            messagebox.showinfo("Нет данных", "Сначала загрузите брони")
            return
        data = [b.days for b in self.bookings]
        counts = Counter(data)
        self.draw_pie_chart(counts, "Сегментация по срокам")

    def segment_by_room(self):
        if not self.bookings:
            messagebox.showinfo("Нет данных", "Сначала загрузите брони")
            return
        data = [b.room_type for b in self.bookings]
        counts = Counter(data)
        self.draw_pie_chart(counts, "Сегментация по типам")

    def draw_pie_chart(self, counts, title):
        self.canvas.delete("all")
        total = sum(counts.values())
        if total == 0: return
        colors = ["#ff9999","#66b3ff","#99ff99","#ffcc99","#c2c2f0","#ffb3e6","#c2f0c2"]
        start = 0
        cx, cy, r = 160, 160, 120
        i = 0
        for label, count in counts.items():
            extent = 360 * count / total
            color = colors[i % len(colors)]
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent, fill=color, outline="black")
            angle = math.radians(start + extent / 2)
            x = cx + math.cos(angle) * (r + 20)
            y = cy + math.sin(angle) * (r + 20)
            self.canvas.create_text(x, y, text=f"{label}: {count}", font=("Arial", 10, "bold"))
            start += extent
            i += 1
        self.canvas.create_text(cx, 20, text=title, font=("Arial", 14, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
