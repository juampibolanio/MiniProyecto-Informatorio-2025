import tkinter as tk
from tkinter import messagebox
import time
import locale
import os

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
ventana.title('Diario de Hábitos')
ventana.geometry('1050x700') 
ventana.configure(bg="#F4EDE4")

# =====> Reloj y Fecha <=====
reloj = tk.Label(
    ventana, 
    font=('Arial', 24, 'bold'),
    fg="#625A5A", 
    bg="#F4EDE4")
fecha = tk.Label(
    ventana, 
    font=('Arial', 14),
    fg='#625A5A', 
    bg='#F4EDE4')

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
    bg="#EADBC8", 
    fg='#000000',
    activebackground="#9DB17C", 
    activeforeground="black")

menu_principal = tk.Menu(
    barra_menu, 
    tearoff=0, 
    bg="#EADBC8",
    fg='#000000', 
    activebackground="#9DB17C", 
    activeforeground="black")

barra_menu.add_cascade(label='Menú', menu=menu_principal)

submenu = tk.Menu(
    menu_principal, 
    tearoff=0, 
    bg="#EADBC8", 
    fg='#000000',
    activebackground="#9DB17C", 
    activeforeground="black")

menu_principal.add_cascade(label='Opciones', menu=submenu)

# =====> Funciones de guardar y cargar <=====
def guardar_tareas():
    with open("tareas.txt", "w", encoding="utf-8") as archivo:
        for tarea in lista_tareas.get(0, tk.END):
            archivo.write(tarea + "\n")

def cargar_tareas():
    if os.path.exists("tareas.txt"):
        with open("tareas.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                lista_tareas.insert(tk.END, linea.strip())

submenu.add_command(label='Guardar tareas', command=guardar_tareas)
submenu.add_command(label='Cargar tareas', command=cargar_tareas)

menu_principal.add_separator()
menu_principal.add_command(label='Salir', command=lambda: confirmar_salida())

ventana.config(menu=barra_menu)

# =====> Entrada de tareas <=====
frame_entrada = tk.Frame(ventana, bg="#F4EDE4")
frame_entrada.pack(anchor="w", padx=10, pady=10)

entrada_tarea = tk.Entry(
    frame_entrada, 
    width=30, 
    font=('Arial', 10, 'normal'),
    bg="#EADBC8", 
    fg="#3E2C23", 
    insertbackground="#3E2C23")
entrada_tarea.pack(side=tk.LEFT, padx=5)

def agregar_tarea():
    tarea = entrada_tarea.get().strip()
    if tarea and tarea not in lista_tareas.get(0, tk.END):
        lista_tareas.insert(tk.END, tarea)
        entrada_tarea.delete(0, tk.END)

entrada_tarea.bind("<Return>", lambda event: agregar_tarea())

boton_agregar = tk.Button(
    frame_entrada, 
    text='Agregar', 
    command=agregar_tarea,       
    bg="#EADBC8", 
    fg="#3E2C23", 
    font=('Arial', 8,))
boton_agregar.pack(side=tk.LEFT)

# =====> Lista de tareas con scroll <=====
frame_lista = tk.Frame(ventana, bg='#F4EDE4')
frame_lista.place(x=10, y=100, width=300, height=150) 

scrollbar = tk.Scrollbar(
    frame_lista,
    troughcolor="#A28C7E", 
    bg="#A28C7E",
    activebackground="#C2B4AA")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_tareas = tk.Listbox(
    frame_lista, 
    yscrollcommand=scrollbar.set,
    height=5, 
    bg="#D6C0B3", 
    fg="#3E2C23",
    selectbackground="#A4B7C1", 
    selectforeground="black",
    highlightbackground="#A28C7E")

lista_tareas.config(font=('Arial', 10, 'normal'))
lista_tareas.bind('<<ListboxSelect>>', lambda e: actualizar_texto_boton())
lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=lista_tareas.yview)

# =====> Botón marcar y desmarcar como hecho <=====
def actualizar_texto_boton(event=None):
    seleccion = lista_tareas.curselection()
    if seleccion:
        texto = lista_tareas.get(seleccion[0])
        if texto.startswith('✔ '):
            boton_alternar.config(text='Marcar como no hecho')
        else:
            boton_alternar.config(text='Marcar como hecho')

