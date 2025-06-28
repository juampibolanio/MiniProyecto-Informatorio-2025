# Proyecto para Informatorio
# Diario de Hábitos

# LIBRERIAS
import tkinter as tk
from tkinter import messagebox
import time
import locale
from tkcalendar import Calendar
from datetime import datetime

# =====> formato de fecha y hora xd <=====
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español.")

# =====> Diccionario para almacenar tareas por fecha <=====
tareas_por_fecha = {}
ultima_fecha_seleccionada = None

# =====> Funciones internas <=====
def iniciar_aplicacion():
    global ventana, calendario, entrada_tarea, lista_tareas, ultima_fecha_seleccionada

    ventana = tk.Tk()
    ventana.title('Diario de Hábitos')
    ventana.geometry('900x500')
    ventana.configure(bg="#F4EDE4")
    ventana.columnconfigure(0, weight=3)
    ventana.columnconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)

    # Reloj y fecha
    reloj = tk.Label(ventana, font=('Arial', 20, 'bold'), fg="#625A5A", bg="#F4EDE4")
    reloj.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
    fecha = tk.Label(ventana, font=('Arial', 12), fg="#625A5A", bg="#F4EDE4")
    fecha.grid(row=1, column=0, sticky="w", padx=10)

    def actualizar():
        ahora = time.localtime()
        reloj.config(text=time.strftime('%H:%M:%S', ahora))
        fecha.config(text=time.strftime('%d de %B %Y', ahora).lower())
        ventana.after(1000, actualizar)

    # Entrada + boton agregar
    frame_entrada = tk.Frame(ventana, bg="#F4EDE4")
    frame_entrada.grid(row=0, column=1, columnspan=2, sticky="e", padx=10)
    entrada_tarea = tk.Entry(frame_entrada, width=40, font=('Arial', 10), bg="#EADBC8", fg="#3E2C23")
    entrada_tarea.pack(side=tk.LEFT, padx=(0, 5))
    tk.Button(frame_entrada, text='Agregar', command=agregar_tarea_fecha, bg="#EADBC8", fg="#3E2C23").pack(side=tk.LEFT)

    # Lista tareas
    frame_tareas = tk.Frame(ventana, bg="#F4EDE4")
    frame_tareas.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame_tareas.columnconfigure(0, weight=1)
    frame_tareas.rowconfigure(0, weight=1)

    scrollbar = tk.Scrollbar(frame_tareas)
    scrollbar.grid(row=0, column=1, sticky="ns")

    lista_tareas = tk.Listbox(frame_tareas, yscrollcommand=scrollbar.set, bg="#D6C0B3", fg="#3E2C23",
                              selectbackground="#A4B7C1", font=('Arial', 10))
    lista_tareas.grid(row=0, column=0, sticky="nsew")
    scrollbar.config(command=lista_tareas.yview)

    # Botones verticales
    frame_botones = tk.Frame(ventana, bg="#F4EDE4")
    frame_botones.grid(row=2, column=1, sticky="ns", padx=10)
    for idx, (texto, comando) in enumerate([
        ("Marcar como hecho", alternar_estado),
        ("Eliminar seleccionada", eliminar_tarea),
        ("Ver estadísticas", mostrar_estadisticas)]):
        tk.Button(frame_botones, text=texto, command=comando,
                  bg="#EADBC8", fg="#3E2C23", font=('Arial', 9)).grid(row=idx, column=0, pady=5, sticky="ew")

    # Calendario
    frame_calendario = tk.Frame(ventana, bg="#F4EDE4")
    frame_calendario.grid(row=2, column=2, padx=10, sticky="n")
    calendario = Calendar(frame_calendario, selectmode="day", background="#EADBC8", foreground="#3E2C23")
    calendario.pack(pady=10)
    calendario.bind("<<CalendarSelected>>", lambda e: cambiar_dia())

    def confirmar_salida():
        if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
            ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", confirmar_salida)
    actualizar()
    mostrar_tareas_del_dia()  # Mostrar las del día por defecto
    ventana.mainloop()

def cambiar_dia():
    global ultima_fecha_seleccionada
    nueva_fecha = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
    if nueva_fecha not in tareas_por_fecha and ultima_fecha_seleccionada in tareas_por_fecha:
        # Aca se agrega sin check las tareas del dia anterior
        tareas_sin_check = [t.lstrip("✔ ").strip() for t in tareas_por_fecha[ultima_fecha_seleccionada]]
        tareas_por_fecha[nueva_fecha] = tareas_sin_check.copy()
    ultima_fecha_seleccionada = nueva_fecha
    mostrar_tareas_del_dia()


# =====> Funciones auxiliares <=====
def agregar_tarea_fecha():
    fecha = calendario.get_date()
    fecha_obj = datetime.strptime(fecha, "%d/%m/%y").date()
    tarea = entrada_tarea.get().strip()
    if tarea:
        tareas_por_fecha.setdefault(fecha_obj, []).append(tarea)
        mostrar_tareas_del_dia()
        calendario.calevent_create(fecha_obj, "Tarea", "tarea")
        calendario.tag_config("tarea", background="lightblue", foreground="black")
        entrada_tarea.delete(0, tk.END)

def mostrar_tareas_del_dia():
    fecha = calendario.get_date()
    fecha_obj = datetime.strptime(fecha, "%d/%m/%y").date()
    lista_tareas.delete(0, tk.END)
    for tarea in tareas_por_fecha.get(fecha_obj, []):
        lista_tareas.insert(tk.END, tarea)

def alternar_estado():
    i = lista_tareas.curselection()
    if i:
        idx = i[0]
        texto = lista_tareas.get(idx)
        nuevo = texto[2:] if texto.startswith("✔ ") else f"✔ {texto}"
        lista_tareas.delete(idx)
        lista_tareas.insert(idx, nuevo)

def eliminar_tarea():
    i = lista_tareas.curselection()
    if i:
        idx = i[0]
        tarea = lista_tareas.get(idx)
        lista_tareas.delete(idx)
        fecha = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
        if fecha in tareas_por_fecha:
            if tarea in tareas_por_fecha[fecha]:
                tareas_por_fecha[fecha].remove(tarea)
            if not tareas_por_fecha[fecha]:
                del tareas_por_fecha[fecha]

def mostrar_estadisticas():
    total = sum(len(t) for t in tareas_por_fecha.values())
    hechas = sum(1 for tareas in tareas_por_fecha.values() for t in tareas if t.startswith("✔ "))
    dias = len(tareas_por_fecha)
    mensaje = f"""📊 Estadísticas:\n\n- Tareas totales: {total}\n- Completadas: {hechas}\n- Días con tareas: {dias}"""
    messagebox.showinfo("Estadísticas", mensaje)

# =====> CONTRASEÑA DE INICIO =====
def verificar_contraseña():
    if entrada_contrasena.get() == "1234":
        login.destroy()
        iniciar_aplicacion()
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")

login = tk.Tk()
login.title("Inicio de sesión")
login.geometry("300x150")
login.configure(bg="#F4EDE4")
tk.Label(login, text="Contraseña:", bg="#F4EDE4").pack(pady=10)
entrada_contrasena = tk.Entry(login, show="*", width=20)
entrada_contrasena.pack()
tk.Button(login, text="Ingresar", command=verificar_contraseña).pack(pady=10)
login.mainloop()

