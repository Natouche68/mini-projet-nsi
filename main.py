import tkinter as tk
from tkinter import ttk
import math

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")
window.minsize(800,500)
window.maxsize(800,500)

arrow_number = tk.IntVar(value=9)
is_trispot = tk.BooleanVar(value=False)
arrows_coordinates = []
current_volley = 1
arc=tk.PhotoImage(file='arc_accueil.png')
window.wm_attributes("-transparentcolor", "orange")

def home():
    def start():
        for _ in range(arrow_number.get()):
            arrows_coordinates.append([])
        home_frame.destroy()
        can1.destroy()
        overview()

    can1=tk.Canvas(window, width=800, height=500)
    can1.create_image(400,250,image=arc)
    can1.place(x=0,y=0)
    home_frame = ttk.Frame(window)
    home_frame.pack(pady=(10,0))

    title_label = ttk.Label(home_frame, text="Trieur de flèches", font=("Segoe UI", 32))
    title_label.pack(padx=10,pady=5)

    arrow_number_label = ttk.Label(home_frame, text="Nombre de flèches :")
    arrow_number_label.pack()
    arrow_number_entry = ttk.Spinbox(home_frame, from_=1, to=30, increment=1, textvariable=arrow_number)
    arrow_number_entry.pack(pady=(5,0))

    is_trispot_entry = ttk.Checkbutton(home_frame, text="Sur trispot", variable=is_trispot)
    is_trispot_entry.pack()

    validate_button = ttk.Button(home_frame, text="Commencer", command=start)
    validate_button.pack(pady=(0,10))

