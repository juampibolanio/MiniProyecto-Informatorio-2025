import tkinter as tk
from tkinter import messagebox
import time
import locale
from tkcalendar import Calendar
from datetime import datetime

try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except locale.Error:
        print("Advertencia: No se pudo configurar el idioma a español.")

# Variables globales
tareas_por_fecha = {}
ultima_fecha_seleccionada = None
mostrar_reloj = True

# Función principal
def iniciar_aplicacion():
    global ventana, calendario, entrada_tarea, lista_tareas, reloj, label_fecha

    ventana = tk.Tk()
    ventana.title('Diario de Hábitos')
    ventana.geometry('900x500')
    ventana.configure(bg="#F4EDE4")
    ventana.columnconfigure(0, weight=3)
    ventana.columnconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)

    # ===== Menú desplegable =====
    barra_menu = tk.Menu(ventana)

    menu_archivo = tk.Menu(barra_menu, tearoff=0)
    menu_archivo.add_command(label="Ordenar hábitos", command=ordenar_habitos)
    menu_archivo.add_command(label="Borrar todos los hábitos", command=borrar_todos)
    menu_archivo.add_separator()
    menu_archivo.add_command(label="Salir", command=ventana.quit)

    menu_ver = tk.Menu(barra_menu, tearoff=0)
    menu_ver.add_command(label="Mostrar/Ocultar reloj", command=alternar_reloj)

    menu_info = tk.Menu(barra_menu, tearoff=0)
    menu_info.add_command(label="Acerca de", command=mostrar_acerca)

    barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
    barra_menu.add_cascade(label="Ver", menu=menu_ver)
    barra_menu.add_cascade(label="Ayuda", menu=menu_info)

    ventana.config(menu=barra_menu)

    # ===== Reloj y Fecha =====
    reloj = tk.Label(ventana, font=('Arial', 20, 'bold'), fg="#625A5A", bg="#F4EDE4")
    reloj.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
    label_fecha = tk.Label(ventana, font=('Arial', 12), fg="#625A5A", bg="#F4EDE4")
    label_fecha.grid(row=1, column=0, sticky="w", padx=10)

    def actualizar():
        ahora = time.localtime()
        reloj.config(text=time.strftime('%H:%M:%S', ahora))
        label_fecha.config(text=time.strftime('%d de %B %Y', ahora).lower())
        ventana.after(1000, actualizar)

    # ===== Entrada y botón agregar =====
    frame_entrada = tk.Frame(ventana, bg="#F4EDE4")
    frame_entrada.grid(row=0, column=1, columnspan=2, sticky="e", padx=10)
    entrada_tarea = tk.Entry(frame_entrada, width=40, font=('Arial', 10), bg="#EADBC8", fg="#3E2C23")
    entrada_tarea.pack(side=tk.LEFT, padx=(0, 5))
    tk.Button(frame_entrada, text='Agregar', command=agregar_tarea_fecha,
              bg="#EADBC8", fg="#3E2C23").pack(side=tk.LEFT)

    # ===== Lista de tareas =====
    frame_tareas = tk.Frame(ventana, bg="#F4EDE4")
    frame_tareas.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    frame_tareas.columnconfigure(0, weight=1)
    frame_tareas.rowconfigure(0, weight=1)

    scrollbar = tk.Scrollbar(frame_tareas)
    scrollbar.grid(row=0, column=1, sticky="ns")

    lista_tareas = tk.Listbox(frame_tareas, yscrollcommand=scrollbar.set,
                              bg="#D6C0B3", fg="#3E2C23", font=('Arial', 10),
                              selectbackground="#A4B7C1")
    lista_tareas.grid(row=0, column=0, sticky="nsew")
    scrollbar.config(command=lista_tareas.yview)

    # ===== Botones =====
    frame_botones = tk.Frame(ventana, bg="#F4EDE4")
    frame_botones.grid(row=2, column=1, sticky="ns", padx=10)
    for idx, (texto, comando) in enumerate([
        ("Marcar como hecho", alternar_estado),
        ("Eliminar seleccionada", eliminar_tarea),
        ("Ver estadísticas", mostrar_estadisticas)]):
        tk.Button(frame_botones, text=texto, command=comando,
                  bg="#EADBC8", fg="#3E2C23", font=('Arial', 9)).grid(row=idx, column=0, pady=5, sticky="ew")

    # ===== Calendario =====
    frame_calendario = tk.Frame(ventana, bg="#F4EDE4")
    frame_calendario.grid(row=2, column=2, padx=10, sticky="n")
    calendario = Calendar(frame_calendario, selectmode="day", background="#EADBC8", foreground="#3E2C23")
    calendario.pack(pady=10)
    calendario.bind("<<CalendarSelected>>", lambda e: cambiar_dia())

    actualizar()
    mostrar_tareas_del_dia()
    ventana.mainloop()


# ===== Funciones auxiliares =====

def cambiar_dia():
    global ultima_fecha_seleccionada
    nueva_fecha = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
    if nueva_fecha not in tareas_por_fecha and ultima_fecha_seleccionada in tareas_por_fecha:
        tareas_sin_check = [t.lstrip("✔ ").strip() for t in tareas_por_fecha[ultima_fecha_seleccionada]]
        tareas_por_fecha[nueva_fecha] = tareas_sin_check.copy()
    ultima_fecha_seleccionada = nueva_fecha
    mostrar_tareas_del_dia()

def agregar_tarea_fecha():
    fecha_obj = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
    tarea = entrada_tarea.get().strip()
    if tarea:
        tareas_por_fecha.setdefault(fecha_obj, []).append(tarea)
        mostrar_tareas_del_dia()
        calendario.calevent_create(fecha_obj, "Tarea", "tarea")
        calendario.tag_config("tarea", background="lightblue", foreground="black")
        entrada_tarea.delete(0, tk.END)

def mostrar_tareas_del_dia():
    lista_tareas.delete(0, tk.END)
    fecha_obj = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
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
        if fecha in tareas_por_fecha and tarea in tareas_por_fecha[fecha]:
            tareas_por_fecha[fecha].remove(tarea)

def ordenar_habitos():
    fecha = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
    if fecha in tareas_por_fecha:
        tareas_por_fecha[fecha].sort(key=lambda t: t.lstrip("✔ ").strip().lower())
        mostrar_tareas_del_dia()

def borrar_todos():
    if messagebox.askyesno("Confirmar", "¿Borrar todas las tareas del día actual?"):
        fecha = datetime.strptime(calendario.get_date(), "%d/%m/%y").date()
        tareas_por_fecha.pop(fecha, None)
        mostrar_tareas_del_dia()

def alternar_reloj():
    global mostrar_reloj
    mostrar_reloj = not mostrar_reloj
    reloj.grid_remove() if not mostrar_reloj else reloj.grid()

def mostrar_estadisticas():
    total = sum(len(t) for t in tareas_por_fecha.values())
    hechas = sum(1 for tareas in tareas_por_fecha.values() for t in tareas if t.startswith("✔ "))
    pendientes = total - hechas
    dias = len(tareas_por_fecha)
    mensaje = f"""📊 Estadísticas:\n\n- Tareas totales: {total}\n- Completadas: {hechas}\n- Pendientes: {pendientes}\n- Días con tareas: {dias}"""
    messagebox.showinfo("Estadísticas", mensaje)

def mostrar_acerca():
    mensaje = "Aplicación creada por el grupo del Informatorio 2025.\nIntegrantes: GRUPO 2."
    messagebox.showinfo("Acerca de", mensaje)

# ===== Login =====
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
