import tkinter as tk
from tkinter import messagebox
import time
import locale
import os
from tkcalendar import Calendar
from datetime import datetime
import json

# =====> Localización en español <=====
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español para los nombres de los meses.")

# =====> Ventana principal <=====
ventana = tk.Tk()
ventana.title('Administrador de hábitos')
ventana.geometry('700x400')
ventana.configure(bg="#190247")
tareas_por_fecha = {}

# =====> Reloj y Fecha <=====
reloj = tk.Label(
    ventana, 
    font=('Calibri', 24, 'bold'),
    fg="#034384", 
    bg="#190247")
fecha = tk.Label(
    ventana, 
    font=('Calibri', 14, 'underline'),
    fg="white", 
    bg="#190247")

reloj.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
fecha.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=50)

def actualizar():
    ahora = time.localtime()
    hora_str = time.strftime('%H:%M:%S', ahora)
    fecha_str = time.strftime('%d de %B %Y', ahora).lower()
    reloj.config(text=hora_str)
    fecha.config(text=fecha_str)
    ventana.after(1000, actualizar)

# =====> Menú desplegable <=====
barra_menu = tk.Menu(
    ventana, 
    bg="#FFFFFF", 
    fg='black',
    activebackground="#0B048A", 
    activeforeground="white")

menu_principal = tk.Menu(
    barra_menu, 
    tearoff=0, 
    bg="#FFFFFF",
    fg='black', 
    activebackground="#0B048A", 
    activeforeground="white")

barra_menu.add_cascade(label='Menú', menu=menu_principal)

submenu = tk.Menu(
    menu_principal, 
    tearoff=0, 
    bg="#FFFFFF", 
    fg='black',
    activebackground="#0B048A", 
    activeforeground="white")

menu_principal.add_cascade(label='Opciones', menu=submenu)

# =====> Funciones de guardar y cargar <=====
def guardar_tareas():
    with open("tareas.json", "w", encoding="utf-8") as archivo:
        json.dump(tareas_por_fecha, archivo, ensure_ascii=False, indent=4)

def cargar_tareas():
    global tareas_por_fecha
    if os.path.exists("tareas.json"):
        with open("tareas.json", "r", encoding="utf-8") as archivo:
            tareas_por_fecha = json.load(archivo)
        fecha_actual = calendario.get_date()
        mostrar_tareas_para_fecha(fecha_actual)
        if os.path.exists("tareas.txt"):
            os.remove("tareas.txt")

submenu.add_command(label='Guardar tareas', command=guardar_tareas)
submenu.add_command(label='Cargar tareas', command=cargar_tareas)

menu_principal.add_separator()
menu_principal.add_command(label='Salir', command=lambda: confirmar_salida())

ventana.config(menu=barra_menu)

# =====> Entrada de tareas <=====
frame_entrada = tk.Frame(ventana, bg="#034384")
frame_entrada.pack(anchor="w", padx=10, pady=10)

entrada_tarea = tk.Entry(
    frame_entrada, 
    width=30, 
    font=('Courier New', 10),
    bg="#8595F9", 
    fg="black", 
    insertbackground="black")
entrada_tarea.pack(side=tk.LEFT, padx=5)

def agregar_tarea():
    tarea = entrada_tarea.get().strip()
    if tarea:
        fecha_sel = calendario.get_date()
        if fecha_sel not in tareas_por_fecha:
            tareas_por_fecha[fecha_sel] = []
        if tarea not in tareas_por_fecha[fecha_sel]:
            tareas_por_fecha[fecha_sel].append(tarea)
            entrada_tarea.delete(0, tk.END)
            mostrar_tareas_para_fecha(fecha_sel)

def mostrar_tareas_para_fecha(fecha):
    lista_tareas.delete(0, tk.END)
    if fecha in tareas_por_fecha:
        for tarea in tareas_por_fecha[fecha]:
            lista_tareas.insert(tk.END, tarea)

entrada_tarea.bind("<Return>", lambda event: agregar_tarea())

boton_agregar = tk.Button(
    frame_entrada, 
    text='Agregar', 
    command=agregar_tarea,       
    bg="#17611D", 
    fg="white", 
    font=('Calibri', 9, "bold"))
boton_agregar.pack(side=tk.LEFT)

# =====> Lista de tareas con scroll <=====
frame_lista = tk.Frame(ventana, bg='#333333')
frame_lista.place(x=10, y=100, width=300, height=230) 