def overview():
    def is_target_complete(target_number):
        return len(arrows_coordinates[target_number]) == current_volley

    def open_target(target_number):
        if len(arrows_coordinates[target_number]) < current_volley:
            overview_frame.destroy()
            add_impact(target_number)

    def on_target_click(event, scroll_bar_offset):
        target_number = int(((event.y + scroll_bar_offset) // 120) * 3 + (event.x // 120))
        open_target(target_number)

    def small_target(target_number):
        xPos = (target_number % 3) * 120 + 10
        yPos = (target_number // 3) * 120 + 10

        if is_trispot.get():
            target_canvas.create_oval(xPos+2, yPos+2, xPos+98, yPos+98, fill="blue")
            target_canvas.create_oval(xPos+11, yPos+11, xPos+89, yPos+89, fill="red")
            target_canvas.create_oval(xPos+20, yPos+20, xPos+80, yPos+80, fill="red")
            target_canvas.create_oval(xPos+30, yPos+30, xPos+70, yPos+70, fill="yellow")
            target_canvas.create_oval(xPos+40, yPos+40, xPos+60, yPos+60, fill="yellow")
        else:
            target_canvas.create_oval(xPos+2, yPos+2, xPos+98, yPos+98, fill="white")
            target_canvas.create_oval(xPos+11, yPos+11, xPos+89, yPos+89, fill="black")
            target_canvas.create_oval(xPos+20, yPos+20, xPos+80, yPos+80, fill="blue")
            target_canvas.create_oval(xPos+30, yPos+30, xPos+70, yPos+70, fill="red")
            target_canvas.create_oval(xPos+40, yPos+40, xPos+60, yPos+60, fill="yellow")
        
        for x, y in arrows_coordinates[target_number]:
            target_canvas.create_oval(xPos+x-2, yPos+y-2, xPos+x+2, yPos+y+2, fill="green", outline="green")

        if is_target_complete(target_number):
            target_canvas.create_oval(xPos+2, yPos+2, xPos+98, yPos+98, fill="#C6C6C6")
            target_canvas.create_text(xPos+50, yPos+49, text="✔️", font=("Segoe UI Emoji", 16))
        else:
            target_canvas.create_text(xPos+50, yPos+49, text=str(target_number+1), font=("Segoe UI", 16))
    
    def is_finish_button_active():
        coordinates_length = len(arrows_coordinates[0])
        for arrow in arrows_coordinates:
            if len(arrow) != coordinates_length:
                return False
        if coordinates_length == 0:
            return False
        return True

    def on_finish_click():
        if not is_finish_button_active():
            return
        overview_frame.destroy()
        stats()
    
    overview_frame = ttk.Frame(window)
    overview_frame.pack(fill="both")

    menu_bar = tk.Frame(overview_frame, bg="#3ED8FF")
    menu_bar.pack(fill="x")
    menu_bar_content = tk.Frame(menu_bar, bg="#3ED8FF")
    menu_bar_content.pack(anchor='center')

    arrow_number_label = tk.Label(menu_bar_content, text="Nombre de flèches : " + str(arrow_number.get()), bg="#3ED8FF")
    arrow_number_label.grid(row=0,column=0)

    current_volley_label = tk.Label(menu_bar_content, text="Volée n°" + str(current_volley), bg="#3ED8FF")
    current_volley_label.grid(row=0,column=1, padx=40, pady=10)

    target_frame_container = tk.Frame(overview_frame)
    target_frame_container.pack(fill="both")
    scroll_bar = ttk.Scrollbar(target_frame_container, orient="vertical")
    scroll_bar.pack(side="right", fill="y")
    target_canvas_height = math.ceil(arrow_number.get() / 3) * 120
    target_canvas = tk.Canvas(
        target_frame_container,
        width=360,
        height=target_canvas_height,
        yscrollcommand=scroll_bar.set,
        scrollregion="0 0 360 " + str(target_canvas_height)
    )
    target_canvas.pack()
    scroll_bar.config(command=target_canvas.yview)
    for i in range(arrow_number.get()):
        small_target(i)
    target_canvas.bind("<Button-1>", lambda event: on_target_click(event, scroll_bar.get()[0]*target_canvas_height))

    finish_button = tk.Button(menu_bar_content, text="Terminer", command=on_finish_click, state="normal" if is_finish_button_active() else "disabled")
    finish_button.grid(row=0,column=2)

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


def stats():
    def moyenne(list):
        somme_x = 0
        somme_y = 0
        for x, y in list:
            somme_x += x
            somme_y += y
        moyenne_x = somme_x / len(list)
        moyenne_y = somme_y / len(list)
        return (moyenne_x, moyenne_y)

    def ecart_type(list):
        moyenne_list = moyenne(list)
        somme_ecart_carree_x = 0
        somme_ecart_carree_y = 0
        for x, y, in list:
            somme_ecart_carree_x += (x - moyenne_list[0])**2
            somme_ecart_carree_y += (y - moyenne_list[1])**2
        ecart_type_x = math.sqrt(somme_ecart_carree_x / len(list))
        ecart_type_y = math.sqrt(somme_ecart_carree_y / len(list))
        return (ecart_type_x, ecart_type_y)

    stats_frame = ttk.Frame(window)
    stats_frame.pack()

    rows=0
    columns=0

    for i in range(len(arrows_coordinates)):
        arrow_frame = ttk.Frame(stats_frame)
        arrow_frame.grid(row=rows,column=columns)

        arrow_number_label = ttk.Label(
            arrow_frame, text="Flèche n°" + str(i+1))
        arrow_number_label.pack()

        impacts_label = ttk.Label(arrow_frame, text=str(arrows_coordinates[i]))
        impacts_label.pack()

        moyenne_label = ttk.Label(
            arrow_frame, text="Moyenne : " + str(moyenne(arrows_coordinates[i])))
        moyenne_label.pack()

        ecart_type_label = ttk.Label(
            arrow_frame, text="Ecart-tpe : " + str(ecart_type(arrows_coordinates[i])))
        ecart_type_label.pack()

        if rows == 4:
            rows=-1
            columns+=1
        if rows < 4:
            rows+=1


home()
window.mainloop()