def alternar_estado():
    seleccion = lista_tareas.curselection()
    if seleccion:
        indice = seleccion[0]
        texto = lista_tareas.get(indice)
        if texto.startswith("✔ "):
            nuevo_texto = texto[2:]
            lista_tareas.delete(indice)
            lista_tareas.insert(indice, nuevo_texto)
            lista_tareas.itemconfig(indice, {'fg': '#3E2C23'})
        else:
            lista_tareas.delete(indice)
            lista_tareas.insert(indice, f"✔ {texto}")
            lista_tareas.itemconfig(indice, {'fg': 'green'})
        actualizar_texto_boton()

boton_alternar = tk.Button(
    ventana, 
    text='Marcar como hecho',
    command=alternar_estado, 
    bg="#EADBC8", 
    fg="#3E2C23", 
    font=('Arial', 8))
boton_alternar.place(x=160, y=260) 

# =====> Botón eliminar <=====
def eliminar_tarea():
    seleccion = lista_tareas.curselection()
    if seleccion:
        lista_tareas.delete(seleccion)

boton_eliminar = tk.Button(
    ventana, 
    text='Eliminar tarea seleccionada',
    command=eliminar_tarea, 
    bg='#EADBC8', 
    fg="#3E2C23",
    font=('Arial', 8))
boton_eliminar.place(x=10, y=260) 

# =====> Salida confirmada <=====
def confirmar_salida():
    if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
        guardar_tareas()
        ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", confirmar_salida)

# =====> Sección de planificación semanal <=====
frame_semanal = tk.LabelFrame(
    ventana,
    text="Planificación Semanal",
    font=("Arial", 12, "bold"),
    bg="#F4EDE4",
    fg="#3E2C23",
    bd=2,
    padx=10,
    pady=10,
    labelanchor="n"
)
frame_semanal.place(x=330, y=100, width=710, height=580)  

# =====> Función para crear día de la semana <=====

def crear_dia(frame_padre, dia_nombre, fila, columna):
    contenedor = tk.Frame(
        frame_padre, 
        bg="#F4EDE4"
    )
    contenedor.grid(
        row=fila, 
        column=columna, 
        padx=5, 
        pady=5, 
        sticky="n"
    )

    label = tk.Label(
        contenedor, 
        text=dia_nombre, 
        font=("Arial", 10, "bold"), 
        bg="#F4EDE4", 
        fg="#3E2C23"
    )
    label.pack()

    entrada = tk.Entry(
        contenedor, 
        width=20, 
        bg="#EADBC8", 
        fg="#3E2C23", 
        font=("Arial", 9)
    )
    entrada.pack(pady=2)
    
    lista_frame = tk.Frame(contenedor)
    lista_frame.pack()

    scrollbar = tk.Scrollbar(lista_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(
        lista_frame, 
        height=6, 
        width=28, 
        yscrollcommand=scrollbar.set, 
        bg="#D6C0B3", 
        fg="#3E2C23", 
        selectbackground="#A4B7C1", 
        font=("Arial", 9)
    )
    lista.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=lista.yview)
    #Tendría que reemplazar esta función de agregar por la q ya teníamos más arriba. También agregar la de eliminar y marcar.
    def agregar():  
        tarea = entrada.get().strip()
        if tarea:
            lista.insert(tk.END, tarea)
            entrada.delete(0, tk.END)
    
    boton = tk.Button(
        contenedor,
        text="Agregar",
        command=agregar,
        bg="#EADBC8", 
        fg="#3E2C23", 
        font=("Arial", 8)
    )
    boton.pack(pady=2)

#Creando los dias de la semana utilizando la función.
crear_dia(frame_semanal, "Lunes", 0, 0)
crear_dia(frame_semanal, "Martes", 0, 1)
crear_dia(frame_semanal, "Miércoles", 0, 2)
crear_dia(frame_semanal, "Jueves", 1, 0)
crear_dia(frame_semanal, "Viernes", 1, 1)
crear_dia(frame_semanal, "Sábado", 1, 2)
crear_dia(frame_semanal, "Domingo", 2, 1)


# =====> Iniciar programa <=====
actualizar()
cargar_tareas()
ventana.mainloop()
