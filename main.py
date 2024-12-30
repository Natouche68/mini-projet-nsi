import tkinter as tk

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")

arrow_number = tk.IntVar(value=9)
is_trispot = tk.BooleanVar(value=False)


def home():
    def start():
        home_frame.destroy()
        overview()

    home_frame = tk.Frame(window)
    home_frame.pack()

    arrow_number_label = tk.Label(home_frame, text="Nombre de flèches :")
    arrow_number_label.pack()
    arrow_number_entry = tk.Spinbox(
        home_frame, from_=1, to=30, increment=1, textvariable=arrow_number)
    arrow_number_entry.pack()

    is_trispot_entry = tk.Checkbutton(
        home_frame, text="Sur trispot", variable=is_trispot)
    is_trispot_entry.pack()

    validate_button = tk.Button(home_frame, text="Commencer", command=start)
    validate_button.pack()


def overview():
    def small_target(i):
        canvas = tk.Canvas(target_frame, width=100, height=100)
        canvas.grid(row=i//3, column=i % 3, padx=10, pady=10)

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

        canvas.bind("<Button-1>", lambda event: print(i))

    overview_frame = tk.Frame(window)
    overview_frame.pack()

    arrow_number_label = tk.Label(
        overview_frame, text="Nombre de flèches : " + str(arrow_number.get()))
    arrow_number_label.pack()

    target_frame = tk.Frame(overview_frame)
    target_frame.pack()
    for i in range(arrow_number.get()):
        small_target(i)


home()
window.mainloop()
