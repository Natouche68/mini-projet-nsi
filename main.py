import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")

arrow_number = tk.IntVar(value=9)
is_trispot = tk.BooleanVar(value=False)
arrows_coordinates = []
current_volley = 1


def home():
    def start():
        for _ in range(arrow_number.get()):
            arrows_coordinates.append([])
        home_frame.destroy()
        overview()

    home_frame = ttk.Frame(window)
    home_frame.pack()

    arrow_number_label = ttk.Label(home_frame, text="Nombre de flèches :")
    arrow_number_label.pack()
    arrow_number_entry = ttk.Spinbox(
        home_frame, from_=1, to=30, increment=1, textvariable=arrow_number)
    arrow_number_entry.pack()

    is_trispot_entry = ttk.Checkbutton(
        home_frame, text="Sur trispot", variable=is_trispot)
    is_trispot_entry.pack()

    validate_button = ttk.Button(home_frame, text="Commencer", command=start)
    validate_button.pack()


def overview():
    def open_target(target_number):
        if len(arrows_coordinates[target_number]) < current_volley:
            overview_frame.destroy()
            add_impact(target_number)

    def small_target(target_number):
        canvas = tk.Canvas(target_frame, width=100, height=100)
        canvas.grid(row=target_number//3, column=target_number %
                    3, padx=10, pady=10)

        if is_trispot.get():
            canvas.create_oval(2, 2, 98, 98, fill="blue")
            canvas.create_oval(11, 11, 89, 89, fill="red")
            canvas.create_oval(20, 20, 80, 80, fill="red")
            canvas.create_oval(30, 30, 70, 70, fill="yellow")
            canvas.create_oval(40, 40, 60, 60, fill="yellow")
        else:
            canvas.create_oval(2, 2, 98, 98, fill="white")
            canvas.create_oval(11, 11, 89, 89, fill="black")
            canvas.create_oval(20, 20, 80, 80, fill="blue")
            canvas.create_oval(30, 30, 70, 70, fill="red")
            canvas.create_oval(40, 40, 60, 60, fill="yellow")

        for x, y in arrows_coordinates[target_number]:
            canvas.create_oval(x-2, y-2, x+2, y+2,
                               fill="green", outline="green")

        canvas.bind("<Button-1>", lambda _: open_target(target_number))

    overview_frame = ttk.Frame(window)
    overview_frame.pack()

    arrow_number_label = ttk.Label(
        overview_frame, text="Nombre de flèches : " + str(arrow_number.get()))
    arrow_number_label.pack()

    current_volley_label = ttk.Label(
        overview_frame, text="Volée n°" + str(current_volley))
    current_volley_label.pack()

    target_frame = ttk.Frame(overview_frame)
    target_frame.pack()
    for i in range(arrow_number.get()):
        small_target(i)


def add_impact(target_number):
    def on_click(event):
        global current_volley
        arrows_coordinates[target_number].append((event.x/4, event.y/4))

        new_volley = True
        for arrow in arrows_coordinates:
            if len(arrow) < current_volley:
                new_volley = False
                break
        if new_volley:
            current_volley += 1

        arrow_frame.destroy()
        overview()

    arrow_frame = ttk.Frame(window)
    arrow_frame.pack()

    canvas = tk.Canvas(arrow_frame, width=400, height=400)
    canvas.pack(padx=10, pady=10)

    if is_trispot.get():
        canvas.create_oval(2, 2, 398, 398, fill="blue")
        canvas.create_oval(42, 42, 358, 358, fill="red")
        canvas.create_oval(80, 80, 320, 320, fill="red")
        canvas.create_oval(120, 120, 280, 280, fill="yellow")
        canvas.create_oval(160, 160, 240, 240, fill="yellow")
        canvas.create_oval(180, 180, 220, 220, fill="yellow")
    else:
        canvas.create_oval(2, 2, 398, 398, fill="white")
        canvas.create_oval(21, 21, 379, 379, fill="white")
        canvas.create_oval(40, 40, 360, 360, fill="black")
        canvas.create_oval(60, 60, 340, 340, fill="black", outline="white")
        canvas.create_oval(80, 80, 320, 320, fill="blue")
        canvas.create_oval(100, 100, 300, 300, fill="blue")
        canvas.create_oval(120, 120, 280, 280, fill="red")
        canvas.create_oval(140, 140, 260, 260, fill="red")
        canvas.create_oval(160, 160, 240, 240, fill="yellow")
        canvas.create_oval(180, 180, 220, 220, fill="yellow")
        canvas.create_oval(190, 190, 210, 210, fill="yellow")

    for x, y in arrows_coordinates[target_number]:
        canvas.create_oval(x*4-5, y*4-5, x*4+5, y*4+5,
                           fill="green", outline="green")

    canvas.bind("<Button-1>", on_click)


home()
window.mainloop()