scrollbar = tk.Scrollbar(
    frame_lista,
    troughcolor="#034384", 
    bg="#555555",
    activebackground="#777777", 
    highlightbackground="#333333")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_tareas = tk.Listbox(
    frame_lista, 
    yscrollcommand=scrollbar.set,
    height=12,  # ahora más alto
    bg="#8595F9", 
    fg="black",
    selectbackground="#370188", 
    selectforeground="white",
    highlightbackground="#FFFFFF",
    font=('Courier New', 10)
)

lista_tareas.config(font=('Courier New', 10))
lista_tareas.bind('<<ListboxSelect>>', lambda e: actualizar_texto_boton())
lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=lista_tareas.yview)

# =====> Botón marcar y desmarcar como hecho <=====
def actualizar_texto_boton(event=None):
    seleccion = lista_tareas.curselection()
    if seleccion:
        texto = lista_tareas.get(seleccion[0])
        if texto.startswith('✅ '):
            boton_alternar.config(
                text='Desmarcar',
                bg='red',
                fg='white',
                font=('Calibri', 9, 'bold')
            )
        else:
            boton_alternar.config(
                text='Marcar como hecho',
                bg='green',
                fg='white',
                font=('Calibri', 9, 'bold')
            )


def alternar_estado():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        fecha_sel = calendario.get_date()
        if fecha_sel in tareas_por_fecha:
            texto = tareas_por_fecha[fecha_sel][indice]
            if texto.startswith("✅ "):
                nuevo_texto = texto[2:]
                tareas_por_fecha[fecha_sel][indice] = nuevo_texto
                lista_tareas.itemconfig(indice, {'fg': 'red'})
            else:
                nuevo_texto = f"✅ {texto}"
                tareas_por_fecha[fecha_sel][indice] = nuevo_texto
                lista_tareas.itemconfig(indice, {'fg': 'green'})
            mostrar_tareas_para_fecha(fecha_sel)
            actualizar_texto_boton()

boton_alternar = tk.Button(
    ventana, 
    text='Marcar hecho',
    command=alternar_estado, 
    bg="#FFFFFF", 
    fg="black", 
    font=('Calibri', 9, 'bold'))
boton_alternar.place(x=160, y=350)

# =====> Botón eliminar <=====
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        fecha_sel = calendario.get_date()
        if fecha_sel in tareas_por_fecha:
            del tareas_por_fecha[fecha_sel][indice]
            # Si ya no quedan tareas en esa fecha, eliminamos la clave
            if not tareas_por_fecha[fecha_sel]:
                del tareas_por_fecha[fecha_sel]
            mostrar_tareas_para_fecha(fecha_sel)

boton_eliminar = tk.Button(
    ventana, 
    text='Eliminar tarea',
    command=eliminar_tarea, 
    bg="#460101", 
    fg="white",
    font=('Calibri', 9, 'bold'))
boton_eliminar.place(x=10, y=350)

# =====> Frame para el calendario <=====
frame_calendario = tk.Frame(ventana, bg="#190247")
frame_calendario.place(x=330, y=100)
calendario = Calendar(
    frame_calendario,
    selectmode='day',
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
    locale='es_ES',  # idioma en español
    background='#370188',
    foreground='white',
    headersbackground='#034384',
    headersforeground='white',
    selectbackground='#17611D',
    selectforeground='white'
)
calendario.bind("<<CalendarSelected>>", lambda e: actualizar_fecha())
calendario.pack(padx=10, pady=10)


# Etiqueta para mostrar la fecha seleccionada
label_fecha = tk.Label(
    frame_calendario, 
    text="Fecha seleccionada: ", 
    bg="#190247", 
    fg="white", 
    font=("Calibri", 10)
)
label_fecha.pack()

# Función para mostrar la fecha al seleccionar
def actualizar_fecha():
    fecha_sel = calendario.get_date()
    label_fecha.config(text=f"Fecha seleccionada: {fecha_sel}")
    mostrar_tareas_para_fecha(fecha_sel)

# =====> Salida confirmada <=====
def confirmar_salida():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        guardar_tareas()
        ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", confirmar_salida)

# =====> Iniciar programa <=====
actualizar()
cargar_tareas()
fecha_actual = calendario.get_date()
mostrar_tareas_para_fecha(fecha_actual)
ventana.mainloop()
