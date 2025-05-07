import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import json
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import random as rdm

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")
window.minsize(800, 500)
window.maxsize(800, 500)

name = tk.StringVar(value="")
arrow_number = tk.IntVar(value=9)
is_trispot = tk.BooleanVar(value=False)
arrows_coordinates = []
current_volley = 1
overview_scroll_position = 0
arc_img = tk.PhotoImage(file='arc_accueil.png')


def home():
    global arrows_coordinates, current_volley, overview_scroll_position

    # Init base values to avoid conflicts
    name.set("")
    arrow_number.set(9)
    arrows_coordinates = []
    current_volley = 1
    overview_scroll_position = 0

    # On validate_buttin click
    # Start a new session
    def start():
        if arrow_number.get() <= 0 or name.get() == "":
            return

        for _ in range(arrow_number.get()):
            arrows_coordinates.append([])
        home_frame.destroy()
        can.destroy()
        overview()

    # On load_button click
    # Load the stats from a data/*.json file
    def load_file(file_name):
        global arrows_coordinates

        with open("data/" + str(file_name) + ".json", "r") as file:
            arrows_coordinates = json.load(file)
            name.set(file_name)
            arrow_number.set(len(arrows_coordinates))

            home_frame.destroy()
            can.destroy()
            stats()
    
    # On delete_button click
    # Delete the given file
    def delete_file(file_name):
        if messagebox.askokcancel(title="Supprimer un tri", message="Etes-vous sûr(e) de vouloir supprimer le tri " + str(file_name) + " ?"):
            os.remove("data/" + str(file_name) + ".json")

            # Re-render the home page
            home_frame.destroy()
            can.destroy()
            home()

    # Home menu
    can = tk.Canvas(window, width=800, height=500)
    can.create_image(400, 250, image=arc_img)
    can.place(x=0, y=0)
    home_frame = ttk.Frame(window)
    home_frame.pack(pady=10)

    title_label = ttk.Label(
        home_frame, text="Trieur de flèches", font=("Segoe UI", 32))
    title_label.pack(padx=10, pady=5)

    name_label = ttk.Label(home_frame, text="Nom du tri :")
    name_label.pack()
    name_entry = ttk.Entry(home_frame, textvariable=name)
    name_entry.pack(pady=(5, 0))

    arrow_number_label = ttk.Label(home_frame, text="Nombre de flèches :")
    arrow_number_label.pack()
    arrow_number_entry = ttk.Spinbox(
        home_frame, from_=1, to=30, increment=1, textvariable=arrow_number)
    arrow_number_entry.pack(pady=(5, 0))

    is_trispot_entry = ttk.Checkbutton(
        home_frame, text="Sur trispot", variable=is_trispot)
    is_trispot_entry.pack()

    validate_button = ttk.Button(home_frame, text="Commencer", command=start)
    validate_button.pack(pady=(0, 10))

    # Get existing data
    files = [file.replace(".json", "")
             for file in os.listdir("data/") if ".json" in file]

    # Menu for loading data
    load_title = ttk.Label(
        home_frame, text="Ouvrir un tri précédent", font=("Segoe UI", 16))
    load_title.pack(pady=10)

    load_buttons = ttk.Frame(home_frame)
    load_buttons.pack(pady=4)

    for i in range(len(files)):
        load_button = ttk.Button(
            load_buttons, text=files[i], command=lambda f=files[i]: load_file(f), width=32)
        load_button.grid(row=i, column=0)

        delete_button = ttk.Button(load_buttons, text="❌", command=lambda f=files[i]: delete_file(f), width=4)
        delete_button.grid(row=i, column=1)


