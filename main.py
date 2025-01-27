import tkinter as tk
from tkinter import ttk
import math

window = tk.Tk()
window.title("Mini-projet NSI")
window.geometry("800x500")
window.minsize(800, 500)
window.maxsize(800, 500)

arrow_number = tk.IntVar(value=9)
is_trispot = tk.BooleanVar(value=False)
arrows_coordinates = []
current_volley = 1
overview_scroll_position = 0
arc = tk.PhotoImage(file='arc_accueil.png')
window.wm_attributes("-transparentcolor", "orange")


def home():
    def start():
        if arrow_number.get() < 1:
            return

        for _ in range(arrow_number.get()):
            arrows_coordinates.append([])
        home_frame.destroy()
        can1.destroy()
        overview()

    can1 = tk.Canvas(window, width=800, height=500)
    can1.create_image(400, 250, image=arc)
    can1.place(x=0, y=0)
    home_frame = ttk.Frame(window)
    home_frame.pack(pady=(10, 0))

    title_label = ttk.Label(
        home_frame, text="Trieur de flèches", font=("Segoe UI", 32))
    title_label.pack(padx=10, pady=5)

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


def overview():
    def is_target_complete(target_number):
        return len(arrows_coordinates[target_number]) == current_volley

    def open_target(target_number):
        global overview_scroll_position

        if len(arrows_coordinates[target_number]) < current_volley:
            overview_scroll_position = scroll_bar.get()[0]
            overview_frame.destroy()
            add_impact(target_number)

    def on_target_click(event, scroll_bar_offset):
        target_number = int(
            ((event.y + scroll_bar_offset) // 120) * 3 + (event.x // 120))
        open_target(target_number)

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
                xPos+x-2, yPos+y-2, xPos+x+2, yPos+y+2, fill="green", outline="green")

        if is_target_complete(target_number):
            target_canvas.create_oval(
                xPos+2, yPos+2, xPos+98, yPos+98, fill="#C6C6C6")
            target_canvas.create_text(
                xPos+50, yPos+49, text="✔️", font=("Segoe UI Emoji", 16))
        else:
            target_canvas.create_text(
                xPos+50, yPos+49, text=str(target_number+1), font=("Segoe UI", 16))

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
    menu_bar_content.pack()

    arrow_number_label = tk.Label(
        menu_bar_content, text="Nombre de flèches : " + str(arrow_number.get()), bg="#3ED8FF")
    arrow_number_label.grid(row=0, column=0)

    current_volley_label = tk.Label(
        menu_bar_content, text="Volée n°" + str(current_volley), bg="#3ED8FF")
    current_volley_label.grid(row=0, column=1, padx=40, pady=10)

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
    for i in range(arrow_number.get()):
        small_target(i)
    target_canvas.bind("<Button-1>", lambda event: on_target_click(event,
                       scroll_bar.get()[0]*target_canvas_height))

    finish_button = tk.Button(menu_bar_content, text="Terminer", command=on_finish_click,
                              state="normal" if is_finish_button_active() else "disabled")
    finish_button.grid(row=0, column=2)

def add_impact(target_number):
    global impact_to_add
    impact_to_add = [None, None]

    def on_target_click(event):
        global impact_to_add
        impact_to_add = [(event.x-30)/4, (event.y-30)/4]
        draw_target()
        canvas.create_oval(impact_to_add[0]*4+25, impact_to_add[1]*4+25, impact_to_add[0]*4+35, impact_to_add[1]*4+35, fill="green", outline="green")
        finish_button.config(state="normal")

    def on_button_click():
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
            canvas.create_oval(x*4+25, y*4+25, x*4+35, y*4+35, fill="green", outline="green")
        
    arrow_frame = ttk.Frame(window)
    arrow_frame.pack(fill="both")

    menu_bar = tk.Frame(arrow_frame, bg="#3ED8FF")
    menu_bar.pack(fill="x")
    menu_bar_content = tk.Frame(menu_bar, bg="#3ED8FF")
    menu_bar_content.pack()

    arrow_number_label = tk.Label(
        menu_bar_content, text="Flèche n° : " + str(target_number + 1), bg="#3ED8FF")
    arrow_number_label.grid(row=0, column=0)

    current_volley_label = tk.Label(
        menu_bar_content, text="Volée n°" + str(current_volley), bg="#3ED8FF")
    current_volley_label.grid(row=0, column=1, padx=40, pady=10)

    finish_button = tk.Button(menu_bar_content, text="Valider", command=on_button_click, state="disabled")
    finish_button.grid(row=0, column=2)

    canvas = tk.Canvas(arrow_frame, width=460, height=460)
    canvas.pack()
    draw_target()
    
    canvas.bind("<Button-1>", on_target_click)


def stats():
    arrows_classement = []

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

    def score(moyenne_score,ecart_type_score):
        distance=math.sqrt((moyenne_score[0]-50)**2+(moyenne_score[1]-50)**2)
        score_fleche=1000/(10*distance+(ecart_type_score[0]*ecart_type_score[1]))
        score_final=float(score_fleche)
        return (score_final)

    stats_frame = ttk.Frame(window)
    stats_frame.pack(fill='both')

    for i in range(len(arrows_coordinates)):
        moyenne_fleche = moyenne(arrows_coordinates[i])
        ecart_type_fleche=ecart_type(arrows_coordinates[i])
        arrows_classement.append([score(moyenne_fleche,ecart_type_fleche),i,moyenne_fleche,ecart_type_fleche])
    arrows_classement.sort()
    arrows_classement.reverse()
    
    scroll_bar_score=ttk.Scrollbar(stats_frame, orient='vertical')
    scroll_bar_score.pack(side='right',fill='y')
    can2=tk.Canvas(stats_frame,width=800,height=(len(arrows_classement)+1)*30,yscrollcommand=scroll_bar_score.set,scrollregion='0 0 800 '+str((len(arrows_classement)+1)*30))
    can2.pack()
    scroll_bar_score.config(command=can2.yview)
    
    can2.create_text(75,15,text="Flèche n°")
    can2.create_text(225,15,text="Moyenne :")
    can2.create_text(425,15,text="Ecart-type :")
    can2.create_text(625,15,text="Score :")
    can2.create_text(725,15,text="Classement :")

    arrow_y = 3

    for i in range(len(arrows_classement)):
        can2.create_text(75,15*arrow_y,text=str(arrows_classement[i][1]+1))
        can2.create_text(225,15*arrow_y,text="x : " + str(arrows_classement[i][2][0]) + "   y : " + str(arrows_classement[i][2][1]))
        can2.create_text(425,15*arrow_y,text="x : " + str(arrows_classement[i][3][0]) + "   y : " + str(arrows_classement[i][3][1]))
        can2.create_text(625,15*arrow_y,text=str(arrows_classement[i][0]))
        can2.create_text(725,15*arrow_y,text="#"+str(i+1))
        arrow_y += 2


home()
window.mainloop()
