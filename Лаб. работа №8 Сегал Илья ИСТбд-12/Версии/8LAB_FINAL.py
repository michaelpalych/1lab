import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import csv
from collections import Counter

class Booking:
    def __init__(self, guest_name, room_type, days):
        self.guest_name = guest_name
        self.room_type = room_type
        self.days = int(days)

    @staticmethod
    def from_list(data):
        name, room, days = data
        days = int(days)
        if days < 1:
            raise ValueError
        return Booking(name, room, days)

class BookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление бронями")
        self.bookings = []
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_by_name())
        self.build_gui()

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)
        tk.Button(frame, text="Загрузить из файла", command=self.load_bookings).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Сохранить в файл", command=self.save_to_file).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Удалить бронь", command=self.delete_booking).grid(row=0, column=2, padx=5)
        tk.Entry(frame, textvariable=self.search_var, width=20).grid(row=0, column=3, padx=(20,5))
        tk.Button(frame, text="Поиск", command=self.search_by_name).grid(row=0, column=4, padx=5)

        table_frame = tk.Frame(frame)
        table_frame.grid(row=1, column=0, columnspan=5, pady=10)
        self.tree = ttk.Treeview(table_frame, columns=("ФИО","Тип номера","Дней"), show='headings', height=12)
        for col, width in [("ФИО",150),("Тип номера",100),("Дней",60)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')
        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='y')
        vsb.pack(side='left', fill='y')
        self.tree.bind('<Double-1>', self.on_double_click)

        tk.Button(frame, text="Сегментация по сроку", width=18, command=self.segment_by_days)\
          .grid(row=2, column=0, sticky='e', pady=5, padx=(0,10))
        tk.Button(frame, text="Сегментация по типу", width=18, command=self.segment_by_room)\
          .grid(row=2, column=4, sticky='w', pady=5, padx=(10,0))

        self.canvas = tk.Canvas(self.root, width=900, height=600, bg="white")
        self.canvas.pack(pady=10)

    def load_bookings(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if not path: return
        try:
            with open(path, encoding='utf-8') as f:
                self.bookings = [Booking.from_list(row) for row in csv.reader(f)]
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        else:
            self.refresh_tree()

    def save_to_file(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files","*.csv")])
        if not path: return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for b in self.bookings:
                writer.writerow((b.guest_name, b.room_type, b.days))
        messagebox.showinfo("Сохранено", "Данные сохранены!")

    def delete_booking(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Удаление", "Выберите запись.")
            return
        idx = self.tree.index(sel[0])
        if messagebox.askyesno("Удалить?", "Удалить выбранную бронь?"):
            del self.bookings[idx]
            self.refresh_tree()

    def search_by_name(self):
        term = self.search_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for b in self.bookings:
            if term in b.guest_name.lower():
                self.tree.insert('', 'end', values=(b.guest_name, b.room_type, b.days))

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y); col = self.tree.identify_column(event.x)
        if not item or not col: return
        idx = self.tree.index(item); ci = int(col.replace('#','')) - 1
        old = self.tree.item(item, 'values')[ci]
        if ci == 2:
            new = simpledialog.askinteger("Изменить", "Число дней:", initialvalue=old, minvalue=1)
        else:
            new = simpledialog.askstring("Изменить", "Новое значение:", initialvalue=old)
        if new is None: return
        if ci == 0: self.bookings[idx].guest_name = new
        elif ci == 1: self.bookings[idx].room_type = new
        else: self.bookings[idx].days = int(new)
        self.tree.set(item, column=col, value=new)

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for b in self.bookings:
            self.tree.insert('', 'end', values=(b.guest_name, b.room_type, b.days))

    def segment_by_days(self):
        counts = Counter(b.days for b in self.bookings)
        self._draw_pie(counts, "Сегментация по срокам", lambda d: f"{d} дней",
                       ["#ff9999","#ffb74d","#fff176","#aed581","#4dd0e1","#ba68c8","#90caf9"])

    def segment_by_room(self):
        counts = Counter(b.room_type for b in self.bookings)
        self._draw_pie(counts, "Сегментация по типам", lambda t: t,
                       ["#e57373","#64b5f6","#81c784","#ffd54f","#9575cd"])

    def _draw_pie(self, counts, title, label_func, palette):
        self.canvas.delete('all')
        total = sum(counts.values()); 
        if total == 0: return
        cx, cy, r = 450, 320, min(900,600)/2 - 100
        self.canvas.create_text(cx, 40, text=title, font=("Arial",16,"bold"))
        start = 0; items = list(counts.items())
        for i, (key, cnt) in enumerate(items):
            extent = 360 * cnt / total
            arc = self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=start, extent=extent,
                                         fill=palette[i % len(palette)], outline='white', width=2)
            self.canvas.tag_bind(arc, '<Button-1>',
                lambda e, k=key, c=cnt: messagebox.showinfo('Сегмент',
                    f"{label_func(k)}: {c} ({c/total*100:.1f}%)"))
            start += extent
        lx, ly = cx + r + 40, cy - r
        for i, (key, cnt) in enumerate(items):
            y = ly + i * 30
            self.canvas.create_rectangle(lx, y, lx+20, y+15,
                                         fill=palette[i % len(palette)], outline='black')
            self.canvas.create_text(lx+25, y+7,
                text=f"{label_func(key)}: {cnt} ({cnt/total*100:.1f}%)",
                anchor='w', font=("Arial",12))

if __name__ == "__main__":
    root = tk.Tk()
    BookingApp(root)
    root.mainloop()