def overview():
    # Check if an impact has been set for a given arrow during the current volley
    def is_target_complete(target_number):
        return len(arrows_coordinates[target_number]) == current_volley

    # Open the "add impact" menu for a given arrow
    def open_target(target_number):
        global overview_scroll_position

        if len(arrows_coordinates[target_number]) < current_volley:
            overview_scroll_position = scroll_bar.get()[0]
            overview_frame.destroy()
            add_impact(target_number)

    # On target_canvas click
    # Get the number of the arrow corresponding to the click 
    def on_target_click(event, scroll_bar_offset):
        target_number = int(
            ((event.y + scroll_bar_offset) // 120) * 3 + (event.x // 120))
        open_target(target_number)

    # Draw a small arrow that can be clicked
    def small_target(target_number):
        xPos = (target_number % 3) * 120 + 10
        yPos = (target_number // 3) * 120 + 10

        if is_trispot.get():
            target_canvas.create_oval(
                xPos+2, yPos+2, xPos+98, yPos+98, fill="blue")
            target_canvas.create_oval(
                xPos+11, yPos+11, xPos+89, yPos+89, fill="red")
            target_canvas.create_oval(
                xPos+20, yPos+20, xPos+80, yPos+80, fill="red")
            target_canvas.create_oval(
                xPos+30, yPos+30, xPos+70, yPos+70, fill="yellow")
            target_canvas.create_oval(
                xPos+40, yPos+40, xPos+60, yPos+60, fill="yellow")
        else:
            target_canvas.create_oval(
                xPos+2, yPos+2, xPos+98, yPos+98, fill="white")
            target_canvas.create_oval(
                xPos+11, yPos+11, xPos+89, yPos+89, fill="black")
            target_canvas.create_oval(
                xPos+20, yPos+20, xPos+80, yPos+80, fill="blue")
            target_canvas.create_oval(
                xPos+30, yPos+30, xPos+70, yPos+70, fill="red")
            target_canvas.create_oval(
                xPos+40, yPos+40, xPos+60, yPos+60, fill="yellow")

        for x, y in arrows_coordinates[target_number]:
            target_canvas.create_oval(
                xPos+x-2, yPos+y-2, xPos+x+2, yPos+y+2, fill="#00C700", outline="#00C700")

        if is_target_complete(target_number):
            target_canvas.create_oval(
                xPos+2, yPos+2, xPos+98, yPos+98, fill="#C6C6C6")
            target_canvas.create_text(
                xPos+50, yPos+49, text="✔️", font=("Segoe UI Emoji", 16))
        else:
            target_canvas.create_text(
                xPos+50, yPos+49, text=str(target_number+1), font=("Segoe UI", 16))

    # Check if the finish_button can be clicked
    # (if the current volley is completed and if at least one has been set) 
    def is_finish_button_active():
        coordinates_length = len(arrows_coordinates[0])
        for arrow in arrows_coordinates:
            if len(arrow) != coordinates_length:
                return False
        if coordinates_length == 0:
            return False
        return True

    # Show the stats menu
    def on_finish_click():
        if not is_finish_button_active():
            return
        overview_frame.destroy()
        stats()

    # Enables the user to scroll using the mouse wheel
    def on_scroll(event):
        target_canvas.yview_scroll(int(-event.delta / 120), "units")

    overview_frame = ttk.Frame(window)
    overview_frame.pack(fill="both")

    menu_bar = tk.Frame(overview_frame, bg="#3ED8FF")
    menu_bar.pack(fill="x")
    menu_bar_content = tk.Frame(menu_bar, bg="#3ED8FF")
    menu_bar_content.pack()

    name_label = tk.Label(menu_bar_content, text=name.get(),
                          bg="#3ED8FF", font=("Segoe UI", 10, "bold"))
    name_label.grid(row=0, column=0, padx=40, pady=10)

    arrow_number_label = tk.Label(
        menu_bar_content, text="Nombre de flèches : " + str(arrow_number.get()), bg="#3ED8FF")
    arrow_number_label.grid(row=0, column=1)

    current_volley_label = tk.Label(
        menu_bar_content, text="Volée n°" + str(current_volley), bg="#3ED8FF")
    current_volley_label.grid(row=0, column=2, padx=40)

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
    target_canvas.yview_moveto(overview_scroll_position)
    target_canvas.bind_all("<MouseWheel>", on_scroll)

    for i in range(arrow_number.get()):
        small_target(i)
    target_canvas.bind("<Button-1>", lambda event: on_target_click(event,
                       scroll_bar.get()[0]*target_canvas_height))

    finish_button = tk.Button(menu_bar_content, text="Terminer", command=on_finish_click,
                              state="normal" if is_finish_button_active() else "disabled")
    finish_button.grid(row=0, column=3)

    # Autofill 2 volleys for each arrow (for testing purposes)
    def autofill():
        global arrows_coordinates
        global arrow_number
        for i in range(arrow_number.get()):
            list1=[rdm.randint(0,100),rdm.randint(0,100)]
            list2=[rdm.randint(0,100),rdm.randint(0,100)]
            arrows_coordinates[i].append(list1)
            arrows_coordinates[i].append(list2)
        stats()
        overview_frame.destroy()

    autofill_button = tk.Button(menu_bar_content, text='Rempli. aléat.', bg='#3ED8FF', command=lambda : autofill())
    autofill_button.grid(row=0,column=4,padx=40)

def add_impact(target_number):
    global impact_to_add
    impact_to_add = [None, None]

    # Update the impact_to_add according to the click
    def on_target_click(event):
        global impact_to_add
        impact_to_add = [(event.x-30)/4, (event.y-30)/4]
        draw_target()
        canvas.create_oval(impact_to_add[0]*4+25, impact_to_add[1]*4+25, impact_to_add[0]
                           * 4+35, impact_to_add[1]*4+35, fill="#00C700", outline="#00C700")
        finish_button.config(state="normal")

    # Go back to the overview page and add the impact to the list
    def on_finish_button_click():
        global current_volley, impact_to_add

        if impact_to_add != [None, None]:
            arrows_coordinates[target_number].append(impact_to_add)

            new_volley = True
            for arrow in arrows_coordinates:
                if len(arrow) < current_volley:
                    new_volley = False
                    break
            if new_volley:
                current_volley += 1

            arrow_frame.destroy()
            overview()

    # Draw a target that can be clicked
    def draw_target():
        canvas.delete("all")

        if is_trispot.get():
            canvas.create_oval(32, 32, 428, 428, fill="blue")
            canvas.create_oval(72, 72, 388, 388, fill="red")
            canvas.create_oval(110, 110, 350, 350, fill="red")
            canvas.create_oval(150, 150, 310, 310, fill="yellow")
            canvas.create_oval(190, 190, 270, 270, fill="yellow")
            canvas.create_oval(210, 210, 250, 250, fill="yellow")
        else:
            canvas.create_oval(32, 32, 428, 428, fill="white")
            canvas.create_oval(51, 51, 409, 409, fill="white")
            canvas.create_oval(70, 70, 390, 390, fill="black")
            canvas.create_oval(90, 90, 370, 370, fill="black", outline="white")
            canvas.create_oval(110, 110, 350, 350, fill="blue")
            canvas.create_oval(130, 130, 330, 330, fill="blue")
            canvas.create_oval(150, 150, 310, 310, fill="red")
            canvas.create_oval(170, 170, 290, 290, fill="red")
            canvas.create_oval(190, 190, 270, 270, fill="yellow")
            canvas.create_oval(210, 210, 250, 250, fill="yellow")
            canvas.create_oval(220, 220, 240, 240, fill="yellow")

        for x, y in arrows_coordinates[target_number]:
            canvas.create_oval(x*4+25, y*4+25, x*4+35, y*4+35,
                               fill="#00C700", outline="#00C700")

    arrow_frame = ttk.Frame(window)
    arrow_frame.pack(fill="both")

    menu_bar = tk.Frame(arrow_frame, bg="#3ED8FF")
    menu_bar.pack(fill="x")
    menu_bar_content = tk.Frame(menu_bar, bg="#3ED8FF")
    menu_bar_content.pack()

    name_label = tk.Label(menu_bar_content, text=name.get(),
                          bg="#3ED8FF", font=("Segoe UI", 10, "bold"))
    name_label.grid(row=0, column=0, padx=40, pady=10)

    arrow_number_label = tk.Label(
        menu_bar_content, text="Flèche n° : " + str(target_number + 1), bg="#3ED8FF")
    arrow_number_label.grid(row=0, column=1)

    current_volley_label = tk.Label(
        menu_bar_content, text="Volée n°" + str(current_volley), bg="#3ED8FF")
    current_volley_label.grid(row=0, column=2, padx=40)

    finish_button = tk.Button(
        menu_bar_content, text="Valider", command=on_finish_button_click, state="disabled")
    finish_button.grid(row=0, column=3)

    canvas = tk.Canvas(arrow_frame, width=460, height=460)
    canvas.pack()
    draw_target()

    canvas.bind("<Button-1>", on_target_click)


def stats():
    arrows_coordinates_sorted = []
    score_list = []

    # Calculates the average value of the impacts of a given arrow
    def moyenne(list):
        somme_x = 0
        somme_y = 0
        for x, y in list:
            somme_x += x
            somme_y += y
        moyenne_x = somme_x / len(list)
        moyenne_y = somme_y / len(list)
        moyenne_x = int(moyenne_x*100)
        moyenne_y = int(moyenne_y*100)
        moyenne_x /= 100
        moyenne_y /= 100
        return (moyenne_x, moyenne_y)

    # Calculates the standard deviation value of the impacts of a given arrow
    def ecart_type(list):
        moyenne_list = moyenne(list)
        somme_ecart_carree_x = 0
        somme_ecart_carree_y = 0
        for x, y, in list:
            somme_ecart_carree_x += (x - moyenne_list[0])**2
            somme_ecart_carree_y += (y - moyenne_list[1])**2
        ecart_type_x = math.sqrt(somme_ecart_carree_x / len(list))
        ecart_type_y = math.sqrt(somme_ecart_carree_y / len(list))
        ecart_type_x = int(ecart_type_x*1000)
        ecart_type_y = int(ecart_type_y*100)
        ecart_type_x /= 1000
        ecart_type_y /= 1000
        return (ecart_type_x, ecart_type_y)

    # Calculates the regularity score of a given arrow
    def score(moyenne_score, ecart_type_score, list, number):
        distance = math.sqrt((moyenne_score[0]-50)**2+(moyenne_score[1]-50)**2)
        score_fleche = 1000 / \
            (10*distance+(ecart_type_score[0]*ecart_type_score[1]))
        score_fleche = int(score_fleche*1000)
        score_final = score_fleche/1000
        list.append((number, score_final))
        return (score_final)

    # Sort the scores in *descending* order
    def sort(coordinates_to_sort):
        n = len(coordinates_to_sort)
        for i in range(n):
            k = i
            for j in range(i+1, n):
                if coordinates_to_sort[k]["score"] < coordinates_to_sort[j]["score"]:
                    k = j
            coordinates_to_sort[k], coordinates_to_sort[i] = coordinates_to_sort[i], coordinates_to_sort[k]
        return coordinates_to_sort

    # Enables the user to scroll using the mouse wheel
    def on_scroll(event):
        can2.yview_scroll(int(-event.delta / 120), "units")

    stats_frame = ttk.Frame(window)
    stats_frame.pack(fill='both')

    for i in range(len(arrows_coordinates)):
        moyenne_fleche = moyenne(arrows_coordinates[i])
        ecart_type_fleche = ecart_type(arrows_coordinates[i])
        arrows_coordinates_sorted.append({
            "index": i,
            "score":score(moyenne_fleche, ecart_type_fleche, score_list, i+1),
            "moyenne": moyenne_fleche,
            "ecart-type": ecart_type_fleche
        })
    arrows_coordinates_sorted = sort(arrows_coordinates_sorted)

    menu_bar = tk.Frame(stats_frame, bg="#3ED8FF")
    menu_bar.pack(fill="x")
    menu_bar_content = tk.Frame(menu_bar, bg="#3ED8FF")
    menu_bar_content.pack()

    name_label = tk.Label(menu_bar_content, text=name.get(), bg="#3ED8FF", font=("Segoe UI", 10, "bold"))
    name_label.grid(row=0, column=0, padx=40, pady=10)

    arrow_number_label = tk.Label(
        menu_bar_content, text="Nombre de flèches : " + str(arrow_number.get()), bg="#3ED8FF")
    arrow_number_label.grid(row=0, column=1)

    table_container = ttk.Frame(stats_frame)
    table_container.pack()

    scroll_bar_score = ttk.Scrollbar(table_container, orient='vertical')
    scroll_bar_score.pack(side='right', fill='y')
    can2 = tk.Canvas(
        table_container,
        width=800,
        height=(len(arrows_coordinates_sorted) + 1)*30,
        yscrollcommand=scroll_bar_score.set,
        scrollregion='0 0 800 ' + str((len(arrows_coordinates_sorted) + 1)*30))
    can2.pack()
    can2.bind_all("<MouseWheel>", on_scroll)
    scroll_bar_score.config(command=can2.yview)

    can2.create_text(100, 15, text="Classement :")
    can2.create_text(250, 15, text="Flèche n°", font=("Segoe UI", 10, "bold"))
    can2.create_text(400, 15, text="Moyenne :")
    can2.create_text(550, 15, text="Ecart-type :")
    can2.create_text(700, 15, text="Score :", font=("Segoe UI", 10, "bold"))

    arrow_y = 3

    for i in range(len(arrows_coordinates_sorted)):
        can2.create_text(100, 15*arrow_y, text="#"+str(i+1))
        can2.create_text(250, 15*arrow_y, text="n°" +
                         str(arrows_coordinates_sorted[i]["index"]+1), font=("Segoe UI", 10, "bold"))
        can2.create_text(400, 15*arrow_y, text="x : " + str(
            arrows_coordinates_sorted[i]["moyenne"][0]) + "   y : " + str(arrows_coordinates_sorted[i]["moyenne"][1]))
        can2.create_text(550, 15*arrow_y, text="x : " + str(
            arrows_coordinates_sorted[i]["ecart-type"][0]) + "   y : " + str(arrows_coordinates_sorted[i]["ecart-type"][1]))
        can2.create_text(
            700, 15*arrow_y, text=str(arrows_coordinates_sorted[i]["score"]), font=("Segoe UI", 10, "bold"))
        arrow_y += 2

    # Create the Matplotlib plot and show it
    def plots(list):
        plots_fleche = []
        plots_score = []
        for i in range(len(list)):
            plots_fleche.append(list[i]["index"]+1)
            plots_score.append(list[i]["score"])
        _, axes = plt.subplots()
        axes.bar(x=plots_fleche, height=plots_score)
        axes.xaxis.set_major_locator(MaxNLocator(integer=True))
        axes.set_title("Tri de flèches")
        plt.ylabel("Score")
        plt.xlabel("Numéro de flèche")
        plt.show()
    graph_button = tk.Button(
        menu_bar_content, text="Graphique", command=lambda: plots(arrows_coordinates_sorted))
    graph_button.grid(row=0, column=2, padx=40, pady=10)

    # Save to disk
    with open("data/" + str(name.get()) + ".json", "w") as file:
        file.write(json.dumps(arrows_coordinates))
    
    # Button to go back to the home page
    def go_home():
        stats_frame.destroy()
        home()

    go_home_button = tk.Button(menu_bar_content, text="Accueil", command=go_home)
    go_home_button.grid(row=0, column=3)


home()
window.mainloop()
