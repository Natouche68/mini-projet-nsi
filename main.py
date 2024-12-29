import tkinter as tk

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")


def home():
    def start():
        home_frame.destroy()

    home_frame = tk.Frame(window)
    home_frame.pack()

    arrow_number_label = tk.Label(home_frame, text="Nombre de flèches :")
    arrow_number_label.pack()
    arrow_number_entry = tk.Spinbox(
        home_frame, from_=1, to=30, increment=1, textvariable=tk.IntVar(value=9))
    arrow_number_entry.pack()

    is_trispot_entry = tk.Checkbutton(home_frame, text="Sur trispot")
    is_trispot_entry.pack()

    validate_button = tk.Button(home_frame, text="Commencer", command=start)
    validate_button.pack()


home()

window.mainloop()
