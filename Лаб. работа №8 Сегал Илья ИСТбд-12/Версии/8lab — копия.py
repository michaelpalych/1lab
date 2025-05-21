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

        tk.Button(frame, text="Загрузить из файла", command=self.load_bookings).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Сохранить в файл", command=self.save_bookings).grid(row=0, column=1, padx=5)

        self.tree = ttk.Treeview(frame, columns=("ФИО","Тип номера","Дней"), show='headings')
        for col, w in [("ФИО",150),("Тип номера",100),("Дней",60)]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor='center')
        self.tree.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Сегментация по сроку", command=self.segment_by_days).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Сегментация по типу", command=self.segment_by_room).grid(row=2, column=1, pady=5)

        # Увеличенный холст для диаграммы
        self.canvas_width = 900  # увеличена ширина холста для легенды и процентов
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)

    def load_bookings(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files","*.csv"),("All files","*.*")])
        if not file: return
        with open(file, encoding='utf-8') as f:
            reader = csv.reader(f)
            bookings = []
            for row in reader:
                try:
                    bookings.append(Booking.from_list(row))
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))
                    return
        self.bookings = bookings
        self.refresh_tree()

    def save_bookings(self):
        file = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files","*.csv")])
        if not file: return
        with open(file,'w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            for b in self.bookings:
                writer.writerow([b.guest_name,b.room_type,b.days])
        messagebox.showinfo("Сохранено","Данные сохранены!")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for b in self.bookings:
            self.tree.insert('','end',values=(b.guest_name,b.room_type,b.days))

    def segment_by_days(self):
        counts = Counter(b.days for b in self.bookings)
        self.draw_pie_days(counts)

    def segment_by_room(self):
        counts = Counter(b.room_type for b in self.bookings)
        self.draw_pie_generic(counts, "Сегментация по типам")

    def draw_pie_generic(self, counts, title):
        self.canvas.delete('all')
        total = sum(counts.values())
        if total == 0: return
        # Заголовок
        cx = self.canvas_width/2
        self.canvas.create_text(cx, 40, text=title, font=("Arial",16,"bold"))
        # Параметры круга
        cy = self.canvas_height/2 + 20
        r = min(self.canvas_width, self.canvas_height)/2 - 100
        palette = ["#e57373","#64b5f6","#81c784","#ffd54f","#9575cd"]
        items = list(counts.items())
        start = 0
        # рисуем секторы с интерактивом
        for i,(label,cnt) in enumerate(items):
            extent = 360*cnt/total
            color = palette[i%len(palette)]
            arc = self.canvas.create_arc(cx-r,cy-r,cx+r,cy+r,
                                         start=start,extent=extent,fill=color,outline='white',width=2)
            # hover effect
            self.canvas.tag_bind(arc, '<Enter>', lambda e,a=arc: self.canvas.itemconfig(a, width=4))
            self.canvas.tag_bind(arc, '<Leave>', lambda e,a=arc: self.canvas.itemconfig(a, width=2))
            self.canvas.tag_bind(arc, '<Button-1>', lambda e,l=label,c=cnt: messagebox.showinfo('Сегмент', f"{l}: {cnt} ({cnt/total*100:.1f}%)"))
            start += extent
        # легенда справа с процентом
        lx = cx + r + 40
        ly = cy - r
        for i,(label,cnt) in enumerate(items):
            y = ly + i*30
            color = palette[i%len(palette)]
            self.canvas.create_rectangle(lx,y,lx+20,y+15,fill=color,outline='black')
            self.canvas.create_text(lx+25,y+7,text=f"{label}: {cnt} ({cnt/total*100:.1f}%)",anchor='w',font=("Arial",12))

    def draw_pie_days(self, counts):
        self.canvas.delete('all')
        total = sum(counts.values())
        if total == 0: return
        # склонение
        def word(n): return "день" if n%10==1 and n%100!=11 else "дня" if n%10 in (2,3,4) and not(12<=n%100<=14) else "дней"
        title = "Сегментация по срокам"
        cx = self.canvas_width/2
        self.canvas.create_text(cx, 40, text=title, font=("Arial",16,"bold"))
        cy = self.canvas_height/2 + 20
        r = min(self.canvas_width, self.canvas_height)/2 - 100
        palette = ["#ff9999","#ffb74d","#fff176","#aed581","#4dd0e1","#ba68c8","#90caf9"]
        items = sorted(counts.items())
        start = 0
        # рисуем сектора с интерактивом
        for i,(day,cnt) in enumerate(items):
            extent = 360*cnt/total
            color = palette[i%len(palette)]
            arc = self.canvas.create_arc(cx-r,cy-r,cx+r,cy+r,
                                         start=start,extent=extent,fill=color,outline='white',width=2)
            self.canvas.tag_bind(arc, '<Enter>', lambda e,a=arc: self.canvas.itemconfig(a, width=4))
            self.canvas.tag_bind(arc, '<Leave>', lambda e,a=arc: self.canvas.itemconfig(a, width=2))
            self.canvas.tag_bind(arc, '<Button-1>', lambda e,d=day,c=cnt: messagebox.showinfo('Срок', f"{day} {word(day)}: {cnt} ({cnt/total*100:.1f}%)"))
            start += extent
        # легенда справа с процентом и склонением
        lx = cx + r + 40
        ly = cy - r
        for i,(day,cnt) in enumerate(items):
            y = ly + i*30
            color = palette[i%len(palette)]
            self.canvas.create_rectangle(lx,y,lx+20,y+15,fill=color,outline='black')
            self.canvas.create_text(lx+25,y+7,text=f"{day} {word(day)}: {cnt} ({cnt/total*100:.1f}%)",anchor='w',font=("Arial",12))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
